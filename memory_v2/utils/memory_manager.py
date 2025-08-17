#? sqlite3, json and numpy are for the db so we can create json entries and store them in the db
import sqlite3
import json
# numpy for handling arrays for fast retrieval
import numpy as np
# datetime for handling timestamps
# since i will make memories fade over time i need to keep an eye on whe it was created and updated
from datetime import datetime
import ast
# external func
from logs.funcs.log_prints import print_log_message
from memory_v2.funcs import faiss_search
from memory_v2.funcs.embedder import Embedder
from memory_v2.funcs.memory_utils import filter_with_fallback, second_level_filtering, third_level_filtering


class MemoryManager:    
    #* That will initialize the memory manager with a database path
    def __init__(self,similarity_threshold,db_path):      
        
        #* manage db
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
        
        #* create the database connection and table if it doesn't exist (only should work once)
        self.similarity_threshold = similarity_threshold
        self.embedder = Embedder()
        ids, vectors = self.load_all_memories()
        
        #* start FAISS search 
        self.faiss_engine = faiss_search.FAISS_SEARCH(ids, vectors)
    
    
        
    #* load all memories from the database but only id and embedding for faiss search
    def load_all_memories(self):
        self.cursor.execute('SELECT id, embedding FROM memories')
        results = self.cursor.fetchall()
        ids = []
        vectors = []

        for row in results:
            memory_id, emb_string = row
            embedding = np.array(ast.literal_eval(emb_string), dtype='float32')
            ids.append(memory_id)
            vectors.append(embedding)

        #? convert to numpy arrays for FAISS
        if len(vectors) == 0:
            return np.array([], dtype='int64'), np.empty((0, 384), dtype='float32')
        
        # ? ensure ids are in int64 format and vectors are in float32 format
        return np.array(ids, dtype='int64'), np.vstack(vectors).astype('float32')
        
        
        
        
    #* create the memories table if it doesn't exist
    def _create_table(self):
        #? some SQL code, CREATE will create something TABLE specified what to create, 
        #? IF NOT EXIST so the code only work if no table is there 
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            text TEXT,
            embedding TEXT,
            tokens TEXT,
            weight REAL,
            attachment REAL,
            lifespan INTEGER,
            last_used TEXT,
            memory_related_to TEXT
        )
        ''')
        self.conn.commit()
        
        
        
        
        
        
    #* now come the real functions that handle memory
    def add_new_memory(self, text, embedding, tokens, wight=1.0, attachment=1.0, lifespan=3600, memory_related_to="global"):
        
        #? more SQL code, INSERT INTO will insert data into the table specified
        self.cursor.execute('''
        INSERT INTO memories (text, embedding, tokens, weight, attachment, lifespan, last_used, memory_related_to)
        VALUES (?, ?, ?, ?, ?, ?, ?,?)
        ''', 
        (text, 
        json.dumps(embedding.tolist()), 
        json.dumps(tokens), wight, 
        attachment, lifespan, 
        datetime.now().isoformat(),
        memory_related_to))
        
        #? commit the changes to the database (i had to debug for a while to figure out that this is needed (0o0))
        self.conn.commit()
        
        
        #? update the loaded on ram data
        last_id = self.cursor.lastrowid
        # Add embedding to FAISS with the ID
        embedding_np = np.array(embedding, dtype='float32')

        # IDs must be numpy array of int64
        ids_np = np.array([last_id], dtype='int64')

        self.faiss_engine.index.add_with_ids(embedding_np, ids_np)
        
    
    # load all saved memories for displaying
    def get_all_for_view(self):
        self.cursor.execute("SELECT id, text FROM memories")
        result = self.cursor.fetchall()
        return result
        
    
    #load specific memory by filtering
    def get_memories(self, query ,user_name,limit=200, 
        user_related_ratio = 0.5, 
        other_users_related_ratio = 0.25, 
        globally_related_ratio = 0.25, 
        memories_count_threshold = 100,
    ):
        # get memories ids
        ids, distances = self.faiss_engine.search(query, limit)
        
        #? just to not end up debugging the wrong thing if something went wrong in the FAISS
        if ids is None:
            raise Exception("IDs array is empty or None")

        #? check if the FAISS is returning items where found
        if ids.size == 0:
            print_log_message("No Memories related were found!")
        
        #? filter
        filtered_list = filter_with_fallback(ids, distances, self.similarity_threshold)
        if(len(filtered_list) == 0):
            print_log_message("No Memories related were found After filtering!")
        
        
        #? SQL code to select the memories by id
        placeholders = ','.join('?' for _ in filtered_list)
        query = f"""
        SELECT id, text, weight, attachment, lifespan, last_used, memory_related_to 
        FROM memories 
        WHERE id IN ({placeholders}) 
        ORDER BY 
            CASE 
                WHEN memory_related_to = ? THEN 0
                WHEN memory_related_to NOT IN (?, 'global', 'self') THEN 1
                WHEN memory_related_to IN ('global', 'self') THEN 2
                ELSE 3
            END,
            weight DESC,
            attachment DESC,
            last_used DESC
        LIMIT {limit}
        """
        
        #? params 
        params = tuple(int(i) for i in filtered_list) + (user_name, user_name)
        
        # execute 
        self.cursor.execute(query, params)
        # fetch the items
        results = self.cursor.fetchall()
        
        #? filtering for the second time for closer response
        second_level_filtered_list = second_level_filtering(results)
        
        # final filtering layer to ensure relevant memory
        third_level_filtered_list = third_level_filtering(
            user_related_ratio, 
            other_users_related_ratio,
            globally_related_ratio,
            memories_count_threshold,
            user_name,
            second_level_filtered_list
        )
        
        if(len(third_level_filtered_list) == 0):
            print_log_message("No Memories related were found After Refiltering Second and Third Stage")
        
        return third_level_filtered_list
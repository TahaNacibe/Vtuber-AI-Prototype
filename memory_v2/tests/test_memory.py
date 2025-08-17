import unittest
import numpy as np
from datetime import datetime
from memory_v2.utils.memory_manager import MemoryManager

class DummyFAISS:
    def __init__(self):
        self.index = []
    
    def search(self, query, limit):
        return np.array([1, 2], dtype='int64'), np.array([0.5, 0.4])
    
    def add_with_ids(self, emb, ids):
        self.index.append((ids, emb))

class DummyEmbedder:
    def embed(self, text):
        return np.random.rand(384).astype('float32')

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = MemoryManager(similarity_threshold=0.3, db_path=":memory:")
        self.manager.faiss_engine = DummyFAISS()
        self.manager.embedder = DummyEmbedder()
    
    def test_add_and_view_memory(self):
        embedding = np.random.rand(384).astype('float32')
        tokens = ['this', 'is', 'test']
        
        self.manager.add_new_memory("Hello Memory!", embedding, tokens)
        all_memories = self.manager.get_all_for_view()
        
        self.assertEqual(len(all_memories), 1)
        self.assertIn("Hello Memory!", all_memories[0][1])

    def test_empty_search_result(self):
        self.manager.faiss_engine.search = lambda q, l: (np.array([], dtype='int64'), np.array([]))
        result = self.manager.get_memories("nothing found")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()

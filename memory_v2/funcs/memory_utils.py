import datetime
from collections import defaultdict

from logs.funcs.log_prints import print_error_message, print_log_message


# handle filtering the memories from the db data
def filter_with_fallback(ids, distances, threshold=1.65, fallback_k=50):
    filtered = [(i, d) for i, d in zip(ids, distances) if d < threshold]
    if filtered:
        return [i for i, _ in filtered]
    # fallback to top-k
    return [i for i, _ in sorted(zip(ids, distances), key=lambda x: x[1])[:fallback_k]]


# get the score for each memory just to keep retrieving the related ones
def calculate_score(memory):
    attachment = memory[3] 
    weight = memory[4]        
    last_used = datetime.datetime.fromisoformat(memory[5])
    recency = (datetime.datetime.now() - last_used).total_seconds()

    # Lower recency is better (more recent), so we can use negative weight
    score = (attachment * 0.5) + (weight * 0.3) - (recency * 0.0001)
    return score

# second stage filtering push important memories up 
def second_level_filtering(memories):
    sorted_memories = sorted(memories, key=calculate_score, reverse=True)
    return sorted_memories


def third_level_filtering(
    user_related_ratio=0.5,
    other_users_related_ratio=0.25,
    globally_related_ratio=0.25,
    memories_count_threshold=100,
    user_name=None,
    results=[]
):
    if not user_name:
        print_error_message("No User Related Name was supplied")
        return []
    
    if len(results) == 0:
        print_log_message("No Match Found Though Memory lookup")
        return []

    # Group memories by type
    memory_groups = defaultdict(list)
    for item in results:
        key = item[6]  # memory_related_to
        if key == user_name:
            memory_groups['user'].append(item)
        elif key in ("global", "self"):
            memory_groups['global_self'].append(item)
        else:
            memory_groups['others'].append(item)

    user_related = memory_groups['user']
    other_users = memory_groups['others']
    global_self = memory_groups['global_self']

    total_requested = memories_count_threshold

    # Calculate initial desired counts per category
    desired_counts = {
        'user': int(total_requested * user_related_ratio),
        'others': int(total_requested * other_users_related_ratio),
        'global_self': int(total_requested * globally_related_ratio)
    }

    # Available counts
    available_counts = {
        'user': len(user_related),
        'others': len(other_users),
        'global_self': len(global_self)
    }

    # Calculate leftover slots from categories with fewer items than requested
    leftover = 0
    for category in desired_counts:
        if available_counts[category] < desired_counts[category]:
            leftover += desired_counts[category] - available_counts[category]
            desired_counts[category] = available_counts[category]

    # Redistribute leftover slots to categories that still have capacity
    while leftover > 0:
        added = False
        for category in desired_counts:
            remaining_capacity = available_counts[category] - desired_counts[category]
            if remaining_capacity > 0:
                add_count = min(remaining_capacity, leftover)
                desired_counts[category] += add_count
                leftover -= add_count
                added = True
                if leftover == 0:
                    break
        if not added:  # No capacity left anywhere, break to avoid infinite loop
            break

    # Now slice the lists according to the adjusted desired counts
    user_selected = user_related[:desired_counts['user']]
    others_selected = other_users[:desired_counts['others']]
    global_selected = global_self[:desired_counts['global_self']]

    # Combine results preserving the order: user, others, global
    return user_selected + others_selected + global_selected
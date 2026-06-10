import time
import random
import tracemalloc
from typing import TypedDict, List, Dict, Set
from collections import defaultdict
from functools import reduce

# 1. DATA STRUCTURE DEFINITION
# Defines a custom type for activity records to ensure consistency
class Activity(TypedDict):
    user: str
    action: str
    duration: float

# 2. DATA PROCESSING FUNCTIONS

def total_time_per_user(logs: List[dict]) -> Dict[str, float]:
    """
    Calculates the cumulative duration spent by each user using 'reduce'.
    Logic: It processes the list in one pass, updating a dictionary 'accumulator'.
    """
    def accumulator(acc, record):
        # Adds the current record's duration to the user's running total
        acc[record["user"]] += record["duration"]
        return acc

    # reduce() applies the accumulator function across the logs list
    # defaultdict(float) initializes new users with a starting duration of 0.0
    totals = reduce(accumulator, logs, defaultdict(float))
    return dict(totals)

def most_active_users(logs: List[dict], k: int) -> List[str]:
  
    totals = total_time_per_user(logs)
    
    # items() converts the dict to a list of (user, time) tuples for sorting
    # key=lambda x: x[1] tells Python to sort based on the duration (the second element)
    sorted_users = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    
    # Returns only the usernames of the top k users
    return [user for user, _ in sorted_users[:k]]

def unique_actions(logs: List[dict]) -> Set[str]:
  
    return {record["action"] for record in logs}

# 3. MOCK DATA GENERATION

def generate_activities(n: int) -> List[Activity]:
    """
    Creates a list of 'n' random activity dictionaries for testing.
    The number of users scales slightly with the sample size (n // 10).
    """
    users = [f"USER{i}" for i in range(1, max(3, n // 10))]
    actions = [
        "visit leetcode", "download movies", "visit google ai studio", 
        "access VPN", "read bcrypt docs", "compile rust code", "watch youtube"
    ]
    
    return [
        {
            "user": random.choice(users),
            "action": random.choice(actions),
            "duration": round(random.uniform(10.0, 50000.0), 2)
        }
        for _ in range(n)
    ]

# 4. BENCHMARKING ENGINE

def measure_performance(func, *args, **kwargs):
    """
    A wrapper function to profile execution time and peak memory usage.
    """
    # Initialize memory tracking
    tracemalloc.start()
    
    # Use perf_counter for high-precision timing (better for small intervals)
    start_time = time.perf_counter()
    
    # Execute the target function with provided arguments
    func(*args, **kwargs)
    
    end_time = time.perf_counter()
    
    # Capture memory: current_mem is what's used now, peak_mem is the highest ever reached
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Convert results to readable units (Milliseconds and Kilobytes)
    time_ms = (end_time - start_time) * 1000
    peak_mem_kb = peak_mem / 1024
    
    return time_ms, peak_mem_kb

# 5. MAIN EXECUTION BLOCK

if __name__ == "__main__":
    # Test across different orders of magnitude (10 to 10,000)
    sample_sizes = [10, 100, 1000, 10000]

    for n in sample_sizes:
        print(f"--- Sampling for n = {n} ---")
        activity_records = generate_activities(n)

        # Performance test for Time per User (Tests Reduce + Dict overhead)
        time_ms, mem_kb = measure_performance(total_time_per_user, activity_records)
        print(f"  Total Time Per User -> Time: {time_ms:.4f} ms | Peak Memory: {mem_kb:.4f} KB")

        # Performance test for Sorting (Tests O(N log N) complexity)
        time_ms, mem_kb = measure_performance(most_active_users, activity_records, 5)
        print(f"  Most Active Users   -> Time: {time_ms:.4f} ms | Peak Memory: {mem_kb:.4f} KB")

        # Performance test for Set Deduplication (Tests Hashing speed)
        time_ms, mem_kb = measure_performance(unique_actions, activity_records)
        print(f"  Unique Actions      -> Time: {time_ms:.4f} ms | Peak Memory: {mem_kb:.4f} KB\n")
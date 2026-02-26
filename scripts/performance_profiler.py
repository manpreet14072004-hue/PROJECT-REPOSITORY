#!/usr/bin/env python3
"""
Performance profiling script for ML pipeline.
Measures execution time and resource usage.
"""

import time
import psutil
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def profile_performance(func):
    """Decorator to profile function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        logger.info(f"Starting {func.__name__}...")
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        logger.info(f"{func.__name__} completed in {execution_time:.2f}s")
        logger.info(f"Memory used: {memory_used:.2f} MB")
        
        return result
    
    return wrapper


@profile_performance
def example_function():
    """Example function to profile."""
    time.sleep(1)
    return "Complete"


if __name__ == "__main__":
    example_function()

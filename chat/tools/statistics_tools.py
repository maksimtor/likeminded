from functools import wraps
import time
from stats import tasks

def wrap_chat_stats():
	def decorate(fn):
		@wraps(fn)
		def wrapper(*args, **kwargs):
			start_time = time.perf_counter()
			result = fn(*args, **kwargs)
			end_time = time.perf_counter()
			total_time = end_time - start_time
			tasks.add_chat_stats.delay(args[1], total_time)
			return result
		return wrapper
	return decorate

def wrap_chat_stats_update_time(func):
	def wrapper(*args, **kwargs):
		result = func(*args, **kwargs)
		tasks.update_chat_stats_time.delay(result[0], time.perf_counter()-result[1])
		return result
	return wrapper
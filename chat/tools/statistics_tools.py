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
			print(kwargs)
			print(args[1])
			tasks.add_chat_stats.delay(args[1], total_time)
			return result
		return wrapper
	return decorate
import multiprocessing
import os
from pathlib import Path

import yaml


# worker
cores = multiprocessing.cpu_count()
workers_per_core = float(os.getenv("WORKER_PER_CORE", "1"))
max_workers = int(os.getenv("MAX_WORKERS", "0"))
default_web_concurrency = workers_per_core * cores
if max_workers > 0:
    worker_nums = int(max(default_web_concurrency, max_workers))
else:
    worker_nums = int(default_web_concurrency)
max_threads = int(os.getenv("MAX_THREADS", "0"))
if max_workers > 0:
    thread_nums = int(max(default_web_concurrency, max_threads))
else:
    thread_nums = int(default_web_concurrency)

# bind
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")

# log
log_filepath = Path(__file__) / "gunicorn_log_config.yml"
with open(log_filepath, "r") as f:
    log_config = yaml.safe_load(f.read())

# gunicorn config variables
bind = f"{host}:{port}"
worker_tmp_dir = "/dev/shm"
workers = max(worker_nums, 2)
threads = max(thread_nums, 2)
max_reqests = int(os.getenv("MAX_REQUESTS", "500"))
max_reqursts_jitter = int(os.getenv("MAX_REQUESTS_JITTER", "100"))
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "120"))
timeout = int(os.getenv("TIMEOUT", "120"))
keepalive = int(os.getenv("KEEP_ALIVE", "75"))
log_config_dict = log_config

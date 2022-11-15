from __future__ import print_function

import json
import multiprocessing
import os


def to_bool(s: str) -> bool:
    if s is not None:
        return s.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
    else:
        return False


env = os.getenv('ENVIRONMENT', 'dev')
use_loglevel = os.getenv("LOG_LEVEL", "info")
host = os.getenv("HOST", "127.0.0.1")
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", "1")
max_requests_str = os.getenv('MAX_REQUESTS', "0")
reload_str = os.getenv('CODE_RELOAD', "0")
port = os.getenv("PORT", "8000")

se_bind = "{host}:{port}".format(host=host, port=port)
cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
max_requests = int(max_requests_str)
reload = to_bool(reload_str)

if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = int(default_web_concurrency)

if env == 'dev':
    pass
elif env in ('prod', 'staging'):
    pass


# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = "{host}:{port}".format(host=host, port=port)
keepalive = 120
errorlog = "-"

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "max_requests": max_requests,
    "bind": bind,
    'reload': reload,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
}
print(json.dumps(log_data, indent=2))

#!/usr/bin/env python3
from api.db import start_redis_server, stop_redis_server
from api.args import get_args
from api.files import list_videos
from api.cache import get_cache_dir

def start():
    print("Running scan")

    args = get_args()
    start_redis_server()
    videos = list_videos()
    stop_redis_server()

if __name__ == "__main__":
    start()

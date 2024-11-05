#!/usr/bin/env python3
from api.db import start_redis_server, stop_redis_server
from api.args import get_args
from api.tags import get_resources_without_tags
from api.files import get_videos_by_ids
from api.cache import get_cache_dir

def start():
    print("Running auto")

    args = get_args()
    start_redis_server()
    untagged = get_resources_without_tags()
    videos = get_videos_by_ids(untagged[0:10])
    for video in videos:
        print(video)
    stop_redis_server()

if __name__ == "__main__":
    start()

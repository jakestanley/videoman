#!/usr/bin/env python3
from api.db import start_redis_server, stop_redis_server
from api.args import get_args
from api.tags import get_resources_without_tags
from api.files import get_videos_by_ids
from api.auto import assume_tags

def start():
    print("Running auto")

    args = get_args()
    start_redis_server()
    untagged = get_resources_without_tags()
    videos = get_videos_by_ids(untagged[0:10])
    for video in videos:
        tags = assume_tags(video)
        print(f"Assumed tags for video %s: %s" % (video["relative_path"], tags))
    stop_redis_server()

if __name__ == "__main__":
    start()

#!/usr/bin/env python3
import os

from api.db import start_redis_server, stop_redis_server
from api.args import get_cleanup_args
from api.files import get_videos_by_ids, remove_video, get_videos
import api.tags as tags

def start():
    print("Running scan")

    args = get_cleanup_args()
    start_redis_server()
    deletable_ids = tags.get_resources_by_tag("delete")
    videos = get_videos_by_ids(deletable_ids)
    video_directory = get_cleanup_args().video_directory

    for video in videos:
        full_path = os.path.join(video_directory, video['relative_path'])
        if os.path.exists(full_path):
            if args.apply:
                print(f"Deleting video '{full_path}'")
                os.remove(full_path)
            else:
                print(f"Would delete video '{full_path}' (run with --apply to delete for real)")

    # check all remaining videos and remove any from the DB that no longer exist on disk (including previews)
    videos = get_videos()
    for video in videos:
        full_path = os.path.join(video_directory, video['relative_path'])
        if not os.path.exists(full_path):
            remove_video(video['relative_path'])

    stop_redis_server()

if __name__ == "__main__":
    start()

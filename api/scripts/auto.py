#!/usr/bin/env python3
from collections import Counter

from api.db import start_redis_server, stop_redis_server
from api.args import get_auto_args
from api.tags import get_resources_without_tags
from api.files import get_videos_by_ids
from api.auto import assume_tags
from api.tags import add_tag_to_resource

def start():
    print("Running auto on untagged videos")

    args = get_auto_args()
    start_redis_server()
    untagged = get_resources_without_tags()
    videos = get_videos_by_ids(untagged)

    all_tags = []

    # get potential tags for all videos
    for video in videos:
        video_tags = assume_tags(video)
        video['potential_tags'] = video_tags

        # add to list of all tags
        all_tags.extend(video_tags)

    # reduce list of tags to a set of ones that occur more than once only
    unique_tags_occurring_more_than_once = set()

    counts = Counter(all_tags)
    for value, count in counts.items():
        if count > 1:
            unique_tags_occurring_more_than_once.add(value)

    # reduce potential_tags to tags contained in the "occur more than once" set
    for video in videos:
        potential_tags = video['potential_tags']
        video['potential_tags'] = [tag for tag in potential_tags if tag in unique_tags_occurring_more_than_once]
        print(f"Assumed tags for video %s: %s" % (video["relative_path"], video['potential_tags']))

    # apply tags if such argument is true
    if args.apply:
        print("Applying tags")
        for video in videos:
            for tag in video['potential_tags']:
                try:
                    add_tag_to_resource(video['id'], tag)
                except ValueError as e:
                    print(f"Error adding tag '{tag}' to video '{video['relative_path']}': {e}")

    stop_redis_server()

if __name__ == "__main__":
    start()

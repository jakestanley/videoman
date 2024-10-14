import os
import hashlib
import uuid
import redis

from tabulate import tabulate
import json

from api.args import get_args
from api.preview import generate_preview
from api.cache import get_cache_dir
from api.tags import get_tags_by_resource
from api.db import get_redis_client

# TODO: scanner worker/background task
# TODO: if the user deletes a video and the video at that path does not match 
#   the loaded hash, we will not delete the video at that path. as this means 
#   that the video has moved or changed. we must omit any videos scanned that 
#   do not have matching hashes and create new IDs for them
class Video:
    def __init__(self, parent_directory, relative_path, id=None, hash=None):
        # TODO store with pickledb
        full_path = os.path.join(parent_directory, relative_path)

        self.parent_directory = parent_directory
        self.relative_path = relative_path
        # calculates the hash every time, not very efficient

        
#        if hash is None:
#            hasher = hashlib.sha256()
#            with open(full_path, 'rb') as f:
#                buf = f.read()
#                hasher.update(buf)
#            self.hash = hasher.hexdigest()
        self.hash = None

        if id is None:
            self.id = uuid.uuid4()

    def dictify(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'relative_path': self.relative_path
        }

def get_video_by_id(uuid):
    r = get_redis_client()
    obj = r.hgetall(uuid)  # Fetch the hash for the given UUID
    safe_obj = {}
    if obj == {}:
        return {}
    safe_obj['id'] = obj['id']
    safe_obj['contents_hash'] = obj['contents_hash']
    safe_obj['relative_path'] = obj['relative_path']
    safe_obj['created'] = obj['created']
    safe_obj['tags'] = list(get_tags_by_resource(resource_id=uuid))

    return safe_obj

def hash_file_path(file_path):
    return hashlib.sha256(file_path.encode('utf-8')).hexdigest()

def get_videos():
    r = get_redis_client()

    all_uuids = r.smembers('uuids')
    all_videos = []

    for uuid in all_uuids:
        # Assuming each object is stored in a hash with key pattern 'uuid:<uuid>'
        video = get_video_by_id(uuid)
        if video == {}:
            continue

        all_videos.append(video)

    return all_videos

def get_videos_by_ids(ids):
    videos = []
    for id in ids:
        video = get_video_by_id(id)
        if video == {}:
            continue

        videos.append(video)
    return videos

def process_video_file(relative_path):
    video_directory = get_args().video_directory

    print(f"Processing '{relative_path}",end=' ')
    r = get_redis_client()

    try:
        id = None

        full_path = os.path.join(video_directory, relative_path)
        file_path_hash = hash_file_path(full_path)

        id = r.get(file_path_hash)
        if id is None:
            id = str(uuid.uuid4())
            print(f"Creating: '{id}'", end=' ')

            # add uuids to a set so we can query them efficiently later
            r.sadd('uuids', id)

            r.set(file_path_hash, id)
        else:
            print(f"Exists: '{id}'", end=' ')

        video = r.hgetall(id)

        # new video
        if video == {}:

            hasher = hashlib.sha256()
            try:
                with open(full_path, 'rb') as f:
                    buf = f.read()
                    hasher.update(buf)
                hash = hasher.hexdigest()
            except MemoryError as e:
                print(f"MemoryError encountered when hashing {relative_path}")
                r.srem('uuids', id)
                return

            video = {
                'id': id,
                'relative_path': relative_path,
                'created': os.path.getctime(full_path),
                'modified': os.path.getmtime(full_path),
                'contents_hash': hash
            }
        else:
            # set created date if it does not exist
            if not video.get('created'):
                video['created'] = os.path.getctime(full_path)
            # if video has modified key and it has not changed, skip the rehash
            if video.get('modified') and video['modified'] == f"{os.path.getmtime(full_path)}":
                print(f"Modified: No", end=' ')
            else:
                print(f"Modified: Yes", end=' ')
                hasher = hashlib.sha256()
                with open(full_path, 'rb') as f:
                    buf = f.read()
                    hasher.update(buf)
                hash = hasher.hexdigest()

                video['modified'] = os.path.getmtime(full_path)
                video['contents_hash'] = hash

        # save the video to redis
        r.hset(id, mapping=video)

        # generate gif if it doesn't exist for this hash
        cache_dir = get_cache_dir(video_directory)
        gif_output_path = os.path.join(cache_dir, f"{video['contents_hash']}.webm")
        if not os.path.exists(gif_output_path):
            print(f"GIF: Generating", end=' ')
            try:
                generate_preview(video_path=full_path, gif_output_path=gif_output_path)
                print(f" (OK)")
            except ValueError as e:
                print(f" (Error)")
        else:
            print(f"GIF: Exists")

    except FileNotFoundError as e:
        print(f"Failed to process {relative_path}")
    except NotADirectoryError:
        print(f"The path '{video_directory}' is not a directory.")

def list_videos():
    video_directory = get_args().video_directory
    video_extensions = video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.m4v'}

    print(f"Scanning '{video_directory}' for video files...")
    exclude_dirs = [".videoman-cache"]
    for dirpath, dirnames, files in os.walk(video_directory):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for file in files:
            if file.startswith('.'):
                continue
            if os.path.splitext(file)[1].lower() in video_extensions:
                relative_path = os.path.relpath(os.path.join(dirpath, file), video_directory)
                process_video_file(relative_path)

if __name__ == '__main__':
    list_videos('/Users/jake/Movies/BATW2/')

import os
import hashlib
import uuid
import redis

from tabulate import tabulate
import json

from api.args import get_args
from api.preview import generate_preview
from api.cache import get_cache_dir

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
            'path': self.relative_path
        }

def hash_file_path(file_path):
    return hashlib.sha256(file_path.encode('utf-8')).hexdigest()

def load_files():
    pass

def process_video_file(video_file):
    video_directory = get_args().video_directory

    print(f"Processing '{video_file}",end=' ')
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    try:
        id = None

        file_path_hash = hash_file_path(video_file)
        video_path = os.path.join(video_directory, video_file)

        id = r.get(file_path_hash)
        if id is None:
            id = str(uuid.uuid4())
            print(f"Creating: '{id}'", end=' ')
            r.set(file_path_hash, id)
        else:
            print(f"Exists: '{id}'", end=' ')

        video = r.hgetall(id)

        # new video
        if video == {}:

            hasher = hashlib.sha256()
            with open(video_path, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            hash = hasher.hexdigest()

            video = {
                'id': id,
                'path': video_path,
                'modified': os.path.getmtime(video_path),
                'contents_hash': hash
            }
        # if video has modified key and it has not changed, skip the rehash
        else:
            # TODO: if modified has changed, recalculate the hash
            if video.get('modified') and video['modified'] == f"{os.path.getmtime(video_path)}":
                print(f"Modified: No", end=' ')
            else:
                print(f"Modified: Yes", end=' ')
                hasher = hashlib.sha256()
                with open(video_path, 'rb') as f:
                    buf = f.read()
                    hasher.update(buf)
                hash = hasher.hexdigest()

                video['modified'] = os.path.getmtime(video_path)
                video['contents_hash'] = hash

        # save the video to redis
        r.hset(id, mapping=video)

        # generate gif if it doesn't exist for this hash
        cache_dir = get_cache_dir(video_directory)
        gif_output_path = os.path.join(cache_dir, f"{video['contents_hash']}.gif")
        if not os.path.exists(gif_output_path):
            print(f"GIF: Generating")
            try:
                generate_preview(video_path=video_path, gif_output_path=gif_output_path)
            except ValueError as e:
                print(f"Error generating preview for {video_path}: {e}")
        else:
            print(f"GIF: Exists")

    except FileNotFoundError as e:
        print(f"Failed to process {video_file}")
    except NotADirectoryError:
        print(f"The path '{video_directory}' is not a directory.")

def list_videos():
    video_directory = get_args().video_directory
    video_extensions = video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.m4v'}

    print(f"Scanning '{video_directory}' for video files...")
    for dirpath, _, files in os.walk(video_directory):
        for file in files:
            if file.startswith('.'):
                continue
            if os.path.splitext(file)[1].lower() in video_extensions:
                process_video_file(os.path.relpath(os.path.join(dirpath, file), video_directory))

if __name__ == '__main__':
    list_videos('/Users/jake/Movies/BATW2/')

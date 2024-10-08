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

def list_videos():
    video_directory = get_args().video_directory
    videos = []
    # List all files in the directory

    r = redis.Redis(host='localhost', port=6379, db=0)

    try:

        video_extensions = video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm'}
        video_files = []

        for root, dirs, files in os.walk(video_directory):
            for file in files:
                if file.startswith('.'):
                    continue
                if os.path.splitext(file)[1].lower() in video_extensions:
                    video_files.append(file)

        print(f"Files in '{video_directory}':")

        for video_file in video_files:
            id = None
            file_path_hash = hash_file_path(video_file)

            id = r.get(file_path_hash)
            if id is None:
                id = str(uuid.uuid4())
                r.set(file_path_hash, id)

            # TODO: might need some
            video = r.hgetall(id)
            if video == {}:

                hasher = hashlib.sha256()
                with open(os.path.join(video_directory, video_file), 'rb') as f:
                    buf = f.read()
                    hasher.update(buf)
                hash = hasher.hexdigest()

                video = {
                    'id': id,
                    'path': os.path.join(video_directory, video_file),
                    'modified': os.path.getmtime(os.path.join(video_directory, video_file)),
                    'contents_hash': hash
                }

                r.hset(id, mapping=video)
            else:
                # TODO: if modified has changed, recalculate the hash
                if video.get('modified'):
                    if video['modified'] == os.path.getmtime(os.path.join(video_directory, video_file)):
                        print("modified date unchanged")
                    else:
                        # TODO recalculate that hash and mset/hset i forget which it is
                        r.hset(id, 'modified', os.path.getmtime(os.path.join(video_directory, video_file)))
                        print("modified date changed, i'll need to recalculate the hash")
                else:
                    print("modified date never set, i'll need to calculate the hash")
                    r.hset(id, 'modified', os.path.getmtime(os.path.join(video_directory, video_file)))
                    # TODO calculate hash

            
            continue







        
        for video_file in video_files:
            videos.append(Video(parent_directory=video_directory, relative_path=video_file))

        for video in videos:
            try:
                generate_preview(os.path.join(video.parent_directory, video.relative_path))
            except ValueError as e:
                print(f"Error generating preview for {video.relative_path}: {e}")

        table_data = [[video.id, video.hash, os.path.join(video.parent_directory, video.relative_path)] for video in videos]
        
        headers = ["ID", "Hash", "Path"]

        # print(tabulate(table_data, headers=headers, tablefmt='pretty'))
    except FileNotFoundError as e:
        print(f"The directory '{video_directory}' does not exist.")
    except NotADirectoryError:
        print(f"The path '{video_directory}' is not a directory.")

    return videos

if __name__ == '__main__':
    list_videos('/Users/jake/Movies/BATW2/')

import os
import hashlib
import uuid

from tabulate import tabulate

# TODO: scanner worker/background task
# TODO: if the user deletes a video and the video at that path does not match 
#   the loaded hash, we will not delete the video at that path. as this means 
#   that the video has moved or changed. we must omit any videos scanned that 
#   do not have matching hashes and create new IDs for them
class Video:
    def __init__(self, parent_directory, relative_path, id=None, hash=None):

        full_path = os.path.join(parent_directory, relative_path)

        self.parent_directory = parent_directory
        self.relative_path = relative_path
        # calculates the hash every time, not very efficient

        
        if hash is None:
            hasher = hashlib.sha256()
            with open(full_path, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            self.hash = hasher.hexdigest()

        if id is None:
            self.id = uuid.uuid4()

    def dictify(self):
        return {
            'id': self.id,
            'hash': self.hash,
            'path': self.relative_path
        }

def load_files(video_directory):
    pass

def list_videos(video_directory):
    videos = []
    # List all files in the directory
    try:

        video_extensions = video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm'}

        video_files = [
            f for f in os.listdir(video_directory)
            if os.path.isfile(os.path.join(video_directory, f)) and
            os.path.splitext(f)[1].lower() in video_extensions
        ]

        print(f"Files in '{video_directory}':")
        
        for video_file in video_files:
            videos.append(Video(parent_directory=video_directory, relative_path=video_file))

        table_data = [[video.id, video.hash, os.path.join(video.parent_directory, video.relative_path)] for video in videos]
        headers = ["ID", "Hash", "Path"]

        print(tabulate(table_data, headers=headers, tablefmt='pretty'))
    except FileNotFoundError:
        print(f"The directory '{video_directory}' does not exist.")
    except NotADirectoryError:
        print(f"The path '{video_directory}' is not a directory.")

    return videos

if __name__ == '__main__':
    list_videos('/Users/jake/Movies/BATW2/')

import os
import shutil

def get_cache_dir(video_directory):
    cache_dir = os.path.join(video_directory, '.videoman-cache')
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir
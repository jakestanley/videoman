import argparse

_SINGLETON = None

def get_args():
    global _SINGLETON
    if _SINGLETON is None:
        # Set up argument parsing
        parser = argparse.ArgumentParser(description="Videoman API")
        parser.add_argument(
            '-v',
            '--video-directory',
            '-d',
            '--dev',
            type=str, 
            help='The root directory to scan for videos.'
        )
        _SINGLETON = parser.parse_args()
    return _SINGLETON

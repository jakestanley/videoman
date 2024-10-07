import os
import argparse

def get_args():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Videoman API")
    parser.add_argument(
        '-v',
        '--video-directory', 
        type=str, 
        help='The root directory to scan for videos.'
    )
    return parser.parse_args()

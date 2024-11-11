import argparse

_SINGLETON = None

def _get_common_args_parser():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Videoman API")
    parser.add_argument(
        '-v',
        '--video-directory',
        '-d',
        '--dev',
        type=str, 
        required=True,
        help='The root directory to scan for videos.'
    )
    return parser

def get_args():
    global _SINGLETON
    if _SINGLETON is None:
        parser = _get_common_args_parser()
        _SINGLETON = parser.parse_args()
    return _SINGLETON

def get_auto_args():
    global _SINGLETON
    if _SINGLETON is None:
        parser = _get_common_args_parser()
        parser.add_argument(
            '-a',
            '--apply',
            action='store_true',
            help='Apply the auto tagging'
        )
        _SINGLETON = parser.parse_args()
    return _SINGLETON

def get_cleanup_args():
    global _SINGLETON
    if _SINGLETON is None:
        parser = _get_common_args_parser()
        parser.add_argument(
            '-a',
            '--apply',
            action='store_true',
            help='Apply destructive operations'
        )
        _SINGLETON = parser.parse_args()
    return _SINGLETON

import os
import subprocess
import redis

from api.args import get_args
from api.cache import get_cache_dir

def start_redis_server():

    args = get_args()
    redis_dir = os.path.join(get_cache_dir(args.video_directory), 'redis')
    os.makedirs(redis_dir, exist_ok=True)

    # Define the command to start Redis with desired configurations
    redis_process = subprocess.Popen([
        'redis-server', 
        '--save', '900 1',
        '--save', '300 10',
        '--dir', redis_dir,  # Change to your desired path
        '--dbfilename', 'dump.rdb',
        '--appendonly', 'yes',
        '--appendfilename', 'appendonly.aof',
        '--appendfsync', 'everysec',
        '--daemonize', 'yes'  # Run Redis as a background process
    ])
    
    return redis_process  # Return the process for later use

def stop_redis_server():
    redis_client = redis.StrictRedis(host='localhost', port=6379)

    # Send the shutdown command
    try:
        redis_client.shutdown()
        print("Redis server stopped.")
    except redis.exceptions.ConnectionError as e:
        print("Redis server already stopped or not running:", e)

def get_redis_client():
    # TODO ensure we're getting the right redis ofc
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
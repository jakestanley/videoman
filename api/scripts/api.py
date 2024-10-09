import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from api.args import get_args
from api.cache import get_cache_dir
from api.db import start_redis_server, stop_redis_server
from api.files import get_videos as fget_videos



args = get_args()
# TODO make sure we don't share redis files, consider using a subdirectory in the cache for those
app = Flask(__name__, static_folder=get_cache_dir(args.video_directory), static_url_path="/assets")
CORS(app, origins=["http://localhost:5000", "http://localhost:8080"])

@app.route("/")
def home():
    return jsonify({"message": "UP"})
# TODO move these into a routes or web package?
@app.route("/videos", methods=['GET'])
def get_videos():

    videos = fget_videos()
    # TODO serve static content
    # videos = [video.dictify() for video in list_videos()]
    # return jsonify(videos)
    return jsonify(videos)

# TODO write a cleanup script for testing
def start():
    stop_redis_server()
    start_redis_server()
    app.run(debug=False)

if __name__ == '__main__':
    start()

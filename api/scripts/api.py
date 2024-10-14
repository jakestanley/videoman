from flask import Flask, jsonify, request

from api.args import get_args
from api.cache import get_cache_dir
from api.db import start_redis_server, stop_redis_server
from api.files import get_videos as fget_videos, get_videos_by_ids
from api.security import setup_cors
import api.tags as tags

args = get_args()
# TODO make sure we don't share redis files, consider using a subdirectory in the cache for those
app = Flask(__name__, static_folder=get_cache_dir(args.video_directory), static_url_path="/assets")
setup_cors(app)

def paginate_items(items, page, page_size=20):
    start = page * page_size
    end = start + page_size
    return items[start:end]

@app.route("/")
def home():
    return jsonify({"message": "UP"})
# TODO move these into a routes or web package?
@app.route("/videos", methods=['GET'])
def get_videos():
    page = request.args.get('page', 0, type=int)

    videos = fget_videos()
    paged = paginate_items(videos, page, page_size=20)

    return jsonify(paged)

@app.route("/tags/<tag>/videos", methods=['GET'])
def get_videos_by_tag(tag):
    page = request.args.get('page', 0, type=int)

    ids = []
    if tag == 'untagged':
        ids = tags.get_resources_without_tags()
    else:
        ids = tags.get_resources_by_tag(tag)
    videos = get_videos_by_ids(ids)
    paged = paginate_items(videos, page, page_size=20)

    return jsonify(paged)

@app.route("/tags", methods=['GET'])
def get_tags():
    return jsonify(tags.list_all_tags())

@app.route("/videos/<video_id>/tags/<tag>", methods=['POST'])
def add_tag(video_id, tag):
    tags.add_tag_to_resource(resource_id=video_id, tag=tag)
    return jsonify({"message": "Tag added successfully"})

@app.route("/videos/<video_id>/tags/<tag>", methods=['DELETE'])
def remove_tag(video_id, tag):
    tags.remove_tag_from_resource(resource_id=video_id, tag=tag)
    return jsonify({"message": "Tag removed successfully"})

# TODO write a cleanup script for testing
def start():
    # stop_redis_server() # TODO: check if already running redis server
    start_redis_server()
    app.run(debug=False)

if __name__ == '__main__':
    start()

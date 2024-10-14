import re

from api.db import get_redis_client

def _validate_tag(tag):
    tag = tag.lower()
    # Define the regular expression for alphanumeric tags with underscores
    pattern = r'^[a-zA-Z0-9_]+$'
    
    # Check if the tag matches the pattern and is not "untagged"
    if re.match(pattern, tag) and tag.lower() != 'untagged':
        return tag
    else:
        raise ValueError(f"Invalid tag: '{tag}'")

# Add tags to a resource and vice versa
def add_tag_to_resource(resource_id, tag):
    tag = _validate_tag(tag)
    r = get_redis_client()
    # Add resource to tag set
    r.sadd(f'tag:{tag}', resource_id)
    # Add tag to resource set
    r.sadd(f'resource:{resource_id}', tag)

def remove_tag_from_resource(resource_id, tag):
    tag = _validate_tag(tag)
    r = get_redis_client()
    # Remove the resource from the tag's set
    r.srem(f'tag:{tag}', resource_id)
    # Remove the tag from the resource's set
    r.srem(f'resource:{resource_id}', tag)

    # Optionally, if the tag set becomes empty, you can delete the tag key
    if r.scard(f'tag:{tag}') == 0:
        r.delete(f'tag:{tag}')

# Get all resources with a specific tag
def get_resources_by_tag(tag):
    r = get_redis_client()
    return r.smembers(f'tag:{tag}')  # Returns a set of resource IDs

def get_resources_without_tags():
    r = get_redis_client()

    untagged_resources = []
    ids = r.smembers('uuids')  # Assuming you maintain a set of all resources
    
    for resource_id in ids:
        # Check if the resource has any tags (if the set is empty)
        if r.scard(f'resource:{resource_id}') == 0:
            untagged_resources.append(resource_id)

    return untagged_resources

# Get all tags for a specific resource
def get_tags_by_resource(resource_id):
    r = get_redis_client()
    return r.smembers(f'resource:{resource_id}')  # Returns a set of tags

# List all tags (using SCAN command to find all tag:* keys)
def list_all_tags():
    r = get_redis_client()
    cursor = 0
    tags = []
    # TODO fix laziness
    tags.append({'tag': 'untagged', 'resource_count': 999999})
    while True:
        cursor, keys = r.scan(cursor, match='tag:*')
        for key in keys:
            tag = key.split(':', 1)[1]  # Extract the tag name
            resource_count = r.scard(f"tag:{tag}")
            tags.append({'tag': tag, 'resource_count': resource_count})
        if cursor == 0:
            break

    tags.sort(key=lambda x: x['resource_count'], reverse=True)
    return tags

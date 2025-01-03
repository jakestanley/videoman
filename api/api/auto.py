import os
import re

from datetime import datetime
from pathlib import Path

from api.db import get_redis_client

date_pattern = r"(\d{4}-?\d{2}-?\d{2})"

def _get_ctime_date(video):
    dt_object = datetime.fromtimestamp(float(video['created']))
    ctime_date = dt_object.date()
    return ctime_date

def _get_filename_date(video):
    filename = os.path.basename(video['relative_path'])

    match = re.search(date_pattern, filename)

    dt_object = None

    if match:
        date_str = match.group(1)
    else:
        return None

    try:
        dt_object = datetime.strptime(date_str, '%Y-%m-%d')

        r = get_redis_client()

        timestamp = f"{dt_object.timestamp()}"

        r.hset(video['id'], "created", timestamp)

    except ValueError:
        pass

    if dt_object is None:
        try:
            dt_object = datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            return None

    ftime_date = dt_object.date()
    return ftime_date

def _get_other_tags(video):

    pattern = r"\b\d{4}-?\d{2}-?\d{2}(?:[\s_-](\d{2}[-_:]\d{2}(?:[-_:]\d{2})?))?\b"

    tags = set()

    # Remove all matches of dates and times
    components = list(Path(video['relative_path']).parts)
    cleaned_components = []
    for component in components:
        try:
            component, _ = os.path.splitext(component)
            component = component.replace("[", "").replace("]", "")
            cleaned_components.append(re.sub(pattern, "", component))
        except AttributeError as e:
            print("AttributeError thrown")

    # remove empty strings and split components into individual tags
    for component in cleaned_components:
        tags.update(set([item for item in component.split(" ") if item]))

    # remove any leading special characters from tags
    tags = set([re.sub(r'^[^a-zA-Z0-9]+', '', tag) for tag in tags])

    return list(tags)

def assume_tags(video):

    tags = []

    # you'll need to format ctime_date before you use it as a tag
    ftime_date = _get_filename_date(video)
    if ftime_date is not None:
        tags.append(ftime_date.strftime('%Y-%m-%d'))
        tags.append(f"{ftime_date.year}")
    else:
        ctime_date = _get_ctime_date(video)
        tags.append(ctime_date.strftime('%Y-%m-%d'))
        tags.append(f"{ctime_date.year}")

    tags.extend(_get_other_tags(video))

    excluded_tags = ["delete"]
    tags = [tag for tag in tags if tag and tag.lower() not in excluded_tags]

    return tags
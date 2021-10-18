"""
Fast, in-memory DB ;)
"""
import json
from enum import Enum
from copy import copy
from lib.utils import get_abs_path, pad_list_right

# titles table, loaded form JSON file
TITLES_FILE = 'etc/data.json'
TITLES_DATA = []


class TitlesColumns(str, Enum):
    id = "id"
    title_number = "title_number"
    title_class = "title_class"
    content = "content"


def init():
    """
        Init the in-memory DB.
        Loads JSON file, perform any initial processing
    """
    TITLES_DATA.clear()
    TITLES_DATA.extend(_load_titles())


def _load_titles():
    """ Loads data.json file and returns as list of dicts """
    json_path = get_abs_path(TITLES_FILE)
    with open(json_path, 'r') as f:
        titles_list = json.load(f)
    for title in titles_list:
        try:
            title[TitlesColumns.id.value] = int(title[TitlesColumns.id.value])
        except (ValueError, TypeError):
            pass
    return titles_list


def filter_data(data, title_class: str):
    """ ToDo: this will be easier to extend once migrated to SQL """
    res = []  # python optimizes array extension reasonably, so won't worry about it here for now
    for title in data:
        if title[TitlesColumns.title_class].lower() == title_class.lower():
            res.append(title)
    return res


def sort_data(data, _sort, _order):
    # Some thoughts on sorting:
    # * Eventually I went with sorting multiple times, as this is simplest to read.
    #   (It will take twice as long as single pass though)
    # * Python does not easily support sorting by multiple strings descending/ascending
    #   (it'd be possible in this particular case with 1 str and 1 num, but code would be tough to read)
    # * For a strategic solution I imagine the data is in an SQL DB rather than memory, where this problem goes away.
    sort_cols = [sort_col.strip() for sort_col in _sort.split(',')]
    sort_orders = [sort_order.strip() for sort_order in _order.split(',')]
    pad_list_right(sort_orders, 'asc', len(sort_cols))  # some default 'asc' if missing
    sorted_titles = copy(data)  # shallow copy, just list not the dicts
    for sort_col, sort_order in zip(reversed(sort_cols), reversed(sort_orders)):
        is_desc = sort_order.lower() == 'desc'
        if sorted_titles and sort_col not in sorted_titles[0]:
            raise RuntimeError('Column not found: "{}"'.format(sort_col))
        sorted_titles.sort(key=lambda x: x.get(sort_col, ''), reverse=is_desc)
    return sorted_titles


def paginate_data(data, page, limit):
    """ Calculate start/end indices for paginated list
        Example:
             full_list = list(range(101))
             page_list = paginate_list(full_list, 3, 10)
             page_list == [20, 21, 22, ..., 29]


    """
    if page > 0 and limit > 0:
        idx_start = (page - 1) * limit
        idx_end = idx_start + limit
        if idx_start >= len(data):
            return []
        else:
            return data[idx_start:idx_end]
    else:
        return copy(data)

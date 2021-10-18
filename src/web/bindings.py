import lib.db


def find_title_by_id(title_id: int):
    """
    Search for a specific title id.
    This may need to be made faster eventually
    """
    for title in lib.db.TITLES_DATA:
        if title['id'] == title_id:
            return title
    raise RuntimeError('Could not find title ID: "{}" in DB'.format(title_id))


def find_titles(title_class: str, _sort, _order, _page, _limit):
    """
    Search for titles.
    ToDo: adding/removing titles will make pagination unstable
    """
    # optional filter by title_class
    if title_class:
        filtered_titles = lib.db.filter_data(lib.db.TITLES_DATA, title_class)
    else:
        filtered_titles = lib.db.TITLES_DATA

    # optional sort
    if _sort:
        sorted_titles = lib.db.sort_data(filtered_titles, _sort, _order)
    else:
        sorted_titles = filtered_titles

    # optional paginate
    paginated_titles = lib.db.paginate_data(sorted_titles, _page, _limit)

    # format
    formatted_titles = []
    for title in paginated_titles:
        formatted_titles.append(
            {
                lib.db.TitlesColumns.id.value: title.get(lib.db.TitlesColumns.id.value),
                lib.db.TitlesColumns.title_number.value: title.get(lib.db.TitlesColumns.title_number.value),
                lib.db.TitlesColumns.title_class.value: title.get(lib.db.TitlesColumns.title_class.value),
            }
        )

    return formatted_titles

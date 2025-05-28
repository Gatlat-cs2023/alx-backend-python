def access_nested_map(nested_map, path):
    """Access a nested map with a path of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_sub_dict(data: dict, keys: list) -> dict:
    """
    Returns a sub-dictionary containing only the specified
    keys from the original dictionary.

    :param data: The original dictionary
    :param keys: A list of keys to extract
    :return: A new dictionary with only the specified keys
    """
    return {k: data[k] for k in keys if k in data}
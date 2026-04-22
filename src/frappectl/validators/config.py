def has_required_keys(data: dict, keys: list[str]) -> bool:
    return all(key in data and data[key] not in (None, "") for key in keys)
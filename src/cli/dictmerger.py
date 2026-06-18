
def merge_dicts(base: dict, override: dict, additive: bool) -> dict:
    result = base.copy()

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = merge_dicts(result[key], value, additive)
        elif (
            key in result
            and isinstance(result[key], bool)
            and isinstance(value, bool)
        ):
            if additive:
                result[key] |= value
            else:
                result[key] ^= value
        elif (
            key not in result.keys()
            or value is not None
        ):
            result[key] = value

    return result

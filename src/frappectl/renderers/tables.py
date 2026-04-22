def render_key_value_table(data: dict) -> str:
    if not data:
        return "(empty)"

    width = max(len(str(k)) for k in data.keys())
    lines = []
    for key, value in data.items():
        lines.append(f"{str(key).ljust(width)} : {value}")
    return "\n".join(lines)
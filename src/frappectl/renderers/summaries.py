def render_summary(title: str, items: list[str]) -> str:
    lines = [title]
    lines.extend(f"- {item}" for item in items)
    return "\n".join(lines)
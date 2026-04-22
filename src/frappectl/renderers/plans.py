def render_plan(title: str, steps: list[str]) -> str:
    lines = [title]
    for index, step in enumerate(steps, start=1):
        lines.append(f"{index}. {step}")
    return "\n".join(lines)
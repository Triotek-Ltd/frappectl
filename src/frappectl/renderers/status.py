def render_status(name: str, ok: bool, detail: str | None = None) -> str:
    state = "OK" if ok else "FAIL"
    if detail:
        return f"[{state}] {name} - {detail}"
    return f"[{state}] {name}"
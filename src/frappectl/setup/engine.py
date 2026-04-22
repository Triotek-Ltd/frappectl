from datetime import datetime, UTC

from frappectl.core import load_state, save_state
from frappectl.setup.planner import get_all_steps, get_step_by_number, get_next_incomplete_step_number


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _ensure_setup_state(state: dict) -> dict:
    if "setup" not in state:
        state["setup"] = {}
    if "steps" not in state["setup"]:
        state["setup"]["steps"] = {}
    return state


def _mark_step_running(bench_name: str, step_number: int, step_key: str, title: str):
    state = _ensure_setup_state(load_state(bench_name))
    state["setup"]["steps"][str(step_number)] = {
        "key": step_key,
        "title": title,
        "status": "running",
        "started_at": _utc_now(),
    }
    state["setup"]["last_step"] = step_number
    save_state(bench_name, state)


def _mark_step_done(bench_name: str, step_number: int, step_key: str, title: str):
    state = _ensure_setup_state(load_state(bench_name))
    existing = state["setup"]["steps"].get(str(step_number), {})
    state["setup"]["steps"][str(step_number)] = {
        "key": step_key,
        "title": title,
        "status": "done",
        "started_at": existing.get("started_at"),
        "completed_at": _utc_now(),
    }
    state["setup"]["last_step"] = step_number
    save_state(bench_name, state)


def _mark_step_failed(bench_name: str, step_number: int, step_key: str, title: str, error: str):
    state = _ensure_setup_state(load_state(bench_name))
    existing = state["setup"]["steps"].get(str(step_number), {})
    state["setup"]["steps"][str(step_number)] = {
        "key": step_key,
        "title": title,
        "status": "failed",
        "started_at": existing.get("started_at"),
        "failed_at": _utc_now(),
        "error": error,
    }
    state["setup"]["last_step"] = step_number
    save_state(bench_name, state)


def run_step(bench_name: str, step_number: int) -> None:
    step = get_step_by_number(step_number)

    _mark_step_running(bench_name, step.number, step.key, step.title)

    try:
        step.handler(bench_name)
    except Exception as exc:
        _mark_step_failed(bench_name, step.number, step.key, step.title, str(exc))
        raise

    _mark_step_done(bench_name, step.number, step.key, step.title)


def run_all(bench_name: str) -> None:
    for step in get_all_steps():
        run_step(bench_name, step.number)


def resume(bench_name: str) -> None:
    state = load_state(bench_name)
    next_step = get_next_incomplete_step_number(state)

    if next_step is None:
        return

    for step in get_all_steps():
        if step.number >= next_step:
            run_step(bench_name, step.number)


def get_status(bench_name: str) -> dict:
    state = _ensure_setup_state(load_state(bench_name))
    return state["setup"]
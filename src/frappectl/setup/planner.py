from frappectl.setup.models import SetupStep
from frappectl.setup.steps import ALL_STEPS


def get_all_steps() -> list[SetupStep]:
    return list(ALL_STEPS)


def get_step_by_number(number: int) -> SetupStep:
    for step in ALL_STEPS:
        if step.number == number:
            return step
    raise ValueError(f"Unknown setup step: {number}")


def get_next_incomplete_step_number(state: dict) -> int | None:
    steps_state = state.get("setup", {}).get("steps", {})
    for step in ALL_STEPS:
        if steps_state.get(str(step.number), {}).get("status") != "done":
            return step.number
    return None
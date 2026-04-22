from frappectl.prompts.common import ask_choice, ask_text


def ask_industry(default: str | None = None) -> str:
    industries = [
        "finance",
        "education",
        "retail",
        "healthcare",
        "utilities",
        "agriculture",
        "nonprofit",
        "hospitality",
        "property",
        "logistics",
        "manufacturing",
    ]
    return ask_choice("Select industry", industries, default=default)


def ask_app_name(default: str | None = None) -> str:
    return ask_text("App name", default=default)
from frappectl.core import load_config, save_config
from frappectl.prompts import ask_industry, ask_text


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def collect_app_selection(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    industry = existing.get("SELECTED_INDUSTRY") or ask_industry(
        default=existing.get("SELECTED_INDUSTRY")
    )

    business_modules_raw = existing.get("SELECTED_BUSINESS_MODULES")
    if business_modules_raw is None:
        business_modules_raw = ask_text(
            "Business modules (comma-separated, e.g. hr,crm,payments)",
            default=existing.get("SELECTED_BUSINESS_MODULES", ""),
        )

    modules = _parse_csv(business_modules_raw)

    return {
        "SELECTED_INDUSTRY": industry,
        "SELECTED_BUSINESS_MODULES": ",".join(modules),
    }


def save_app_selection(bench_name: str, data: dict[str, str]) -> dict[str, str]:
    existing = load_config(bench_name)
    merged = {**existing, **data}
    save_config(bench_name, merged)
    return merged
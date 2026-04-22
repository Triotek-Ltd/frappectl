from frappectl.catalog.loader import load_catalog, parse_app_list
from frappectl.catalog.models import AppSelection, AppPlan, AppDefinition


def _dedupe_apps(apps: list[AppDefinition]) -> list[AppDefinition]:
    seen: set[str] = set()
    result: list[AppDefinition] = []

    for app in apps:
        if app.name in seen:
            continue
        seen.add(app.name)
        result.append(app)

    return result


def resolve_apps(selection: AppSelection, catalog_path: str | None = None) -> AppPlan:
    catalog = load_catalog(catalog_path)

    foundation = parse_app_list(catalog.get("foundation", []))

    business_apps: list[AppDefinition] = []
    business_catalog = catalog.get("business", {})
    for module in selection.business_modules:
        business_apps.extend(parse_app_list(business_catalog.get(module, [])))

    vertical_apps: list[AppDefinition] = []
    vertical_catalog = catalog.get("verticals", {})
    if selection.industry:
        vertical_apps.extend(parse_app_list(vertical_catalog.get(selection.industry, [])))

    return AppPlan(
        foundation=_dedupe_apps(foundation),
        business=_dedupe_apps(business_apps),
        vertical=_dedupe_apps(vertical_apps),
    )


def resolve_all_apps(catalog_path: str | None = None) -> AppPlan:
    catalog = load_catalog(catalog_path)

    foundation = parse_app_list(catalog.get("foundation", []))

    business_apps: list[AppDefinition] = []
    for app_list in catalog.get("business", {}).values():
        business_apps.extend(parse_app_list(app_list))

    vertical_apps: list[AppDefinition] = []
    for app_list in catalog.get("verticals", {}).values():
        vertical_apps.extend(parse_app_list(app_list))

    return AppPlan(
        foundation=_dedupe_apps(foundation),
        business=_dedupe_apps(business_apps),
        vertical=_dedupe_apps(vertical_apps),
    )


def installable_site_apps(plan: AppPlan) -> list[AppDefinition]:
    apps = [app for app in plan.all_apps if app.name != "frappe"]

    def sort_key(app: AppDefinition) -> tuple[int, str]:
        if app.name == "erpnext":
            return (0, app.name)
        if app.category == "business":
            return (1, app.name)
        if app.category == "vertical":
            return (2, app.name)
        return (3, app.name)

    return sorted(_dedupe_apps(apps), key=sort_key)

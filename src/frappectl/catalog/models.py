from dataclasses import dataclass, field


@dataclass(frozen=True)
class AppDefinition:
    name: str
    repo: str
    branch: str | None = None
    category: str = "custom"


@dataclass(frozen=True)
class AppSelection:
    industry: str | None = None
    business_modules: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AppPlan:
    foundation: list[AppDefinition]
    business: list[AppDefinition]
    vertical: list[AppDefinition]

    @property
    def all_apps(self) -> list[AppDefinition]:
        return [*self.foundation, *self.business, *self.vertical]
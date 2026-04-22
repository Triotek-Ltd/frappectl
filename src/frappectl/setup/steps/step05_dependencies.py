from ..step_helpers import (
    ensure_step_support_directories,
    save_service_flags,
    dependency_service_targets,
    platform_supports_real_service_actions,
)


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    services = dependency_service_targets()
    flags = {
        "PYTHON_DEPENDENCIES_READY": "no",
        "MARIADB_READY": "no",
        "REDIS_READY": "no",
        "NODE_READY": "no",
        "YARN_READY": "no",
        "NGINX_READY": "no",
        "SUPERVISOR_READY": "no",
        "WKHTMLTOPDF_READY": "no",
        **services,
    }

    if platform_supports_real_service_actions():
        flags.update(
            {
                "PYTHON_DEPENDENCIES_READY": "planned",
                "MARIADB_READY": "planned",
                "REDIS_READY": "planned",
                "NODE_READY": "planned",
                "YARN_READY": "planned",
                "NGINX_READY": "planned",
                "SUPERVISOR_READY": "planned",
                "WKHTMLTOPDF_READY": "planned",
            }
        )

    merged = save_service_flags(bench_name, flags)

    print(f"[{bench_name}] step 05: dependencies complete")
    print(f"  PYTHON_DEPENDENCIES_READY={merged['PYTHON_DEPENDENCIES_READY']}")
    print(f"  MARIADB_READY={merged['MARIADB_READY']}")
    print(f"  REDIS_READY={merged['REDIS_READY']}")
    print(f"  NODE_READY={merged['NODE_READY']}")
    print(f"  YARN_READY={merged['YARN_READY']}")
    print(f"  NGINX_READY={merged['NGINX_READY']}")
    print(f"  SUPERVISOR_READY={merged['SUPERVISOR_READY']}")
    print(f"  WKHTMLTOPDF_READY={merged['WKHTMLTOPDF_READY']}")
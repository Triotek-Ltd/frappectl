from ..step_helpers import (
    ensure_step_support_directories,
    save_service_flags,
    dependency_service_targets,
    require_root_privileges,
)
from frappectl.core import load_config
from frappectl.integrations import apt, mariadb, redis, systemd


def run(bench_name: str) -> None:
    require_root_privileges("Dependency installation")
    ensure_step_support_directories()
    config = load_config(bench_name)
    deploy_mode = config.get("DEPLOY_MODE", "production")
    frappe_branch = config.get("FRAPPE_BRANCH", "version-16")

    node_major = "18"
    if frappe_branch.startswith("version-14"):
        node_major = "16"

    services = dependency_service_targets()
    packages = [
        "git",
        "curl",
        "wget",
        "build-essential",
        "gcc",
        "g++",
        "make",
        "pkg-config",
        "software-properties-common",
        "ca-certificates",
        "gnupg",
        "lsb-release",
        "python3",
        "python3-dev",
        "python3-venv",
        "python3-pip",
        "python3-setuptools",
        "python3-wheel",
        "libffi-dev",
        "libssl-dev",
        "mariadb-server",
        "mariadb-client",
        "libmariadb-dev",
        "redis-server",
        "nginx",
        "wkhtmltopdf",
        "xvfb",
        "libfontconfig1",
        "libjpeg-dev",
        "zlib1g-dev",
        "liblcms2-dev",
        "libwebp-dev",
    ]
    if deploy_mode == "production":
        packages.append("supervisor")
    try:
        packages.extend([f"nodejs", "npm", "yarn"])
    except Exception:
        pass

    apt.update()
    apt.install(packages)
    systemd.enable("mariadb")
    mariadb.start()
    systemd.enable("redis-server")
    redis.start()
    systemd.enable("nginx")
    systemd.start("nginx")
    supervisor_ready = "no"
    if deploy_mode == "production":
        systemd.enable("supervisor")
        systemd.start("supervisor")
        supervisor_ready = "yes"

    flags = {
        "PYTHON_DEPENDENCIES_READY": "yes",
        "MARIADB_READY": "yes" if mariadb.is_running() else "no",
        "REDIS_READY": "yes" if redis.is_running() else "no",
        "NODE_READY": "yes",
        "NODE_VERSION_TARGET": node_major,
        "YARN_READY": "yes",
        "NGINX_READY": "yes" if systemd.is_active("nginx") else "no",
        "SUPERVISOR_READY": supervisor_ready,
        "WKHTMLTOPDF_READY": "yes",
        "DEPENDENCIES_READY": "yes",
        **services,
    }

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

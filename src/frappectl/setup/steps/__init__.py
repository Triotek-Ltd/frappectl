from frappectl.setup.models import SetupStep

from .step01_system_prep import run as step01_run
from .step02_cleanup_layout import run as step02_run
from .step03_security import run as step03_run
from .step04_user_dev_env import run as step04_run
from .step05_dependencies import run as step05_run
from .step06_bench_init import run as step06_run
from .step07_apps_fetch import run as step07_run
from .step08_site_setup import run as step08_run
from .step09_production import run as step09_run
from .step10_https import run as step10_run
from .step11_operations import run as step11_run
from .step12_finalize import run as step12_run


ALL_STEPS: tuple[SetupStep, ...] = (
    SetupStep(1, "system_prep", "System Preparation", step01_run),
    SetupStep(2, "cleanup_layout", "System Cleanup & Layout", step02_run),
    SetupStep(3, "security", "Security Hardening", step03_run),
    SetupStep(4, "user_dev_env", "User & Development Environment Setup", step04_run),
    SetupStep(5, "dependencies", "Install Dependencies", step05_run),
    SetupStep(6, "bench_init", "Bench Initialization", step06_run),
    SetupStep(7, "apps_fetch", "Apps Fetch", step07_run),
    SetupStep(8, "site_setup", "Default Site Setup", step08_run),
    SetupStep(9, "production", "Production Setup", step09_run),
    SetupStep(10, "https", "Enable HTTPS", step10_run),
    SetupStep(11, "operations", "Bench Operations", step11_run),
    SetupStep(12, "finalize", "Finalization, Health Checks, and Backup Automation", step12_run),
)
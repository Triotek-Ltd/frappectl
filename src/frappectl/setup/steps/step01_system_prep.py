from ..step_helpers import (
    prepare_installer_directories,
    collect_bench_identity,
    derive_layout,
    assert_no_bench_conflicts,
    save_bench_identity,
)


def run(bench_name: str) -> None:
    prepare_installer_directories()

    identity = collect_bench_identity(bench_name)
    layout = derive_layout(identity)
    # Step 1 runs after the installer has already seeded bench config and after the
    # setup engine has started tracking step state, so those files are not collisions.
    assert_no_bench_conflicts(bench_name, identity, layout, include_installer_state=False)
    merged = save_bench_identity(bench_name, identity)

    print(f"[{bench_name}] step 01: system preparation complete")
    print(f"  BENCH_NAME={merged['BENCH_NAME']}")
    print(f"  BENCH_USER={merged['BENCH_USER']}")
    print(f"  DEPLOY_MODE={merged['DEPLOY_MODE']}")

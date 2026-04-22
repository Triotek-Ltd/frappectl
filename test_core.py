from frappectl.core import (
    ensure_base_dirs,
    register_bench,
    list_benches,
    set_active_bench,
    resolve_bench,
    load_config,
    save_config,
    load_state,
    save_state,
)

ensure_base_dirs()

register_bench("testbench", {
    "path": "/home/testbench",
    "user": "test",
    "mode": "dev"
})

print("BENCHES:", list_benches())

set_active_bench("testbench")
print("ACTIVE:", resolve_bench(None))

save_config("testbench", {"KEY": "VALUE"})
print("CONFIG:", load_config("testbench"))

save_state("testbench", {"step": 1})
print("STATE:", load_state("testbench"))
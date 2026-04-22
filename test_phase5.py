from frappectl.validators import (
    is_valid_bench_name,
    is_valid_username,
    is_valid_site_name,
    can_resolve_host,
    path_exists,
    has_required_keys,
)
from frappectl.renderers import (
    render_key_value_table,
    render_summary,
    render_status,
    render_plan,
)

print(is_valid_bench_name("client-a-bench"))
print(is_valid_username("frappe"))
print(is_valid_site_name("erp.example.com"))
print(can_resolve_host("localhost"))
print(path_exists("."))

print(render_key_value_table({"bench": "testbench", "mode": "dev"}))
print(render_summary("Apps", ["frappe", "erpnext"]))
print(render_status("registry", True, "loaded"))
print(render_plan("Setup Plan", ["Step 1", "Step 2"]))

print(has_required_keys({"A": 1, "B": 2}, ["A", "B"]))
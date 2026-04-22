from frappectl.integrations import run

result = run(["python", "--version"], check=True)
print("RETURNCODE:", result.returncode)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
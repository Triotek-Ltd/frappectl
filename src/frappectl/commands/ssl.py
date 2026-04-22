import typer

from frappectl.core import resolve_bench, load_config
from frappectl.services import prepare_https

app = typer.Typer()


@app.command("prepare")
def prepare_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = prepare_https(bench_name)

    typer.echo(f"HTTPS prepared for: {bench_name}")
    typer.echo(f"  SSL_ENABLED={config.get('SSL_ENABLED', '')}")
    typer.echo(f"  SSL_CERT_INSTALLED={config.get('SSL_CERT_INSTALLED', '')}")
    typer.echo(f"  HTTPS_REDIRECT_ENABLED={config.get('HTTPS_REDIRECT_ENABLED', '')}")
    typer.echo(f"  SSL_RENEWAL_ENABLED={config.get('SSL_RENEWAL_ENABLED', '')}")


@app.command("status")
def status_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)

    typer.echo(f"HTTPS status for: {bench_name}")
    typer.echo(f"  SSL_EMAIL={config.get('SSL_EMAIL', '')}")
    typer.echo(f"  DNS_READY={config.get('DNS_READY', '')}")
    typer.echo(f"  SSL_ENABLED={config.get('SSL_ENABLED', 'unknown')}")
    typer.echo(f"  SSL_CERT_INSTALLED={config.get('SSL_CERT_INSTALLED', 'unknown')}")
    typer.echo(f"  HTTPS_REDIRECT_ENABLED={config.get('HTTPS_REDIRECT_ENABLED', 'unknown')}")
    typer.echo(f"  SSL_RENEWAL_ENABLED={config.get('SSL_RENEWAL_ENABLED', 'unknown')}")
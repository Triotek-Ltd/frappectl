import socket


def can_resolve_host(host: str) -> bool:
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False
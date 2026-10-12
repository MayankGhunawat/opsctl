import socket
import time
import urllib.parse


def check_dns(hostname: str) -> dict:
    """Concepts: DNS Resolution & IP Mapping"""
    start = time.perf_counter()
    try:
        ip = socket.gethostbyname(hostname)
        latency = (time.perf_counter() - start) * 1000
        return {
            "target": hostname,
            "type": "DNS",
            "status": "UP",
            "detail": f"IP: {ip}",
            "latency": f"{latency:.1f}ms",
        }
    except socket.gaierror as e:
        return {
            "target": hostname,
            "type": "DNS",
            "status": "DOWN",
            "detail": f"DNS failure ({e})",
            "latency": "N/A",
        }


def check_port(host: str, port: int, timeout: float = 2.0) -> dict:
    """Concepts: TCP Handshake, Ports & Timeouts (Cross-platform for Windows/Linux)"""
    start = time.perf_counter()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            # Using connect() with try/except prevents Windows WSAEWOULDBLOCK (10035) bugs
            s.connect((host, port))
            latency = (time.perf_counter() - start) * 1000
            return {
                "target": f"{host}:{port}",
                "type": "TCP",
                "status": "UP",
                "detail": "Port Open",
                "latency": f"{latency:.1f}ms",
            }
        except socket.timeout:
            return {
                "target": f"{host}:{port}",
                "type": "TCP",
                "status": "DOWN",
                "detail": f"Timed out ({timeout}s)",
                "latency": "N/A",
            }
        except ConnectionRefusedError:
            return {
                "target": f"{host}:{port}",
                "type": "TCP",
                "status": "DOWN",
                "detail": "Connection Refused (Service Down)",
                "latency": "N/A",
            }
        except Exception as e:
            return {
                "target": f"{host}:{port}",
                "type": "TCP",
                "status": "DOWN",
                "detail": str(e),
                "latency": "N/A",
            }


def check_http(url: str, timeout: float = 3.0) -> dict:
    """Concepts: HTTP Protocol on top of Raw TCP Sockets"""
    parsed = urllib.parse.urlparse(url if url.startswith("http") else f"http://{url}")
    host = parsed.hostname or url
    port = parsed.port or 80
    path = parsed.path or "/"

    start = time.perf_counter()
    try:
        # 1. Resolve DNS
        ip = socket.gethostbyname(host)

        # 2. Establish TCP Connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))

            # 3. Send raw HTTP/1.1 request bytes
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode("utf-8"))

            # 4. Read raw response bytes
            response = s.recv(512).decode("utf-8", errors="ignore")
            status_line = response.split("\r\n")[0] if response else "NO RESPONSE"
            latency = (time.perf_counter() - start) * 1000

            is_up = any(code in status_line for code in ["200", "301", "302"])
            return {
                "target": url,
                "type": "HTTP",
                "status": "UP" if is_up else "DOWN",
                "detail": status_line,
                "latency": f"{latency:.1f}ms",
            }

    except socket.timeout:
        return {
            "target": url,
            "type": "HTTP",
            "status": "DOWN",
            "detail": f"Timed out ({timeout}s)",
            "latency": "N/A",
        }
    except ConnectionRefusedError:
        return {
            "target": url,
            "type": "HTTP",
            "status": "DOWN",
            "detail": "Connection Refused",
            "latency": "N/A",
        }
    except Exception as e:
        return {
            "target": url,
            "type": "HTTP",
            "status": "DOWN",
            "detail": str(e),
            "latency": "N/A",
        }


def run_health_checks(custom_target: str = None):
    """Runs default suite or checks a specific user-supplied target."""
    if custom_target:
        checks = [
            check_dns(custom_target),
            check_port(custom_target, 80),
            check_http(f"http://{custom_target}/"),
        ]
    else:
        # Default test target suite for learning on your laptop
        checks = [
            check_dns("google.com"),
            check_port("127.0.0.1", 8080),
            check_port("8.8.8.8", 53),
            check_http("http://example.com/"),
            check_http("http://127.0.0.1:9999/"),
        ]

    print(f"\n{'TYPE':<6} {'TARGET':<25} {'STATUS':<8} {'LATENCY':<10} {'DETAILS'}")
    print("-" * 75)

    for res in checks:
        status_fmt = f"[ {res['status']} ]"
        print(
            f"{res['type']:<6} {res['target']:<25} {status_fmt:<8} {res['latency']:<10} {res['detail']}"
        )
    print()
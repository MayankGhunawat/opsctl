import shutil


def get_disk_info(path="/"):
    """Return disk usage information for a filesystem path."""

    usage = shutil.disk_usage(path)

    return {
        "path": path,
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "percent_used": round((usage.used / usage.total) * 100, 2),
    }


def print_disk_info(path="/"):
    """Print disk usage information."""

    info = get_disk_info(path)

    print("Disk Information")
    print("----------------")
    print(f"Path: {info['path']}")
    print(f"Total: {info['total']:,} bytes")
    print(f"Used: {info['used']:,} bytes")
    print(f"Free: {info['free']:,} bytes")
    print(f"Used: {info['percent_used']}%")


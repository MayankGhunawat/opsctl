import os
import platform
import socket
import sys


def get_system_info():
    """Collect basic information about the local system."""

    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "hostname": socket.gethostname(),
        "architecture": platform.machine(),
        "cpu_cores": os.cpu_count(),
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
    }



def print_system_info():
    """Print system information in a human-readable format."""

    info = get_system_info()

    print("System Information")
    print("------------------")
    print(f"OS: {info['os']} {info['os_release']}")
    print(f"Hostname: {info['hostname']}")
    print(f"Architecture: {info['architecture']}")
    print(f"CPU cores: {info['cpu_cores']}")
    print(f"Python version: {info['python_version']}")
    print(f"Python executable: {info['python_executable']}")

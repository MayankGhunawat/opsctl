import sys

try:
    import psutil
except ImportError:
    print(
        "Error: The 'psutil' library is required.",
        file=sys.stderr
    )
    print(
        "Install it with: pip install psutil",
        file=sys.stderr
    )
    sys.exit(1)

def get_running_processes(sort_by="cpu"):

    processes = list(psutil.process_iter(["name", "pid"]))

    # Fetch running processes and return their CPU and memory usage.

    for proc in processes:
        try:
            proc.cpu_percent()
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Give psutil some time to measure CPU usage.
    import time
    time.sleep(1)

    process_list = []

    for proc in processes:
        try:
            name = proc.name() or "Unknown"

            process_list.append({
                "pid" : proc.pid ,
                "name" : name ,
                "cpu_percent" : proc.cpu_percent(None) ,
                "memory_percent" : proc.memory_percent()
            })

        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if sort_by == "cpu":
        process_list.sort(key=lambda x: x["cpu_percent"], reverse=True)

    elif sort_by == "memory":
        process_list.sort(key=lambda x : x["memory_percent"], reverse=True)

    elif sort_by == "pid":
        process_list.sort(key=lambda x: x["pid"])

    return process_list

def display_processes(processes, limit=10):
    # Display the most relevant processes in a clean table.

    print(f"Running processes: {len(processes)}")
    print()

    header = (
        f"{'PID':<8}"
        f"{'NAME':<28}"
        f"{'CPU %':>8}"
        f"{'MEM %':>8}"
    )

    print(header)
    print("─" * len(header))

    for proc in processes[:limit]:
        name = proc["name"][:27]

        print(
            f"{proc['pid']:<8}"
            f"{name:<28}"
            f"{proc['cpu_percent']:>7.1f}%"
            f"{proc['memory_percent']:>7.1f}%"
        )


if __name__ == "__main__":
    try:
        running_processes = get_running_processes(sort_by="cpu")

        display_processes(running_processes, limit=10)

    except KeyboardInterrupt:
        print("\nProcess inspection cancelled.")
        sys.exit(0)

import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m opsctl <command>")
        print("Commands: system, disk, process, health, logs, deploy")
        sys.exit(1)

    command = sys.argv[1]

    if command == "system":
        from . import system
        system.print_system_info()

    elif command == "disk":
        from . import disk
        disk.print_disk_info()

    elif command == "process":
        from . import process
        process.print_process_info()

    elif command == "health":
        from . import health
        
        # Optional: accept a custom host/target if provided as 3rd arg
        # e.g., python -m opsctl health google.com
        target = sys.argv[2] if len(sys.argv) > 2 else None
        health.run_health_checks(target)
    
        

    elif command == "deploy":
        print("Deploying...")

    elif command == "logs":
        if len(sys.argv) < 3:
            print("Usage: python -m opsctl logs <log_file> [--errors]")
            sys.exit(1)

        from . import logs

        file_path = sys.argv[2]

        result = logs.analyze_log(file_path)

        if result is None:
            sys.exit(1)

        counts, error_messages = result

        if "--errors" in sys.argv:
            logs.print_errors(error_messages)
        else:
            logs.print_log_summary(counts)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
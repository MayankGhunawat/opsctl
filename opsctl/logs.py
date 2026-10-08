from collections import Counter
import re

LOG_LEVELS  = ["INFO", "WARNING", "ERROR"]

def analyze_log(file_path):
    counts = {
        "INFO": 0,
        "WARNING" : 0,
        "ERROR" : 0
    }

    try:
        error_messages = Counter()

        with open(file_path, "r") as file:
            for line in file:
                for level in LOG_LEVELS:
                    if level in line:
                        counts[level] += 1

                        if level == "ERROR":
                            message = extract_error_messages(line)
                            if message:
                                error_messages[message] += 1

                        break

    except FileExistsError:
        print(f"Log file not found: {file_path}")
        return None

    return counts, error_messages


def extract_error_messages(line):
    match = re.search(r"ERROR\s(.*)", line)

    if match:
        return match.group(1).strip()
   
    return None


def print_log_summary(counts):
    print("Log Summary")
    print("────────────────────────")
    print(f"INFO       {counts['INFO']:>5}")
    print(f"WARNING    {counts['WARNING']:>5}")
    print(f"ERROR      {counts['ERROR']:>5}")


def print_errors(error_messages):
    print("Top Errors")
    print("────────────────────────")

    for message, count in error_messages.most_common():
        print(f"{message:<25} {count:>3}")
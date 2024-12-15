#!/usr/bin/env python3
import os
import sys
import random
import time


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <sleep_time>", file=sys.stderr)
        sys.exit(1)

    try:
        sleep_time = int(sys.argv[1])
        if sleep_time <= 0:
            raise ValueError()
    except ValueError:
        print("sleep_time must be a positive integer", file=sys.stderr)
        sys.exit(1)

    pid = os.getpid()
    ppid = os.getppid()

    print(f"Minion[{pid}]: created. Parent PID {ppid}.")

    time.sleep(sleep_time)

    exit_status = random.choice([0, 1])

    print(f"Child[{pid}]: before terminated. Parent PID {ppid}. Exit status {exit_status}.")
    sys.exit(exit_status)


if __name__ == "__main__":
    main()

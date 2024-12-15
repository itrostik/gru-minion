#!/usr/bin/env python3
import os
import sys
import random
import time


def start_child():
    sleep_time = random.randint(5, 10)

    pid = os.fork()
    if pid == 0:
        try:
            args = ["./minion.py", str(sleep_time)]
            os.execve("/usr/bin/python3", ["/usr/bin/python3"] + args, os.environ)
        except Exception as e:
            print(f"Minion execve failed: {e}", file=sys.stderr)
            os._exit(1)
    return pid


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <N>")
        sys.exit(1)

    try:
        N = int(sys.argv[1])
        if N <= 0:
            raise ValueError()
    except ValueError:
        print("N must be a positive integer")
        sys.exit(1)

    random.seed(time.time())

    pid = os.getpid()
    children = []

    for _ in range(N):
        child_pid = start_child()
        print(f"Gru[{pid}]: process created. PID {child_pid}.")
        children.append(child_pid)

    for i, child_pid in enumerate(children):
        while True:
            try:
                pid, status = os.waitpid(child_pid, 0)
                exit_status = os.WEXITSTATUS(status)
                print(f"Gru[{os.getpid()}]: process terminated. PID {pid}. Exit status {exit_status}.")

                if exit_status == 0:
                    break
                else:
                    print(f"Gru[{os.getpid()}]: restarting process for PID {child_pid}.")
                    child_pid = start_child()
            except Exception as e:
                print(f"Error waiting for child process: {e}", file=sys.stderr)
                break

    sys.exit(0)


if __name__ == "__main__":
    main()

import subprocess
import csv
import os
import sys
import select
from datetime import datetime

INTERFACE = "eth0"
OUTPUT_FILE = "data/captured.csv"

cmd = [
    "tshark", "-i", INTERFACE,
    "-Y", "ssl.handshake.extensions_server_name",
    "-T", "fields",
    "-e", "ip.src",
    "-e", "ssl.handshake.extensions_server_name",
    "-e", "frame.time"
]

def start_capture(duration_seconds=None):
    print(f"Capturing on {INTERFACE}...")

    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Source IP", "Domain", "Timestamp"])

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )

        try:
            start_time = datetime.now()

            while True:
                if duration_seconds and (datetime.now() - start_time).total_seconds() > duration_seconds:
                    print(f"\nCapture time limit reached ({duration_seconds} seconds). \nStopping capture...")
                    break

                ready, _, _ = select.select([proc.stdout], [], [], 1.0)
                if ready:
                    line = proc.stdout.readline()
                    if not line:
                        break

                    parts = line.strip().split('\t')
                    if len(parts) == 3:
                        src_ip, domain, timestamp_str = parts
                        writer.writerow([src_ip, domain, timestamp_str])
                        file.flush()
                        print(f"{src_ip} -> {domain} at {timestamp_str}")

        except KeyboardInterrupt:
            print("\nCapture stopped by user.")
        finally:
            proc.terminate()

def main():
    if os.geteuid() != 0:
        print("Run this script with sudo.")
        sys.exit(1)

    try:
        duration = int(input("Enter capture duration in seconds (preferably 300 atleast): "))
        duration = None if duration == 0 else duration
    except ValueError:
        duration = None

    start_capture(duration_seconds=duration)

if __name__ == "__main__":
    main()

def run():
    main()
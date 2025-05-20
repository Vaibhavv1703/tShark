import subprocess
import csv
import os
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
            for line in iter(proc.stdout.readline, ''):
                if duration_seconds and (datetime.now() - start_time).total_seconds() > duration_seconds:
                    print(f"\nCapture time limit reached ({duration_seconds} seconds). Stopping capture.")
                    break

                parts = line.strip().split('\t')
                if len(parts) == 3:
                    src_ip, domain, timestamp_str = parts

                    try:
                        dt = datetime.strptime(timestamp_str.split(" IST")[0], "%b %d, %Y %H:%M:%S.%f")
                    except ValueError:
                        dt = datetime.strptime(timestamp_str.split(" IST")[0], "%b %d, %Y %H:%M:%S")
                    time_formatted = dt.strftime("%H:%M")

                    writer.writerow([src_ip, domain, time_formatted])
                    file.flush()
                    print(f"{src_ip} -> {domain} at {time_formatted}")

        except KeyboardInterrupt:
            print("\nCapture stopped by user.")

        finally:
            proc.terminate()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Run this script with sudo.")
    else:
        try:
            duration = int(input("Enter capture duration in seconds (0 for unlimited): "))
            duration = None if duration == 0 else duration
        except ValueError:
            duration = None

        start_capture(duration_seconds=duration)

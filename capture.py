import subprocess
import csv
import os

INTERFACE = "eth0"
OUTPUT_FILE = "captured.csv"

cmd = [
    "tshark", "-i", INTERFACE,
    "-Y", "ssl.handshake.extensions_server_name",
    "-T", "fields",
    "-e", "ip.src",
    "-e", "ip.dst",
    "-e", "ssl.handshake.extensions_server_name",
    "-e", "frame.time"
]

def start_capture():
    print(f"[+] Capturing on {INTERFACE}...")
    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Source IP", "Destination IP", "Domain", "Timestamp"])

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )

        try:
            for line in iter(proc.stdout.readline, ''):
                parts = line.strip().split('\t')
                if len(parts) == 4:
                    writer.writerow(parts)
                    file.flush()
                    print(f"[+] {parts[0]} -> {parts[2]} at {parts[3]}")
        except KeyboardInterrupt:
            proc.terminate()
            print("\n[!] Capture stopped.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] Run this script with sudo.")
    else:
        start_capture()

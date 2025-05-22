# tShark
An automated script for tShark that scans, analyze and categorize domains by using tShark. Designed for cybersecurity insights, domain monitoring, and traffic classification.

---

## Overview
tShark captures SSL handshake traffic, extracts domain names, categorizes them by type (e.g., social media, search engines, ads), cleans the data, and displays it in a user-friendly table — all from your terminal.

## Features
- **Packet Capture**: Captures traffic using tshark via SSL handshake extension; Extracts IP, Domain, and precise Timestamps.
- **Domain Categorization**: Matches domain using a simple rule-based classification; more categories can be easily added by tweaking the files a bit.
- **Data Cleaning & Merging**: Merges repetitive visits within a 3-second window; Filters out ad/tracking categories.
- **Visualization**: Displays the cleaned data in a beautifully formatted terminal table using `tabulate`.

## Requirements
- Python 3.x
- `tshark` installed and accessible in PATH
- Root privileges (for packet capture)

## Usage
1. **Clone the repository:**
    ```bash
    git clone https://github.com/Vaibhavv1703/tShark.git
    ```
2. **Navigate to the working directory:**
    ```bash
    cd tShark
    ```
3. **Run the application:**
    ```bash
    sudo py main.py
    ```

## Project Structure
- [`main.py`](main.py): Main menu and entry point.
- [`capture.py`](capture.py): Uses tshark to capture packets.
- [`scrape.py`](scrape.py): Visits the domains captured and scrapes of details.
- [`categorize.py`](categorize.py): Categorizes the domain using a simple rule-based classification which can be easily edited.
- [`clean.py`](clean.py): Removes useless details as well as ads/tracking websites.
- [`tab.py`](tab.py): Visualizes the final data into a readable table.

## Notes
- Currently works only on Linux. Adaptation for Windows/Mac is possible with tweaks.
- Currently scans traffic only for the host device.
- You must run `main.py` with sudo for `tshark` to capture packets.

## Future Scope
- Multi-device scanning over a network
- Browser extension integration
- Machine learning for category prediction
- Support for more protocols (HTTP, DNS, etc.)

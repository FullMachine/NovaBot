import os

REPORT_FILE = 'nba_health_report.txt'

def delete_broken_files():
    if not os.path.exists(REPORT_FILE):
        print(f"Report file {REPORT_FILE} not found.")
        return
    deleted = 0
    with open(REPORT_FILE) as f:
        for line in f:
            if 'BROKEN:' in line:
                fpath = line.split('BROKEN:')[1].strip()
                if os.path.exists(fpath):
                    os.remove(fpath)
                    print(f"Deleted: {fpath}")
                    deleted += 1
    print(f"\nTotal broken files deleted: {deleted}")

if __name__ == "__main__":
    delete_broken_files() 
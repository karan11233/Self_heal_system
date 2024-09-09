import os
import shutil
import logging
import psutil  # Requires installation: pip install psutil

# Set up logging
LOG_DIR = "MaliciousFilesLog"
os.makedirs(LOG_DIR, exist_ok=True)

# File extensions considered malicious (modify this as needed)
MALICIOUS_EXTENSIONS = ['.exe', '.bat', '.cmd', '.vbs', '.js', '.scr', '.pif', '.com']

def is_malicious_file(file_path):
    """Check if the file is malicious based on its extension."""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in MALICIOUS_EXTENSIONS

def scan_directory(directory):
    """Scan a directory for malicious files."""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_malicious_file(file_path):
                store_malicious_file(file_path)

def store_malicious_file(file_path):
    """Store the malicious file in the log directory."""
    try:
        shutil.copy(file_path, LOG_DIR)
    except Exception as e:
        logging.error(f"Failed to copy {file_path}: {e}")

def display_storage_info():
    """Display storage devices and their available space."""
    print("Storage Devices and Available Space:")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"Device: {partition.device} - Total Size: {usage.total // (1024**3)} GB, "
              f"Used: {usage.used // (1024**3)} GB, Free: {usage.free // (1024**3)} GB")

def main():
    # Setup logging
    logging.basicConfig(filename='malicious_file_scan.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Display storage information
    display_storage_info()

    # Scan each partition
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"Scanning device {partition.device}...")
        scan_directory(partition.mountpoint)
        print("Device is under scanning...")

if __name__ == "__main__":
    main()

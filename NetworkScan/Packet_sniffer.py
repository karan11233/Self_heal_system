import os
import logging
from scapy.all import sniff, IP, TCP, UDP
import datetime

# Directories for logs
LOG_DIR = "NetworkLogFile"
MALICIOUS_LOG_DIR = "MaliciousLogFile"

# Ensure the directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MALICIOUS_LOG_DIR, exist_ok=True)

# File paths for logs
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(LOG_DIR, f"network_log_{timestamp}.log")
malicious_log_file = os.path.join(MALICIOUS_LOG_DIR, f"malicious_log_{timestamp}.log")

# Set up logging for general packet logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Set up logging for malicious packets
malicious_logger = logging.getLogger('malicious')
malicious_handler = logging.FileHandler(malicious_log_file)
malicious_handler.setLevel(logging.WARNING)  # Set level to WARNING for malicious log
malicious_logger.addHandler(malicious_handler)

# Example criteria for detecting malicious activity
SUSPICIOUS_IPS = {"192.168.1.100"}  # Example suspicious IPs
SUSPICIOUS_KEYWORDS = [b'attack', b'virus', b'exploit']  # Example suspicious content keywords

def is_packet_malicious(packet):
    """Check if the packet matches malicious criteria."""
    # Check for suspicious IP addresses
    if IP in packet:
        if packet[IP].src in SUSPICIOUS_IPS or packet[IP].dst in SUSPICIOUS_IPS:
            return True

    # Check for suspicious payload content
    if TCP in packet or UDP in packet:
        payload = bytes(packet[TCP].payload) if TCP in packet else bytes(packet[UDP].payload)
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in payload:
                return True

    return False

def packet_callback(packet):
    """Process each captured packet."""
    # Log every packet
    logging.info(f"Packet: {packet.summary()}")

    # Check if the packet is malicious
    if is_packet_malicious(packet):
        malicious_logger.warning(f"Malicious Packet: {packet.summary()}")

# Start sniffing packets
def start_packet_sniffing():
    print("Starting packet sniffing...")
    sniff(prn=packet_callback, store=0)  # prn specifies the callback function to handle each packet

if __name__ == "__main__":
    start_packet_sniffing()

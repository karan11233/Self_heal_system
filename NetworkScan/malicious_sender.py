from scapy.all import Ether, IP, TCP, sendp
import time

def send_malicious_packets():
    # Define the malicious packet
    # Adjust the target MAC and IP as needed for your environment
    target_ip = "192.168.1.100"  # Replace with a valid target IP in your network
    malicious_payloads = [
        b'attack',
        b'virus',
        b'exploit',
        b'GET /malicious HTTP/1.1\r\nHost: evil.com\r\n\r\n'  # Example of HTTP request payload
    ]

    for payload in malicious_payloads:
        # Create Ethernet frame
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
        ip = IP(src="192.168.1.200", dst=target_ip)  # Replace with your source IP
        tcp = TCP(sport=12345, dport=80)  # Example source and destination ports

        # Create the packet with the malicious payload
        packet = ether / ip / tcp / payload

        # Send the packet
        sendp(packet, iface="Wi-Fi")  # Replace 'YOUR_INTERFACE' with your network interface
        print(f"Sent malicious packet with payload: {payload}")
        time.sleep(1)  # Sleep for a second before sending the next packet

if __name__ == "__main__":
    send_malicious_packets()

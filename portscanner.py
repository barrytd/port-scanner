import pyfiglet
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

ascii_banner = pyfiglet.figlet_format("Port Scanner")
print(ascii_banner)


def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)  # Adjust the timeout as needed
    result = sock.connect_ex((target, port))
    sock.close()
    return port if result == 0 else None


def scan_ports(target, start_port, end_port, max_workers=50):  # Adjust the max workers as needed
    print(f"Scanning target {target} for open ports...\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(start_port, end_port + 1)]

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                open_ports.append(result)

    print("Scan complete. Open ports:", open_ports)


if __name__ == "__main__":
    target_host = input("Enter the target host: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    scan_ports(target_host, start_port, end_port)



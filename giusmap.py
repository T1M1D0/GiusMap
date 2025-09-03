import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_IP_WORKERS = 200
MAX_PORT_WORKERS = 1000

#def singlePort():
#    selectedPort = int(input("which port would you like closed?"))
    

#def closePort():
#    print("placeholder")


def id_subnet():
    local_host = socket.gethostname()
    host_ip = socket.gethostbyname(local_host)
    ip_raw = host_ip.split('.')
    if len(ip_raw) != 4 or (ip_raw[0] not in ['10', '172', '192'] and ip_raw[0] != '127'):
        print("Somethings wrong with your ip dawg")
        return
    print(f"Scanning subnet, {ip_raw[0]}.{ip_raw[1]}.0.0")
    with ThreadPoolExecutor(max_workers=MAX_IP_WORKERS) as ip_executor:    
        for s in range(256):
            for f in range(256):
                target_ip = f"{ip_raw[0]}.{ip_raw[1]}.{s}.{f}"
                ip_executor.submit(scan_host, target_ip)
                
def scan_host(host):
    with ThreadPoolExecutor(max_workers=MAX_PORT_WORKERS) as port_executor:
        future_to_port = {
            port_executor.submit(scan_port, host, port): port
            for port in range(1, 65536)
        }
        for future in as_complete(future_to_port):
            pass

def scan_port(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        try:
            s.connect((host, port))
            print(f"{host}:{port} is open")
            return True
        except (socket.timeout, ConnectionRefusedError):
            pass
        finally:
            s.close()

#def funcSel(sel):
#    if sel == 2:
#        ip_split()
#    if sel == 1:
#        print("Placeholder")


def main():
    id_subnet()

if __name__ == "__main__":
    main()
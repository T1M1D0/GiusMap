import socket

def singlePort():
    selectedPort = int(input("which port would you like closed?"))
    

def closePort():
    print("placeholder")


def ip_split():
    local_host = socket.gethostname()
    host_ip = socket.gethostbyname(local_host)
    ip_raw = host_ip.split('.')
    s = 0
    while s != 255:
        for f in range(255):
            if f == 255:
                f = 0
                s =+ 1
            f+=1
            subnet_raw = ip_raw[0], ip_raw[1], str(s), str(f)
            subnet = ".".join(subnet_raw)
            print(subnet)

def id_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    target_host = socket.gethostname()

    s.bind((socket.gethostname(), port_sel))
    s.listen(5)

def funcSel(sel):
    if sel == 2:
        ip_split()
    if sel == 1:
        print("Placeholder")


def main():
    #welcome_msg = print("Hello, Welcome to GiusMap! Select whatever you want and have fun but not too much fun ;)")
    #sel = input("1) Scan whole network on specific port\n2) Scan whole network on all ports (why would you do this(RECOURSE INTENSIVE!!!))\n3)")
    #funcSel(sel)
    #id_port()
    ip_split()

if __name__ == "__main__":
    main()
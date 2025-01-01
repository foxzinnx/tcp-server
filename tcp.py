from colorama import Fore, Style, init
import socket
import argparse

init(autoreset= True)

def main_menu():
    banner = f"""{Fore.YELLOW}
 _____ ____ ____    ____  _____ ______     _______ ____  
|_   _/ ___|  _ \  / ___|| ____|  _ \ \   / / ____|  _ \ 
  | || |   | |_) | \___ \|  _| | |_) \ \ / /|  _| | |_) |
  | || |___|  __/   ___) | |___|  _ < \ V / | |___|  _ < 
  |_| \____|_|     |____/|_____|_| \_\ \_/  |_____|_| \_\\
                                                        
                 {Fore.CYAN}github.com/foxzinnx                                      
                                                        """
    print(banner)

def start_server(ip, port):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind((ip, port))
    tcp.listen()
    print(f"Listening {ip} {port}")
    return tcp

def accept_connection(tcp):
    con, client = tcp.accept()
    print(f"{Fore.YELLOW}{client[0]} {Fore.GREEN}connected")
    return con, client

def authentication(con, client, max_attempts):
    attempts = 0
    while attempts < max_attempts:
        con.sendall("Username: ".encode())
        user = con.recv(1024).decode().strip()
        con.sendall("Password: ".encode())
        password = con.recv(1024).decode().strip()

        if user == "admin" and password == "administrator":
            con.sendall(f"Logged in, Welcome back {user}\n".encode())
            print(f"{Fore.GREEN}User: {Fore.YELLOW}{client[0]} {Fore.GREEN}logged in successfully.")
            return True
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                con.sendall("Incorrect credentials, Please try again.\n".encode())
            else:
                con.sendall("Attempts exhausted. Connection closed.".encode())
                print(f"User: {client[0]} failed all attempts.")
                return False
            
def interactive_loop(con):
    while True:
        msg = input("> ")
        msg += "\n"
        con.sendall(msg.encode())
        data = con.recv(1024).decode()
        print(data)

def main():
    main_menu()
    ip = "0.0.0.0"
    max_attempts = 3
    parser = argparse.ArgumentParser(description=f"{Fore.YELLOW}Simple python TCP Server")
    parser.add_argument("-p", "--port", required=True, help=f"{Style.BRIGHT}Port number")

    args = parser.parse_args()
    port = int(args.port)

    tcp = start_server(ip, port)
    con, client = accept_connection(tcp)

    con.sendall("Welcome to TCP server\n".encode())

    if authentication(con, client, max_attempts):
        interactive_loop(con)

    tcp.close()

if __name__ == "__main__":
    main()
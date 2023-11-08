import socket
import time

# Adresse IP et port du serveur
server_address = ('172.18.10.51', 666)

def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    return client_socket

def display_menu():
    print("Menu:")
    print("1) CPU (Dispo/Total)")
    print("2) RAM (Dispo/Total)")
    print("3) Interface réseau (Actives, IP dessus, vitesse)")
    print("4) Info système d'exploitation (Quel OS et quelle version)")
    print("5) Temps d'activité de l'OS")
    print("6) Disque")
    print("7) Quitter le script")

def send_choice(client_socket, choice):
    if choice == '7':
        return True
    elif choice in ['1', '2', '3', '4', '5']:
        client_socket.sendall(choice.encode())
    elif choice == '6':
        sub_choice = input("Sous-menu Disque:\n1) Listing des volumes (Disque physique et partitions)\n2) Utilisation des disques/Capacité de stockage restante\nChoisissez une option : ")
        if sub_choice in ['1', '2']:
            client_socket.sendall(f'6{sub_choice}'.encode())
        else:
            print("Option invalide.")
    else:
        print("Option invalide. Choisissez à nouveau.")
    return False

def receive_response(client_socket):
    response = client_socket.recv(1024)
    print("Réponse du serveur :")
    print(response.decode('utf-8'))

def main():
    while True:
        client_socket = connect_to_server(server_address)
        try:
            display_menu()
            choice = input("Choisissez une option : ")
            exit_requested = send_choice(client_socket, choice)
            if exit_requested:
                break
            receive_response(client_socket)
        except KeyboardInterrupt:
            print("Client arrêté.")
        finally:
            client_socket.close()
        time.sleep(1)

if __name__ == "__main__":
    main()

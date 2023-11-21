#-----Modules utilisés-----#
import socket # Pour la création de socket
import time #  Utilise pour le timesleep

#-----Demande IP et Port Server-----#
def get_server_address():
    server_ip = input("Entrez l'adresse IP du serveur : ")
    server_port = int(input("Entrez le port du serveur : "))
    return (server_ip, server_port)

#-----Initialisation de la connexion au serveur-----#
def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    return client_socket

#-----Affichage du menu-----#
def display_menu():
    print("Menu:")
    print("1) CPU (Dispo/Total)")
    print("2) RAM (Dispo/Total)")
    print("3) Interface réseau (Actives, IP/Masque)")
    print("Info système d'exploitation (Quel OS / version)")
    print("5) Temps d'activité de l'OS")
    print("6) Afficher le cache ARP")
    print("7) Disque")
    print("8) Quitter le script")

#-----Fonction de choix des options du menu-----#
def send_choice(client_socket, choice):
    if choice == '8':
        return True
    elif choice in ['1', '2', '3', '4', '5', '6']:
        client_socket.sendall(choice.encode())
    elif choice == '7':
        sub_choice = input("Sous-menu Disque:\n1) Listing des volumes (Disque physique et partitions)\n2) Utilisation des disques/Capacité de stockage restante\nChoisissez une option : ")
        if sub_choice in ['1', '2']:
            client_socket.sendall(f'6{sub_choice}'.encode())
        else:
            print("Option invalide.")
    else:
        print("Option invalide. Choisissez à nouveau.")
    return False

#-----Reception des réponses du serveur-----#
def receive_response(client_socket):
    response = client_socket.recv(1024)
    print("Réponse du serveur :")
    print(response.decode('utf-8'))

#-----Fonction principal (Connexion, affichage menu, choix des options, attente réponse, et fin du programme)-----#
def main():
    server_address = get_server_address()  # Appel de la fonction pour obtenir l'adresse IP et le port
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

#-----Lancement de la fonction main appelant le reste du script-----#
main()
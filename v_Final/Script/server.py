#-----Modules utilisés-----#
import socket # Pour la création de socket
import threading #  Pour la création de thread
import psutil # Utilise sur option 1,2,4,6.1,6.2
import netifaces as ni # Utilise sur option 3, renommé "ni"
import platform # Utilise sur option 4
import time #  Utilise sur option 5

#-----Partie serveur-----#
# Adresse IP & Port du serveur
server_ip = input("Entrez l'ip du serveur : ")
server_port = int(input("Entrez le port d'écoute du serveur : "))

# Créer un socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

# Écouter les connexions entrantes
server_socket.listen(1)
print(f"Serveur en attente de connexions sur le port {server_port}...")

#-----Partie Option-----#
def option_1(client_socket):
    # Option 1 : Info CPU
    cpu_info = psutil.cpu_percent(interval=1, percpu=True)
    
    # Mise en forme de la réponse
    response = "Informations sur le CPU :\n"
    for i, cpu in enumerate(cpu_info):
        response += f"CPU {i}: {cpu}%\n"
    response = response.encode('utf-8')

    # Envoyer de la réponse au client
    client_socket.send(response)
    client_socket.close()

def option_2(client_socket):
    # Option 2 : Info RAM
    ram_info = psutil.virtual_memory()
    
    # Mise en forme de la réponse
    response = "Informations sur la RAM :\n"
    response += f"RAM totale: {ram_info.total / (1024 * 1024):.2f} Mo\n"  # ALL RAM - Conversion en Mo
    response += f"RAM utilisée: {ram_info.used / (1024 * 1024):.2f} Mo\n"  # Usage RAM - Conversion en Mo
    response = response.encode('utf-8')

    # Envoyer de la réponse au client
    client_socket.send(response)
    client_socket.close()

def option_3(client_socket):
    # Option 3 : Info réseau
    response = "Informations sur les interfaces réseau :\n"
    interfaces = ni.interfaces()
    # Mise en forme de la réponse
    for iface in interfaces:
        response += f"Nom: {iface}\n"
        response += f"Active : {'Up' if ni.AF_INET in ni.ifaddresses(iface) else 'Down'}\n"
        if ni.AF_INET in ni.ifaddresses(iface):
            ip = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
            netmask = ni.ifaddresses(iface)[ni.AF_INET][0]['netmask']
            response += f"Adresse IP / Masque réseau : {ip} / {netmask}\n"
        response += "\n"
    response = response.encode('utf-8')

    # Envoyer de la réponse au client
    client_socket.send(response)
    client_socket.close()

def option_4(client_socket):
    # Option 4 : Info système d'exploitation
    system_info = platform.uname()

    machine_name = system_info.node
    release = system_info.release
    version = system_info.version

    # Mise en forme de la réponse
    response = f"Informations sur le système d'exploitation :\n"
    response += f"Machine Name: {machine_name}\n"
    response += f"Release: {release}\n"
    response += f"Version: {version}\n"
    response = response.encode('utf-8')

    # Envoie de la réponse au client
    client_socket.send(response)
    client_socket.close()

def option_5(client_socket):
    # Option 4 : Uptime serveur
    uptime = psutil.boot_time()

    # Calculer en heures/minutes/secondes
    uptime_seconds = time.time() - uptime
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Formulation uptime avec heures,minutes,secondes
    response = f"Serveur opérationnel depuis: {int(hours)} heures, {int(minutes)} minutes, {int(seconds)} secondes\n".encode('utf-8')

    # Envoyer de la réponse au client
    client_socket.send(response)
    client_socket.close()

def option_61(client_socket):
    # Option 6.1 : Information disques 1
    response = "Informations sur les volumes (Disque physique et partitions) :\n"

    # Liste des disques physiques
    disk_partitions = psutil.disk_partitions()
    # Mise en forme de la réponse
    for partition in disk_partitions:
        response += f"Device: {partition.device}\n"
        response += f"Mountpoint: {partition.mountpoint}\n"
        response += f"File System Type: {partition.fstype}\n"
        response += "\n"
    response = response.encode('utf-8')

    # Envoyer de la réponse au client
    client_socket.send(response)
    client_socket.close()

def option_62(client_socket):
    # Option 6.2 : Information disques 2
    response = "Utilisation de l'espace disque pour les disques et partitions commençant par '/dev/' :\n\n"

    partitions = psutil.disk_partitions(all=True)

    for partition in partitions:
        device = partition.device
        if device.startswith("/dev/"):
            mountpoint = partition.mountpoint
            disk_usage = psutil.disk_usage(mountpoint)
            capacite_totale_go = disk_usage.total / (1024 ** 3)
            espace_utilise_go = disk_usage.used / (1024 ** 3)
            pourcentage_utilisation = disk_usage.percent
            
            # Mise en forme de la réponse
            response += f"Nom de l'appareil : {device}\n"
            response += f"Point de montage : {mountpoint}\n"
            response += f"Capacité totale : {capacite_totale_go:.2f} Go\n"
            response += f"Utilisation : {espace_utilise_go:.2f} Go\n"
            response += f"Pourcentage d'utilisation : {pourcentage_utilisation}%\n"
            response += "\n"
    response = response.encode('utf-8')

    # Envoyer de la réponse au client
    client_socket.send(response)
    client_socket.close()
    
#-----Partie connexion client et choix option (Appel fonction)-----#
try:
    while True:
        # Accepter la connexion d'un client
        connexion, client_address = server_socket.accept()
        print(f"Connexion établie avec {client_address}")

        # Lire le choix du client
        choice = connexion.recv(2)
        if choice == b'1':
            option_1(connexion)
        elif choice == b'2':
            option_2(connexion)
        elif choice == b'3':
            option_3(connexion)
        elif choice == b'4':
            option_4(connexion)
        elif choice == b'5':
            option_5(connexion)
        elif choice == b'61':
            option_61(connexion)
        elif choice == b'62':
            option_62(connexion)
        else:
            response = b"Option invalide."
            connexion.send(response)
            connexion.close()

#Arrêt du serveur si action clavier (Ctrl+c)
except KeyboardInterrupt:
    print("Serveur arrêté.")

# Fermer le socket serveur
server_socket.close()
import socket
import sys
from datetime import datetime

def scan_ports(target_host, ports):
    print("-" * 50)
    print(f"[*] Scan en cours sur l'hôte : {target_host}")
    print(f"[*] Début du scan : {str(datetime.now())}")
    print("-" * 50)
    
    for port in ports:
        # Création d'une socket IPv4 (AF_INET) et TCP (SOCK_STREAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Timeout de 0.5 seconde pour ne pas bloquer si le port est fermé
        s.settimeout(0.5) 
        
        # connect_ex renvoie 0 si la connexion réussit
        result = s.connect_ex((target_host, port))
        if result == 0:
            print(f"[+] Port {port:4} : OUVERT")
        s.close()

if __name__ == "__main__":
    # Par défaut, on scanne la machine locale (localhost)
    # On cible les ports standards : SSH (22), HTTP (80), HTTPS (443), MySQL (3306)
    target = "127.0.0.1"
    ports_to_scan = [22, 80, 443, 3306, 8080]
    
    scan_ports(target, ports_to_scan)
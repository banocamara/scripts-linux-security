import os
import platform
import sys

def ping_host(ip_address):
    """
    Envoie un paquet ICMP (Ping) à une adresse IP pour vérifier si l'hôte est actif.
    S'adapte automatiquement à l'système d'exploitation (Linux ou Windows).
    """
    # Détermination du paramètre selon le système d'exploitation
    # -c 1 pour Linux (compte 1 paquet), -n 1 pour Windows
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    # Construction de la commande système (ex: ping -c 1 192.168.1.1)
    # On redirige la sortie textuelle pour que le terminal reste propre
    commande = f"ping {param} 1 {ip_address} > /dev/null 2>&1" if param == "-c" else f"ping {param} 1 {ip_address} > nul"
    
    # os.system renvoie 0 si la machine répond (Hôte actif)
    reponse = os.system(commande)
    
    if reponse == 0:
        print(f"[+] Hôte actif : {ip_address}")
        return True
    return False

if __name__ == "__main__":
    print("-" * 50)
    print("[*] Démarrage du Ping Sweep sur le sous-réseau local...")
    print("-" * 50)
    
    # Exemple : On va balayer les adresses de 192.168.1.1 à 192.168.1.10
    base_ip = "192.168.1."
    
    for i in range(1, 11):
        adresse_cible = f"{base_ip}{i}"
        ping_host(adresse_cible)
        
    print("-" * 50)
    print("[*] Balayage terminé.")
    print("-" * 50);
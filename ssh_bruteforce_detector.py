import os
import re
from collections import Counter

# Nombre de tentatives échouées max avant de lever une alerte
SEUIL_ALERTE = 5

def generer_faux_logs_pour_test():
    """
    Génère un fichier de logs temporaire contenant des tentatives de connexion
    réussies et échouées pour simuler un cas réel d'attaque brute force.
    """
    faux_logs = [
        "Jul 15 10:00:01 serveur-ubuntu sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 54321 ssh2\n",
        "Jul 15 10:00:15 serveur-ubuntu sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 54322 ssh2\n",
        "Jul 15 10:00:30 serveur-ubuntu sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 54323 ssh2\n",
        "Jul 15 10:01:00 serveur-ubuntu sshd[1234]: Accepted password for user bano from 192.168.1.50 port 52100 ssh2\n",
        "Jul 15 10:01:12 serveur-ubuntu sshd[1234]: Failed password for root from 10.0.0.8 port 34211 ssh2\n",
        "Jul 15 10:01:45 serveur-ubuntu sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 54324 ssh2\n",
        "Jul 15 10:02:10 serveur-ubuntu sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 54325 ssh2\n",
        "Jul 15 10:02:30 serveur-ubuntu sshd[1234]: Failed password for root from 10.0.0.8 port 34212 ssh2\n",
    ]
    with open("auth_simulation.log", "w") as f:
        f.writelines(faux_logs)
    print("[*] Fichier 'auth_simulation.log' créé pour la simulation.")


def analyser_logs(chemin_fichier):
    """
    Parcourt le fichier de log ligne par ligne et extrait les IP
    qui ont généré des erreurs d'authentification (Failed password).
    """
    print("-" * 60)
    print(f"[*] Analyse du fichier de log : {chemin_fichier}")
    print("-" * 60)

    if not os.path.exists(chemin_fichier):
        print(f"[-] Erreur : Le fichier {chemin_fichier} n'existe pas.")
        return

    tentatives_echouees = []

    # Expression régulière pour capturer l'adresse IP lors d'un échec de mot de passe
    # Format ciblé : "Failed password for ... from <IP_ADDRESS> ..."
    regex_echec = r"Failed password for .* from ([\d\.]+) port"

    with open(chemin_fichier, "r") as fichier:
        for ligne in fichier:
            # Recherche d'un échec d'authentification
            match = re.search(regex_echec, ligne)
            if match:
                ip_attaquant = match.group(1)
                tentatives_echouees.append(ip_attaquant)

    # Comptabiliser le nombre d'occurrences pour chaque IP
    compteur_attaques = Counter(tentatives_echouees)

    alertes_declenché = False
    for ip, nb_tentatives in compteur_attaques.items():
        if nb_tentatives >= SEUIL_ALERTE:
            print(f"[🚨 ALERTE SÉCURITÉ] IP suspecte : {ip} | Tentatives échouées : {nb_tentatives}/{SEUIL_ALERTE} (Brute Force possible)")
            alertes_declenché = True
        else:
            print(f"[i] IP : {ip} | Tentatives échouées : {nb_tentatives} (Sous le seuil d'alerte)")

    if not alertes_declenché:
        print("[+] Analyse terminée : Aucune activité suspecte détectée.")
    print("-" * 60)


if __name__ == "__main__":
    # Test d'accès au vrai fichier système ou lancement du mode simulation
    vrai_chemin_systeme = "/var/log/auth.log"

    if os.path.exists(vrai_chemin_systeme) and os.access(vrai_chemin_systeme, os.R_OK):
        print("[+] Droits de lecture OK sur le journal système. Analyse réelle...")
        analyser_logs(vrai_chemin_systeme)
    else:
        print("[!] Impossible de lire /var/log/auth.log (accès restreint ou OS différent).")
        print("[*] Lancement automatique du mode SIMULATION...")
        generer_faux_logs_pour_test()
        analyser_logs("auth_simulation.log")
        
        # Nettoyage
        if os.path.exists("auth_simulation.log"):
            os.remove("auth_simulation.log")
            print("[*] Fichier de simulation nettoyé.")

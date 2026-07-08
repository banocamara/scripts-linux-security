import socket

def validate_ip(ip_address):
    try:
        # La fonction inet_aton lève une erreur si l'IP n'est pas au format IPv4 valide
        socket.inet_aton(ip_address)
        print(f"[+] L'adresse IP {ip_address} est VALIDE.")
        return True
    except socket.error:
        print(f"[-] L'adresse IP {ip_address} est INVALIDE.")
        return False

if __name__ == "__main__":
    # Test de l'outil
    validate_ip("192.168.1.1")   # Valide
    validate_ip("999.999.9.9")   # Invalide
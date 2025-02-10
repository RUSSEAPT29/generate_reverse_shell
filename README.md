# Reverse Shell Generator

Ce projet est un script Python tout-en-un pour générer, chiffrer et compiler un reverse shell Windows en C++. Le script automatise la création d'un exécutable qui établit une connexion reverse shell vers une adresse IP et un port spécifiés.

## Fonctionnalités

- Génération automatique de shellcode avec msfvenom
- Chiffrement XOR du payload pour éviter la détection statique
- Génération d'un fichier C++ prêt à être compilé
- Compilation automatique en exécutable Windows
- Nettoyage des fichiers temporaires

## Prérequis

- Python 3.x
- Metasploit Framework (msfvenom)
- Mingw-w64 (pour la compilation)

### Installation des dépendances

Sur Debian/Ubuntu :

```bash
sudo apt update
sudo apt install python3 python3-pip mingw-w64 metasploit-framework
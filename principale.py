import random

# Ouvre le fichier en lecture
with open("mot.txt") as fichier:
    # Lit toutes les lignes et enlève les retours à la ligne
    mot_choisi=random.choice([ligne.strip() for ligne in fichier])

print("Mot choisi :", mot_choisi)

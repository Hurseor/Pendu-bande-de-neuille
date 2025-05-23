#Mot à saisir pour lancer le programme : "python principale.py"
import random

choixx = input("Ecrivez 1 pour jouer seul et 2 pour jouer à deux: ")
if choixx == "1":
    # Ouvre le fichier en lecture
    with open("mots.txt") as fichier:
        # Lit toutes les lignes et enlève les retours à la ligne
        mot_choisi=str(random.choice([ligne.strip() for ligne in fichier]))
else:
    mot_choisi= input("Joueur 2, choisissez un mot: ")

dico={}
rang=1

for ltr in mot_choisi:
    if ltr not in dico:
        dico[ltr]=[str(rang)]
    else:
        dico[ltr]+=[str(rang)]
    rang+=1


vie=int(10)
elt=rang-1
print(f"Ce mot a {elt} position")

def lettre(rep1):
    global vie
    if rep1 in dico:
        print(f"le rang de la lettre '{rep1}' est à la {dico.get(rep1)} position")
    else:
        vie-=1
        print(f"Il n'y a pas la lettre '{rep1}' donc vous reste {vie} vie")

def mot(rep2):
    if rep2==mot_choisi:
        print(f"Le mot était: {mot_choisi}, vous êtes génial")
    else:
        print(f"Le mot n'est pas: {rep2}, c'était: {mot_choisi} donc il vous éliminé")

validation=False
while vie>0 and validation!=True:
    choix=str(input("Voulez-vous devinez une lettre ou devinez le mot? (répondre par 'mot' ou 'lettre') :"))
    if choix=="lettre":
        rep1=str(input("Votre lettre? :"))
        lettre(rep1)
    elif choix=="mot":
        rep2=str(input("Quel est le mot? :"))
        mot(rep2)
        validation=True
    else:
        print("répondre par 'mot' ou 'lettre'")

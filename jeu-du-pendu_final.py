#Mot à saisir pour lancer le programme : "jeu-du-pendu_final.py"
import tkinter as tk
from tkinter import messagebox
import random
from tkinter import filedialog
from datetime import datetime

# Variables globales utilisées dans tout le programme
mot_choisi = ""
dico = {}
vie = 10
vie_initiale = 10
validation = False
lettres_fausses = set()
affichage_mot = []
elt = 0
mot_trouve = False
mode_actuel = "1"

#Fonctions principales du jeu 
def initialiser_mot(choix_mode: str, saisie_joueur: str | None = None) -> None:
    """
    Initialise les variables du jeu selon le mode choisi (solo ou duo) et prépare le mot à deviner.
    Prend en paramètre deux choses :
    - choix_mode : Mode de jeu "1" pour solo, "2" pour duo.
    - saisie_joueur : Mot saisi par le joueur 2 en mode duo, sinon None.
    """
    global mot_choisi, dico, vie, lettres_fausses, affichage_mot, elt, validation, mot_trouve, mode_actuel
    vie = vie_initiale
    validation = False
    mot_trouve = False
    lettres_fausses = set()
    dico = {}
    mode_actuel = choix_mode

    if choix_mode == "1":
        with open("mots.txt") as fichier:
            mot_choisi = str(random.choice([ligne.strip() for ligne in fichier]))
    else:
        mot_choisi = saisie_joueur

    rang = 1
    for ltr in mot_choisi:
        if ltr not in dico:
            dico[ltr] = [str(rang)]
        else:
            dico[ltr] += [str(rang)]
        rang += 1

    elt = rang - 1
    affichage_mot = ["_"] * elt

def lettre(rep1: str) -> str:
    """
    Traite la proposition d'une lettre : met à jour l'affichage si elle est dans le mot, retire une vie sinon.
    Prend en paramètre rep1 : Lettre proposée par le joueur.
    Renvoie un message indiquant la position de la lettre ou le nombre de vies restantes.
    """
    global vie
    if rep1 in dico:
        for pos in dico[rep1]:
            affichage_mot[int(pos) - 1] = rep1
        return f"La lettre '{rep1}' est à la position {', '.join(dico[rep1])}"
    else:
        vie -= 1
        return f"La lettre '{rep1}' n'est pas dans le mot. Il vous reste {vie} vies."

def mot(rep2: str) -> str:
    """
    Traite la proposition d'un mot : indique si la proposition est correcte et termine la partie.
    Prend en argument rep2 : Mot proposé par le joueur.
    Renvoie un message de victoire ou de défaite avec le mot correct.
    """
    global validation, mot_trouve
    if rep2 == mot_choisi:
        validation = True
        mot_trouve = True
        return f"Bravo ! Le mot était : {mot_choisi}"
    else:
        validation = True
        return f"Faux ! Le mot était : {mot_choisi}"

# Enregistrement de la partie 
def enregistrer_partie() -> None:
    """
    Enregistre les résultats de la partie dans un fichier texte choisi par l'utilisateur (mot, vies, date, réussite).
    """
    try:
        # Ouvre une boîte de dialogue pour que l'utilisateur choisisse l'emplacement et le nom du fichier
        chemin_fichier = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt")],
            title="Enregistrer la partie",
            initialfile="partie_pendu.txt"
        )

        # Si l'utilisateur a annulé, on sort de la fonction
        if not chemin_fichier:
            return

        resultat = "TROUVÉ" if mot_trouve else "NON TROUVÉ"
        vies_utilisées = vie_initiale - vie
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Écrit les données dans le fichier choisi
        with open(chemin_fichier, "a", encoding="utf-8") as fichier:
            fichier.write(f"[{date}] Mot : {mot_choisi} | Vies utilisées : {vies_utilisées} | Résultat : {resultat}\n")

        messagebox.showinfo("Sauvegarde", f"Partie enregistrée avec succès dans :\n{chemin_fichier}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement : {e}")

# Interface graphique 
def lancer_jeu(mode: str) -> None:
    """
    Lance le jeu selon le mode choisi : solo (mot aléatoire) ou duo (saisie d’un mot par le joueur 2).
    Prend en paramètre deux choses : "1" pour solo, "2" pour duo.
    """
    def valider_mot_joueur2() -> None:
        """
        Valide le mot saisi par le joueur 2, lance la partie en mode duo si le mot est valide.
        """
        mot_utilisateur = entry_mot.get()
        if mot_utilisateur.isalpha():
            initialiser_mot("2", mot_utilisateur.lower())
            afficher_interface_jeu()
        else:
            messagebox.showerror("Erreur", "Entrez un mot valide.")

    for widget in root.winfo_children():
        widget.destroy()

    if mode == "1":
        initialiser_mot("1")
        afficher_interface_jeu()
    else:
        label = tk.Label(root, text="Joueur 2, entrez un mot :", font=("Helvetica", 16))
        label.pack(pady=10)
        entry_mot = tk.Entry(root, font=("Helvetica", 16))
        entry_mot.pack()
        btn_valider = tk.Button(root, text="Valider", command=valider_mot_joueur2, font=("Helvetica", 16))
        btn_valider.pack(pady=10)

def afficher_interface_jeu() -> None:
    """
    Affiche l’interface principale du jeu (saisie des lettres ou mots, feedback, gestion des événements).
    """
    def jouer() -> None:
        """
        Sous-fonction qui traite chaque saisie (lettre ou mot) : met à jour les labels, détecte victoire ou défaite.
        """
        global validation, mot_trouve
        if validation or vie <= 0:
            return

        choix = var_choix.get()
        reponse = entry_input.get().lower().strip()
        if not reponse.isalpha():
            messagebox.showwarning("Erreur", "Veuillez entrer une lettre ou un mot valide.")
            return

        if choix == "lettre" and len(reponse) == 1:
            resultat = lettre(reponse)
            if reponse not in dico:
                lettres_fausses.add(reponse)
        elif choix == "mot":
            resultat = mot(reponse)
        else:
            messagebox.showwarning("Erreur", "Choisissez 'lettre' ou 'mot' et entrez une saisie correcte.")
            return

        label_resultat.config(text=resultat)
        label_tirets.config(text=" ".join(affichage_mot))
        label_lettres.config(text="Lettres fausses : " + ", ".join(sorted(lettres_fausses)))
        entry_input.delete(0, tk.END)

        if "_" not in affichage_mot:
            mot_trouve = True
            validation = True
            afficher_boutons_fin()
            messagebox.showinfo("Gagné", f"Vous avez trouvé le mot : {mot_choisi}")
        elif vie <= 0:
            afficher_boutons_fin()
            messagebox.showerror("Perdu", f"Vous avez perdu ! Le mot était : {mot_choisi}")

    def afficher_boutons_fin() -> None:
        """
        Affiche les boutons de fin de partie (rejouer ou enregistrer).
        """
        btn_rejouer.pack(pady=10)
        btn_sauvegarder.pack()

    for widget in root.winfo_children():
        widget.destroy()

    global label_tirets, label_lettres, entry_input, label_resultat, var_choix, btn_rejouer, btn_sauvegarder

    label_tirets = tk.Label(root, text=" ".join(affichage_mot), font=("Helvetica", 28))
    label_tirets.pack(pady=20)

    label_lettres = tk.Label(root, text="Lettres fausses : ", font=("Helvetica", 14))
    label_lettres.pack()

    var_choix = tk.StringVar(value="lettre")
    frame_choix = tk.Frame(root)
    tk.Radiobutton(frame_choix, text="Lettre", variable=var_choix, value="lettre", font=("Helvetica", 14)).pack(side="left", padx=10)
    tk.Radiobutton(frame_choix, text="Mot", variable=var_choix, value="mot", font=("Helvetica", 14)).pack(side="left", padx=10)
    frame_choix.pack(pady=10)

    entry_input = tk.Entry(root, font=("Helvetica", 16))
    entry_input.pack()

    btn_valider = tk.Button(root, text="Valider", command=jouer, font=("Helvetica", 16))
    btn_valider.pack(pady=10)

    label_resultat = tk.Label(root, text="", font=("Helvetica", 14))
    label_resultat.pack()

    # Boutons fin de partie
    btn_rejouer = tk.Button(root, text="Recommencer à jouer", command=lambda: lancer_jeu(mode_actuel), font=("Helvetica", 14))
    btn_sauvegarder = tk.Button(root, text="Enregistrer la partie", command=enregistrer_partie, font=("Helvetica", 14))

# Menu principal de l'interface graphique Tkinter
root = tk.Tk()
root.title("Jeu du Pendu")
root.geometry("600x500")

label_titre = tk.Label(root, text="Jeu du Pendu", font=("Helvetica", 32, "bold"))
label_titre.pack(pady=30)

btn_solo = tk.Button(root, text="Jouer en solo", command=lambda: lancer_jeu("1"), font=("Helvetica", 20), width=20)
btn_solo.pack(pady=10)

btn_duo = tk.Button(root, text="Jouer à deux", command=lambda: lancer_jeu("2"), font=("Helvetica", 20), width=20)
btn_duo.pack(pady=10)

root.mainloop()

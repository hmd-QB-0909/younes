import sqlite3
from colorama import Fore, Style
from tqdm import tqdm
import time

# Connexion à la base de données et création de la table si elle n'existe pas
db = sqlite3.connect("users.db")
cr = db.cursor()

cr.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER
    )
""")
db.commit()

# Fonction d'ajout d'un utilisateur
def add_user():
    """Ajouter un nouvel utilisateur"""
    name = input("🔹 Entrez le nom de l'utilisateur : ").strip().capitalize()
    age = input("🔹 Entrez l'âge de l'utilisateur : ").strip()

    if name and age.isdigit():
        # Simulation d'une opération en ajoutant une barre de progression
        for _ in tqdm(range(100), desc="Ajout de l'utilisateur"):
            time.sleep(0.02)

        cr.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, int(age)))
        db.commit()
        print(Fore.GREEN + f"✅ {name} a été ajouté avec succès !" + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ Erreur : Veuillez entrer des données valides !" + Style.RESET_ALL)

# Fonction pour afficher tous les utilisateurs
def show_users():
    """Afficher tous les utilisateurs"""
    cr.execute("SELECT * FROM users")
    users = cr.fetchall()

    if users:
        print("\n📋 Liste des utilisateurs :")
        print("🆔 ID  | 👤 Nom      | 🎂 Âge")
        print("-" * 30)
        for user in users:
            print(f"{user[0]:<4} | {user[1]:<10} | {user[2]:<3}")
    else:
        print(Fore.YELLOW + "⚠️ Aucun utilisateur trouvé dans la base de données." + Style.RESET_ALL)

# Fonction pour mettre à jour un utilisateur
def update_user():
    """Mettre à jour les informations d'un utilisateur"""
    user_id = input("🔹 Entrez l'ID de l'utilisateur à modifier : ").strip()
    new_age = input("🔹 Entrez le nouvel âge : ").strip()

    if user_id.isdigit() and new_age.isdigit():
        cr.execute("UPDATE users SET age = ? WHERE id = ?", (int(new_age), int(user_id)))
        db.commit()

        if cr.rowcount:
            print(Fore.GREEN + f"✅ L'utilisateur ID {user_id} a été mis à jour avec succès !" + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Erreur : Utilisateur non trouvé !" + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ Erreur : Veuillez entrer des valeurs valides !" + Style.RESET_ALL)

# Fonction pour supprimer un utilisateur
def delete_user():
    """Supprimer un utilisateur"""
    user_id = input("🔹 Entrez l'ID de l'utilisateur à supprimer : ").strip()

    if user_id.isdigit():
        confirm = input(f"Êtes-vous sûr de vouloir supprimer l'utilisateur ID {user_id} ? (y/n) : ").strip().lower()
        if confirm == 'y':
            cr.execute("DELETE FROM users WHERE id = ?", (int(user_id),))
            db.commit()

            if cr.rowcount:
                print(Fore.GREEN + f"✅ L'utilisateur ID {user_id} a été supprimé avec succès !" + Style.RESET_ALL)
            else:
                print(Fore.RED + "❌ Erreur : Utilisateur non trouvé !" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "❌ Suppression annulée." + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ Erreur : Veuillez entrer un ID valide !" + Style.RESET_ALL)

# Fonction pour afficher l'aide
def show_help():
    """Afficher l'aide sur les options disponibles"""
    print("""
    📖 ** Guide d'Aide **
    1️⃣ Ajouter un utilisateur : Ajouter un nouvel utilisateur avec son nom et son âge.
    2️⃣ Afficher tous les utilisateurs : Voir tous les utilisateurs dans la base de données.
    3️⃣ Mettre à jour un utilisateur : Modifier les données d'un utilisateur (par exemple, l'âge).
    4️⃣ Supprimer un utilisateur : Retirer un utilisateur de la base de données en utilisant son ID.
    5️⃣ Quitter : Fermer le programme.
    """)

# Menu principal et boucle de l'application
while True:
    print("\n📌 ** Menu **")
    print("1️⃣ - Ajouter un utilisateur")
    print("2️⃣ - Afficher tous les utilisateurs")
    print("3️⃣ - Mettre à jour les données d'un utilisateur")
    print("4️⃣ - Supprimer un utilisateur")
    print("5️⃣ - Aide")
    print("6️⃣ - Quitter")

    choice = input("🔸 Entrez votre choix : ").strip()

    if choice == "1":
        add_user()
    elif choice == "2":
        show_users()
    elif choice == "3":
        update_user()
    elif choice == "4":
        delete_user()
    elif choice == "5":
        show_help()
    elif choice == "6":
        print("👋 Fermeture du programme.")
        db.close()
        break
    else:
        print(Fore.RED + "⚠️ Choix invalide ! Veuillez réessayer." + Style.RESET_ALL)

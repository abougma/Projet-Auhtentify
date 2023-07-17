import requests

# Fonction pour s'inscrire à l'application
def register():
    username = input("Entrez un nom d'utilisateur : ")
    password = input("Entrez un mot de passe : ")

    # Envoi de la requête POST à l'API pour enregistrer l'utilisateur
    response = requests.post("http://localhost:8000/register", json={"pseudo": username, "password": password})

    if response.status_code == 200:
        print("Inscription réussie !")
    else:
        print("L'utilisateur existe deja !!")

# Fonction pour se connecter à l'application
def login():
    username = input("Entrez votre nom d'utilisateur : ")
    password = input("Entrez votre mot de passe : ")

    # Envoi de la requête POST à l'API pour connecter l'utilisateur
    response = requests.post("http://localhost:8000/login", json={"pseudo": username, "password": password})

    if response.status_code == 200:
        print("Connexion réussie !")
    else:
        print("Impossible de se connecter avec les informations fournies.")

# Menu principal
while True:
    
    print("-----------Bienvenu chez authentify---------")
    print("Que voulez-vous faire ?")
    print("0. Quitter le programme")
    print("1. S'inscrire pour s'authentifier")
    print("2. Se connecter à l'application")

    choice = input("Entrez votre choix : ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "0":
        print("Au revoir !")
        break    
    else:
        print("Choix invalide.")

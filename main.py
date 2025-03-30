# Importation des modules nécessaires
from shutil import copy
from os import getenv, path
from dotenv import load_dotenv
from configparser import ConfigParser
from discord import Activity, ActivityType, Client, Intents
from anthropic import Anthropic

# Vérification que le fichier "settings.ini" existe
if not path.exists("settings.ini"):
    # Vérifier si "settings.example.ini" existe
    if not path.exists("settings.example.ini"):
        # Lever une exception si "settings.example.ini" est introuvable
        raise FileNotFoundError("Les fichiers \"settings.ini\" et \"settings.example.ini\" sont introuvables.")

    # Copie du fichier "settings.example.ini" vers "settings.ini"
    copy("settings.example.ini", "settings.ini")

# Chargement du fichier de configuration
config = ConfigParser()
config.read("settings.ini")
PROMPT = config["SETTINGS"].get("PROMPT", "")
MODEL = config["SETTINGS"].get("MODEL", "claude-3-haiku-20240307") or "claude-3-haiku-20240307"
CHANNELS = tuple(map(int, config["SETTINGS"]["CHANNELS"].split(","))) if "CHANNELS" in config["SETTINGS"] else (0,)
ACTIVITY_NAME = config["SETTINGS"].get("ACTIVITY_NAME", None)
activity_type = config["SETTINGS"].get("ACTIVITY_TYPE", None)
ACTIVITY_TYPE = getattr(ActivityType, activity_type, None) if activity_type else None
HISTORY_LENGTH = max(1, config["SETTINGS"].getint("HISTORY_LENGTH", 1))

# Si le fichier .env existe
if path.exists(".env"):
    # Chargement des variables d’environnement à partir du fichier .env
    load_dotenv()

# Récupération du jeton d’accès Discord à partir des variables d’environnement
DISCORD_TOKEN = getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("Aucun jeton d’accès Discord trouvé dans le fichier .env ou dans les variables d’environnement")

# Création de l’activité
activity = Activity(name=ACTIVITY_NAME, type=ACTIVITY_TYPE) if ACTIVITY_TYPE and ACTIVITY_NAME else None

# Création des intents pour le client Discord
intents = Intents.default()
intents.message_content = True

# Création du client Discord
client = Client(activity=activity, intents=intents)

# Création de l’instance Anthropic
anthropic = Anthropic()


# Événement déclenché lorsque le bot est prêt
@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")


# Événement déclenché lorsqu’un message est envoyé
@client.event
async def on_message(message):
    # Vérification que le message n’est pas envoyé par un bot et qu’il n’est pas vide
    if message.author.bot or not message.content:
        return
    # Vérification que le bot est mentionné dans le message ou que le message est envoyé dans un salon autorisé
    if client.user not in message.mentions and message.channel.id not in CHANNELS:
        return

    # Dernier message traité
    last_msg = None
    # Création de la liste des messages et de l'historique
    messages = []
    history = []

    # Envoi d’une indication que le bot est en train d’écrire
    async with message.channel.typing():
        # Récupération de l’historique des messages du salon
        async for msg in message.channel.history(limit=HISTORY_LENGTH):
            # Ajout les messages à la liste
            history.append(msg)

        # Inversion de l’ordre des messages
        history.reverse()

        for msg in history:
            # Si le message a été envoyé par un autre bot ou est vide, on passe au suivant
            if (msg.author.bot and msg.author != client.user) or not msg.content:
                continue

            # Détermine le rôle
            role = "assistant" if msg.author.bot else "user"

            # Si le message précédent vient du même utilisateur, on fusionne
            if last_msg and last_msg["role"] == role:
                # On ajoute le contenu du message actuel à celui du précédent
                last_msg["content"].append({"type": "text", "text": msg.content})
            else:
                # Sinon, on ajoute un nouveau message
                new_msg = {
                    "role": role,
                    "content": [{"type": "text", "text": msg.content}]
                }
                messages.append(new_msg)
                last_msg = new_msg  # On garde en mémoire ce message comme dernier message

        # Appel à l’API Anthropic pour générer une réponse
        completion = anthropic.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=PROMPT,
            messages=messages
        )

        # Envoi de la réponse générée par Claude
        await message.reply(completion.content[0].text.encode("utf-8").decode("utf-8"))


# Démarrage du client Discord avec le jeton d’accès
client.run(DISCORD_TOKEN)

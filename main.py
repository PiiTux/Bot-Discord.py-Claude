# Importation des modules nécessaires
from os import getenv, path
from dotenv import load_dotenv
from configparser import ConfigParser
from discord import Activity, ActivityType, Client, Intents
from anthropic import Anthropic

# Chargement du fichier de configuration
config = ConfigParser()
config.read("settings.ini")
PROMPT = config["SETTINGS"]["PROMPT"]
MODEL = config["SETTINGS"]["MODEL"]
CHANNELS = tuple(map(int, config["SETTINGS"]["CHANNELS"].split(",")))
ACTIVITY_NAME = config["SETTINGS"]["ACTIVITY_NAME"]
activity_type_str = config["SETTINGS"]["ACTIVITY_TYPE"]
ACTIVITY_TYPE = getattr(ActivityType, activity_type_str, None)
HISTORY_LENGTH = config["SETTINGS"].getint("HISTORY_LENGTH")

# Si le fichier .env existe
if path.exists(".env"):
    # Chargement des variables d’environnement à partir du fichier .env
    load_dotenv()

# Création de l’activité
activity = Activity(name=ACTIVITY_NAME, type=ACTIVITY_TYPE)

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
client.run(getenv("DISCORD_TOKEN"))

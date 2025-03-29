# 🤖 Bot Discord Claude 🧠

Bienvenue sur ton super bot Discord qui répond avec **Claude** ! 😜

## Fonctionnalités 🔥

- 📩 Répond aux messages dans les salons configurés ou s’il est mentionné.
- 🔧 Configuration ultra simple grâce au fichier `settings.ini` !
- ⚡ Léger et rapide, grâce à `discord.py` (la magie Python 🐍).

## 💡 Comment ça marche ?

Il garde un œil sur les salons que tu as choisis, ou attend gentiment d’être invoqué par ta mention Discord comme un démon en quête d’âme à torturer, prêt à répondre ~~en échange de quelques sacrifices~~ ! 👹

## 📦 Installation

### 📋 Prérequis
- Python (version 3.8 ou supérieure). Si tu as une version plus vieille… c’est probablement le moment de la mettre à jour 😉

### 🚀 Étapes d’installation

1. Clone le dépôt :
    ```bash
    git clone https://github.com/PiiTux/Bot-Discord.py-Claude.git
    cd Bot-Discord.py-Claude
    ```

2. Crée un environnement virtuel pour que tout soit bien isolé :
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Installe les dépendances :
    ```bash
    pip install -U discord python-dotenv anthropic
    ```

### ⚙️ Configuration

1. **Crée un fichier `.env`** : À la racine du projet, ajoute un fichier `.env` pour stocker les infos sensibles.
2. **Ajoute-y ton token Discord** : Ajoute cette ligne dans ton fichier `.env` pour que le bot puisse se connecter :
    ```env
    DISCORD_TOKEN = VOTRE_TOKEN_DISCORD_ICI
    ```
3. **Ajoute ta clé API** : Ajoute ta clé API Anthropic dans le fichier `.env` comme ça :
    ```env
    ANTHROPIC_API_KEY = Votre_clé_API_Anthropic_ici
    ```
4. **Paramètres dans `settings.ini`** : Le bot se configure avec un fichier `settings.ini` ultra simple (presque trop facile, genre pas d’excuses !). Voilà ce que tu peux modifier pour faire tourner la bête :
- **`PROMPT`** : C’est la personnalité de ton assistant ! Si tu veux qu’il soit plus sérieux, plus drôle, ou même qu’il fasse des blagues pourries, tu peux changer ce texte. 😜
- **`MODEL`** : C’est là que tu choisis quel modèle de Claude utiliser (par exemple `claude-3-5-haiku-latest` ou `claude-3-7-sonnet-latest`). C’est toi qui choisis ! 🚀
- **`CHANNELS`** : Mets ici les ID des salons où ton bot doit répondre. Sépare-les par des virgules (exemple : `123456789, 987654321`). Il surveillera ces salons pour les messages. 📲
- **`ACTIVITY_NAME` et `ACTIVITY_TYPE`** : L’activité du bot, genre ce qu’il fait sur Discord. Par exemple, il peut "jouer à répondre aux questions". 🎮
- **`HISTORY_LENGTH`** : C’est le nombre de messages que le bot garde en mémoire pour répondre de manière plus cohérente. Plus c’est long, plus il a d’infos, mais il consomme aussi plus de ressources. 📚

## 🚀 Démarrage du bot

1. Une fois que tu as tout configuré, tu peux lancer ton bot (pas trop violemment) avec cette commande :
    ```bash
    python3 main.py
    ```
2. Pour l’exécuter en arrière-plan sans trop de souffrance (promis, il ne criera pas), tu peux utiliser cette commande :
    ```bash
    nohup python3 main.py &
    ```
3. Ou avec `tmux` (si tu es du genre à aimer organiser ta vie comme un boss) :
    ```bash
    tmux new -s bot_discord "python3 main.py"
    ```

## 🛠️ Dépannage

Si le bot joue les troubles-fêtes, voici quelques vérifications :

1. **Vérifie ton token Discord**
   - Ton fichier `.env` doit contenir la ligne suivante avec un token valide :
     ```
     DISCORD_TOKEN = VOTRE_TOKEN_DISCORD_ICI
     ```
   - Assure-toi qu’il n’a pas été révoqué via le [portail des développeurs Discord](https://discord.com/developers/applications).

2. **Le fichier `settings.ini`**
   - Vérifie que les ID des salons sont corrects :
     ```ini
     CHANNELS = 0000000000000000000, 0000000000000000000
     ```
   - Le bot doit avoir la permission d’envoyer des messages dans ces salons.
   - Vérifie le modèle est bien choisi (claude-3-haiku-20240307, claude-3-5-haiku-latest, claude-3-7-sonnet-latest, ...).
     ```ini
     MODEL = claude-3-haiku-20240307
     ```

3. **Les dépendances sont-elles installées ?**
   - Assure-toi que tout est bien installé :
    ```bash
    pip install -U discord python-dotenv anthropic
    ```

4. **Regarde les logs**
   - Si le bot plante, regarde les erreurs affichées dans le terminal pour avoir un indice.

## 📜 Licence

Ce projet est sous licence Apache 2.0. Consulte le fichier [LICENSE](LICENSE) pour plus d’infos.
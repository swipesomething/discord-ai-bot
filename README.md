# Discord AI Bot

This project aims to provide the means to quickly whip out a free Discord chatbot with AI capabilities. Users can ask questions and the bot will use a large language model to reply. I'm using this to learn how to use github, so if it's not that good, well, sorry about that, I'm an amateur and this whole setup could probably be coded better :P

The bot uses Qwen2.5-72B-Instruct via the HuggingFace API.

## Requirements

To run this bot, you need:

- Have docker and docker compose installed
- A **Discord Bot Token**: Allows the bot to connect to and interact on Discord.
- Your **Discord ID**: Used for managing bot commands and permissions.
- A **Hugging Face Token**: Required to connect the bot with Hugging Face for AI model access.
- **System Prompt**: This is an optional but helpful prompt that establishes the bot's general tone and behavior, giving it a consistent personality or response style.

## Quick start

### Clone the Project

```bash
git clone https://github.com/swipesomething/discord-ai-bot.git
cd discord-ai-bot
```

### Configure the Bot

1. In the `bot` directory, open `config.ini`.
2. Add the following information:
   - **Discord Bot Token**: The token for your bot (available in the Discord Developer Portal).
   - **Discord Owner ID**: Your personal Discord user ID (for bot management permissions).
   - **Hugging Face Token**: Token for connecting to Hugging Face models (available in your Hugging Face account).
   - **System Prompt**: A custom instruction or guiding message to influence the bot's initial responses and behavior.

   Example `config.ini`:
   ```ini
   [DISCORD]
   token=your_discord_bot_token
   owner=your_discord_user_id
   
   [AI]
   hftoken=your_huggingface_token
   system=System Prompt for the chat bot
   ```

### Start the container

Once configured, start the docker container:

```bash
sudo docker compose up -d
```

### ⚠️ **Note for Ubuntu Users**:  
> If `docker compose` doesn't work, it could be because Docker Compose was installed via Ubuntu's package manager (`apt`), which installs the older standalone `docker-compose` command instead of the integrated `docker compose` subcommand.
>
> To resolve this, try starting the container with:
> ```bash
> sudo docker-compose up -d
> ```
> Alternatively, you can reinstall Docker and Docker Compose using the [official Docker installation instructions](https://docs.docker.com/engine/install/), which include the integrated `docker compose` CLI.

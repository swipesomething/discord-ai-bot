from discord.ext import commands
from discord.ext.commands import Context
from ai_chat import chat
import discord


class Chat(commands.Cog, name="chat"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conversation_history = {}  # Dictionary to store conversation history by channel ID
        self.last_message_ids = {}  # Dictionary to store last message ID by message ID

    @commands.hybrid_command(
        name="chat",
        description="Talk to Pixelle",
    )
    async def chat(self, context: Context, prompt: str, skip_intro: bool = False) -> None:
        # Send the user's question to the channel
        if not skip_intro:
            await context.send(f"{context.author.mention} asked: {prompt}")

        channel_id = context.channel.id

        # Retrieve existing history or start a new one for the channel
        if channel_id not in self.conversation_history:
            self.conversation_history[channel_id] = []

        # Append the user's message to the history, including username
        self.conversation_history[channel_id].append(f"{context.author.display_name}: {prompt}")

        # Limit the conversation history to the last 10 exchanges
        if len(self.conversation_history[channel_id]) > 20:  # 10 exchanges means 20 messages (10 user + 10 bot)
            self.conversation_history[channel_id] = self.conversation_history[channel_id][-20:]

        # Show that the bot is typing
        async with context.channel.typing():
            # Use the entire conversation history as context
            history = "\n".join(self.conversation_history[channel_id])
            response = await chat(history)  # Use await here since the chat function is now async

            # Append the bot's response to the history
            self.conversation_history[channel_id].append(f"Pixelle: {response}")

        # Ensure the response is no longer than 4096 characters
        MAX_EMBED_LENGTH = 4096
        response = response[:MAX_EMBED_LENGTH]

        # Create an embed for the response
        embed = discord.Embed(title=f"{context.author.display_name}'s Question", description=response, color=discord.Color.blue())
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar.url)

        # Send the response in an embed and store the message ID
        message = await context.send(embed=embed)
        self.last_message_ids[message.id] = message.id

    @commands.hybrid_command(
        name="show_context",
        description="Show the current conversation history",
    )
    async def show_context(self, context: Context) -> None:
        channel_id = context.channel.id

        # Retrieve and display the conversation history
        if channel_id in self.conversation_history and self.conversation_history[channel_id]:
            history = "\n".join(self.conversation_history[channel_id])
            # Ensure the history is no longer than 4096 characters
            MAX_EMBED_LENGTH = 4096
            history = history[:MAX_EMBED_LENGTH]

            # Create an embed for the conversation history
            embed = discord.Embed(title="Conversation History", description=history, color=discord.Color.green())
            await context.send(embed=embed)
        else:
            response = "No conversation history found."
            await context.send(response)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.bot.user:
            return

        # Check if the message is a reply to the bot's message
        if message.reference and message.reference.message_id:
            original_message_id = message.reference.message_id

            # Check if the original message ID matches the stored ID for the user
            if original_message_id in self.last_message_ids:
                # Use the message content as the new prompt
                new_prompt = message.content
                await self.chat(Context(message=message, bot=self.bot, prefix=None, view=None), new_prompt, skip_intro=True)

        # Check if the message starts by mentioning the bot
        if message.content.startswith(f"<@{self.bot.user.id}>"):
            # Extract the prompt from the message (removing the mention)
            prompt = message.content[len(f"<@{self.bot.user.id}> "):].strip()
            if prompt:
                await self.chat(Context(message=message, bot=self.bot, prefix=None, view=None), prompt, skip_intro=True)

    @commands.hybrid_command(
        name="clear_history",
        description="Clear the chat history with Pixelle",
    )
    async def clear_history(self, context: Context) -> None:
        channel_id = context.channel.id

        # Clear the channel's conversation history
        if channel_id in self.conversation_history:
            del self.conversation_history[channel_id]
            response = "The conversation history has been cleared."
        else:
            response = "No conversation history found to clear."

        # Send the response
        await context.send(response, ephemeral=True)

async def setup(bot) -> None:
    await bot.add_cog(Chat(bot))

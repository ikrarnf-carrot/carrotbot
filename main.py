import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
LYRICS_CHANNEL_ID = int(os.getenv("LYRICS_CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

GENRES = {
    "emo": "🖤 Emo",
    "posthardcore": "🔥 Post-Hardcore",
    "metalcore": "💀 Metalcore",
    "altrock": "🎸 Alt Rock",
    "indie": "🌙 Indie",
    "experimental": "🌀 Experimental",
    "custom": "✨ Other"
}
GENRE_COLORS = {
    "emo": discord.Color.dark_gray(),
    "posthardcore": discord.Color.dark_orange(),
    "metalcore": discord.Color.dark_red(),
    "altrock": discord.Color.blurple(),
    "indie": discord.Color.teal(),
    "experimental": discord.Color.fuchsia(),
    "custom": discord.Color.gold()
}

class LyricsModal(discord.ui.Modal, title="🎼 Write Your Mantra"):
    def __init__(self, selected_genre):
        super().__init__()
        self.selected_genre = selected_genre

        self.title_input = discord.ui.TextInput(label="🎵 Title", max_length=100)
        self.lyrics_input = discord.ui.TextInput(
            label="📝 Lyrics",
            style=discord.TextStyle.paragraph,
            placeholder="Write something or I will sleep",
            max_length=4000
        )

        self.add_item(self.title_input)
        self.add_item(self.lyrics_input)

    async def on_submit(self, interaction: discord.Interaction):
        genre_key = self.selected_genre
        genre_label = GENRES.get(genre_key, "🎶 Unknown")
        embed_color = GENRE_COLORS.get(genre_key, discord.Color.purple())

        paragraphs = [p.strip() for p in self.lyrics_input.value.strip().split("\n\n")]
        formatted_lyrics = "\n\n".join(paragraphs)

        embed_description = (
            f"*{genre_label}*\n\n"  
            f"**__{self.title_input.value.strip()}__**\n\n"  
            f"{formatted_lyrics}"  
        )

        embed = discord.Embed(
            description=embed_description,
            color=embed_color,
            timestamp=discord.utils.utcnow()
        )

        embed.set_author(
            name=f"{interaction.user.display_name}'s lyrics",
            icon_url=interaction.user.display_avatar.url
        )

        embed.set_footer(
            text="📝 CarrotBot • Use /writelyrics to submit yours"
        )

        channel = bot.get_channel(LYRICS_CHANNEL_ID)
        await channel.send(embed=embed)
        await interaction.response.send_message("✅ twe bwututh divaish eiz koneiktideeee saiksesfeli!", ephemeral=True)

class GenrePickerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.selected_genre = None

        options = [
            discord.SelectOption(label=label, value=key)
            for key, label in GENRES.items()
        ]

        self.genre_dropdown = discord.ui.Select(
            placeholder="Pick me or Ruby..?",
            options=options,
            min_values=1,
            max_values=1
        )
        self.genre_dropdown.callback = self.genre_selected
        self.add_item(self.genre_dropdown)

        self.start_button = discord.ui.Button(label="✍️ Start with Bismillah", style=discord.ButtonStyle.primary)
        self.start_button.callback = self.start_writing
        self.add_item(self.start_button)

    async def genre_selected(self, interaction: discord.Interaction):
        self.selected_genre = self.genre_dropdown.values[0]
        await interaction.response.edit_message(view=self)

    async def start_writing(self, interaction: discord.Interaction):
        if not self.selected_genre:
            await interaction.response.send_message("❗Why not choosing genre? are you ghey?", ephemeral=True)
            return
        await interaction.response.send_modal(LyricsModal(self.selected_genre))

@bot.tree.command(name="writelyrics", description="Write lyrics with a genre tag")
async def writelyrics(interaction: discord.Interaction):
    await interaction.response.send_message("🎧 Choose your fighter, then click to begin:", view=GenrePickerView(), ephemeral=True)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")
    print(f"🤖 Logged in as {bot.user}")

bot.run(TOKEN)

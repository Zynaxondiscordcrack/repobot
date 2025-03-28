import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio

# Hilfsfunktion zur Erstellung eines Balkendiagramms
def create_bar(percentage, length=20):
    filled_length = int(round(length * percentage / 100))
    bar = "█" * filled_length + "░" * (length - filled_length)
    return bar

# PollView zur Speicherung der Umfrage-Daten
class PollView(discord.ui.View):
    def __init__(self, events):
        super().__init__(timeout=None)
        self.events = events  # Liste der Events für diese Abstimmung
        self.votes = {event: 0 for event in events}  # Stimmen-Tracker
        self.add_item(EventSelect(events, self))  # Dropdown-Menü hinzufügen

    def total_votes(self):
        return sum(self.votes.values())

    def generate_results(self):
        total = self.total_votes()
        result_text = ""
        for event, count in self.votes.items():
            percent = (count / total * 100) if total > 0 else 0
            bar = create_bar(percent)
            result_text += f"**{event}**\n{bar} {percent:.1f}% ({count} Stimmen)\n\n"
        return result_text

# Dropdown-Menü für Event-Auswahl
class EventSelect(discord.ui.Select):
    def __init__(self, events, view: PollView):
        options = [discord.SelectOption(label=event[:100], value=event) for event in events]
        self.poll_view = view
        super().__init__(placeholder="Wähle ein Event aus!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        chosen = self.values[0]
        self.poll_view.votes[chosen] += 1  # Stimme erhöhen

        # Neues Embed mit aktualisierten Ergebnissen
        embed = discord.Embed(
            title="💛 Community Event Vorschläge 💛",
            description="Hier sind einige Event-Ideen für unseren Server!\n\n"
                        "Stimme ab und schau, was aktuell am weitesten liegt:",
            color=discord.Color.gold()
        )

        for event in self.poll_view.events:
            embed.add_field(name="✨", value=f"**{event}**", inline=False)

        embed.add_field(name="📊 Aktuelle Abstimmungsergebnisse:", value=self.poll_view.generate_results(), inline=False)
        embed.set_footer(text="welches event gefällt euch am besten")

        await interaction.response.edit_message(embed=embed, view=self.poll_view)

# Bot-Setup
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# Liste mit 200 einzigartigen Events
event_list = [
    "🎮 **Gaming Turnier** – Trete in deinem Lieblingsspiel gegen andere an!",
    "🎤 **Karaoke Abend** – Singe deine Lieblingssongs mit der Community!",
    "🎲 **Brettspiel Nacht** – Spiele klassische oder digitale Brettspiele!",
    "🖌️ **Kunst-Wettbewerb** – Teile deine kreativen Zeichnungen!",
    "📢 **Q&A mit den Admins** – Stelle deine Fragen direkt an das Team!",
    "🎬 **Filmabend** – Gemeinsam schauen wir einen Film und kommentieren!",
    "🎵 **Musik-Quiz** – Erkenne Songs schneller als alle anderen!",
    "💬 **Community-Talk** – Diskutiere interessante Themen mit uns!",
    "🏆 **Meme-Wettbewerb** – Wer macht das beste Meme?",
    "📚 **Lesestunde** – Lies mit uns spannende Bücher oder Gedichte!",
    "🎭 **Impro-Theater** – Spiele improvisierte Szenen mit anderen!",
    "🎉 **Überraschungsevent** – Sei gespannt, was passiert!",
    "👾 **Retro-Gaming Abend** – Zocke alte Klassiker mit uns!",
    "🎨 **Live-Zeichnen** – Zeichne live und lass dich inspirieren!",
    "🕵️ **Escape Room Event** – Löse Rätsel und entkomme!",
    "🏹 **Minecraft Hunger Games** – Überlebe als Letzter!",
    "🎮 **Speedrun Challenge** – Wer ist am schnellsten?",
    "📷 **Fotografie-Wettbewerb** – Zeige deine besten Schnappschüsse!",
    "🏅 **Discord-Awards** – Stimme für die coolsten Mitglieder ab!",
    "🎲 **Dungeons & Dragons Runde** – Spiele eine spannende DnD-Kampagne!",
    "🎶 **Songwriting Contest** – Schreibe und präsentiere einen Song!",
    "🚀 **Sci-Fi Quiz** – Teste dein Wissen über Science-Fiction!",
    "🌍 **GeoGuessr Battle** – Finde heraus, wo auf der Welt du bist!",
    "📀 **Nostalgie-Nacht** – Lass uns über die Kindheit quatschen!",
    "🎯 **Skribbl.io Abend** – Wer errät die meisten Begriffe?",
    "👑 **King of the Hill Challenge** – Bleib am längsten an der Spitze!",
    "📝 **Schreibwettbewerb** – Erstelle eine kreative Geschichte!",
    "🎼 **Karaoke mit Bewertung** – Werde der Karaoke-Champion!",
    "💡 **Ideenworkshop für den Server** – Bringe neue Vorschläge ein!",
    "🎲 **Werwolf-Spiel** – Lüfte das Geheimnis: Wer ist der Werwolf?",
    "🔍 **Detektiv-Abend** – Löse knifflige Fälle mit anderen!",
    "💰 **Wirtschafts-Simulator** – Baue dein eigenes Business auf!",
    "🌌 **Sternenhimmel-Nacht** – Lerne mehr über Astronomie!",
    "🎮 **Pokémon Showdown Turnier** – Werde der beste Trainer!",
    "🧩 **Rätsel-Marathon** – Knacke die schwierigsten Denksport-Aufgaben!",
    "🏆 **Speed-Quiz** – Wer kann die meisten Fragen in 5 Minuten lösen?",
    "🎭 **Verkleidungstag** – Ziehe dein bestes Cosplay an!",
    "📺 **Anime-Marathon** – Schaue mit uns die besten Anime-Serien!",
    "📖 **Märchenstunde** – Erzähle oder höre dir tolle Geschichten an!",
    "🎹 **Instrumenten-Showcase** – Spiele dein Lieblingsinstrument!",
    "⚔️ **Mittelalter-Rollenspielabend** – Lebe wie ein Ritter oder Magier!",
    "🖍️ **Pixel-Art-Wettbewerb** – Erstelle pixelige Kunstwerke!",
    "🎧 **Podcast-Aufnahme** – Mache mit bei einem Community-Podcast!",
    "🚴 **Fitness-Challenge** – Wer bleibt am längsten aktiv?",
    "🎮 **Jackbox Party Night** – Spiele die besten Party-Games!",
    "🛠 **DIY & Bastelabend** – Teile deine kreativen Projekte!",
    "🎵 **Lieder erraten** – Errate Songs aus nur einer Sekunde Ton!",
    "💑 **Blind Date Event** – Lerne zufällige Mitglieder kennen!",
    "🔬 **Wissenschaftsquiz** – Teste dein Wissen über Physik & Chemie!",
    "🍳 **Koch-Show** – Teile Rezepte und koche gemeinsam!",
    "💰 **Investitions-Spiel** – Wer wird der reichste Händler?",
    "🏁 **Mario Kart Turnier** – Fahre gegen andere und werde Erster!",
    "🎶 **Musikproduktion 101** – Lerne, eigene Songs zu erstellen!",
    "👀 **True Crime Nacht** – Diskutiere echte Kriminalfälle!",
    "👗 **Fashion Contest** – Wer hat das beste Outfit?",
    "📅 **Throwback-Event** – Erinnere dich an alte Community-Momente!",
    "🕹 **Speedrunning-Wettkampf** – Wer schlägt das Spiel am schnellsten?",
    "🎲 **Pictionary Wettbewerb** – Zeichne und errate Begriffe!",
    "🧙 **Magischer Abend** – Lerne Zaubertricks & Magie!",
    "🚗 **GTA-Rennen** – Wer ist der beste Fahrer?",
    "🏀 **Sport-Quiz** – Teste dein Wissen über Fußball, Basketball & mehr!",
    "🔠 **Buchstabensalat** – Wer kann die meisten Wörter bilden?",
    "🎤 **Freestyle Rap Battle** – Wer kann am besten reimen?",
    "🤹 **Talent-Show** – Zeige dein einzigartiges Talent!",
    "🌍 **Sprachen-Challenge** – Lerne Wörter in neuen Sprachen!",
    "🤖 **KI-Kunst-Wettbewerb** – Wer macht das kreativste Bild mit AI?",
    "🎭 **Schauspiel-Wettbewerb** – Wer kann am besten improvisieren?",
    "📈 **Aktienmarkt-Simulator** – Wer wird der beste Investor?",
    "🕰 **Zeitreise-Quiz** – Teste dein Wissen über die Geschichte!",
    "🎤 **Stand-up Comedy Abend** – Bringe die Community zum Lachen!",
    "👾 **Indie-Gaming Showcase** – Teile deine Lieblings-Indie-Spiele!",
    "📣 **Motivations-Reden** – Inspiriere andere mit deinen Worten!",
    "💃 **Tanz-Wettbewerb** – Zeige deine besten Moves!",
    "🎧 **ASMR & Entspannungsabend** – Genieße beruhigende Klänge!",
    "🔨 **Minecraft-Bau-Challenge** – Wer baut das beste Gebäude?",
    "🎵 **Musik-Wunschkonzert** – Deine Lieblingssongs auf Discord!",
    "🌱 **Nachhaltigkeits-Workshop** – Wie können wir die Welt verbessern?",
    "🏰 **Disney-Abend** – Schaue & rate Disney-Filme!",
    "🏂 **Winter-Sport-Event** – Virtuelle Skirennen & Snowboard-Challenges!",
    "🦉 **Harry Potter Trivia** – Wer weiß am meisten über Hogwarts?",
    "🎵 **80er/90er Party** – Reise zurück in die coolste Musik-Zeit!",
    "🎮 **Gaming-Themenabend** – Ein ganzes Event zu deinem Lieblingsspiel!",
    "🤯 **Verrückte Challenge** – Sei mutig und mach mit!",
]


@bot.tree.command(name="event", description="Zeigt 5 zufällige Event-Vorschläge mit Dropdown und Voting an")
async def event(interaction: discord.Interaction):
    # Verzögere die Antwort, um später eine Nachricht zu senden
    await interaction.response.defer()

    # Sende eine Nachricht im Chat, dass die KI arbeitet
    working_message = await interaction.followup.send(
        "⏳ **Die KI ist am Arbeiten...**\nEs kann einige Sekunden dauern.")

    await asyncio.sleep(5)  # Wartezeit von 5 Sekunden

    selected_events = random.sample(event_list, 5)

    embed = discord.Embed(
        title="💛 Community Event Vorschläge 💛",
        description="Hier sind einige Event-Ideen für unseren Server!\n\nStimme ab und schau, was aktuell am weitesten liegt:",
        color=discord.Color.gold()
    )

    for event in selected_events:
        embed.add_field(name="✨", value=f"**{event}**", inline=False)

    embed.add_field(name="📊 Aktuelle Abstimmungsergebnisse:", value="Noch keine Stimmen abgegeben.", inline=False)
    embed.set_footer(text="Stimmt im Team ab P.S Jorgo ist Ein komischer Grieche")

    view = PollView(selected_events)

    # Bearbeite die ursprüngliche Nachricht, um das Event-Embed zu ersetzen
    await working_message.edit(content=None, embed=embed, view=view)

bot.run('MTM1MjczOTE1MzMwMDgyMDA1Mw.GwvcjX.i65HQt27mVtabKXIkS4iM4Or9QDnlgAg4wB6JM')

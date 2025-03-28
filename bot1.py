import discord
from discord.ext import commands
from discord.ui import View, Select
from discord import app_commands


# Bot Setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Channel und Rollen-IDs
MODERATOR_ROLE_ID = 1346466917707288627
ADMIN_ROLE_ID = 1345789304131031110

# /weiterleitung Command
@bot.tree.command(name="weiterleitung", description="Leitet das Ticket an den Moderator oder Administrator weiter")
async def weiterleitung(interaction: discord.Interaction):
    # Channel, wo der Command ausgeführt wird
    channel = interaction.channel

    # Dropdown mit Auswahlmöglichkeiten für Moderator oder Administrator
    select = Select(
        placeholder="Wähle den Empfänger der Weiterleitung",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Moderator", value="moderator"),
            discord.SelectOption(label="Administrator", value="administrator")
        ]
    )

    # Callback Funktion
    async def select_callback(interaction: discord.Interaction):
        selected_value = select.values[0]

        if selected_value == "moderator":
            role = interaction.guild.get_role(MODERATOR_ROLE_ID)
            mentioned_role = "<@&1346466917707288627>"  # Ping the moderator role
        elif selected_value == "administrator":
            role = interaction.guild.get_role(ADMIN_ROLE_ID)
            mentioned_role = "<@&1345789304131031110>"  # Ping the admin role
        
        # Nachrichten an den Ticket-Channel
        await channel.send(f"**WEITERLEITUNG**\n"
                           f"weiterleitung an: {mentioned_role}\n"
                           f"Das Ticket darf nurnoch von der {role.name} Beschrieben werden.")

        # Berechtigungen anpassen: Nur die moderierenden Rollen dürfen schreiben
        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = True  # Moderatoren oder Administratoren dürfen schreiben

        # Entziehe anderen Benutzern die Schreibrechte
        for member in interaction.guild.members:
            if not any(role.id == MODERATOR_ROLE_ID or role.id == ADMIN_ROLE_ID for role in member.roles):
                overwrite = channel.overwrites_for(member)
                overwrite.send_messages = False

        # Berechtigungen aktualisieren
        await channel.set_permissions(role, overwrite=overwrite)

        # Feedback an den Benutzer, dass der Vorgang abgeschlossen ist
        await interaction.response.send_message(f"Das Ticket wurde erfolgreich an {mentioned_role} weitergeleitet.")

    # Hinzufügen der Callback-Funktion zur Auswahl
    select.callback = select_callback

    # View zum Senden der Auswahl
    view = View()
    view.add_item(select)

    # Erste Nachricht zur Auswahl
    await interaction.response.send_message("Bitte wähle den Empfänger der Weiterleitung:", view=view)
    
    bot.run('MTM1MjczOTE1MzMwMDgyMDA1Mw.GwvcjX.i65HQt27mVtabKXIkS4iM4Or9QDnlgAg4wB6JM')

# Discord Bot - Work in Progress
# Placeholder for bot code
import discord
from discord import app_commands
import re
import os

TOKEN = "MTU0MzczMDMyODUzNzkzMTc3Ng.GQ76-J.yPLhS0Rb4jBAfnZR4I_2bp8RoP6cLEg0Rn1r40"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


class AddModal(discord.ui.Modal, title="Ajouter des informations"):

    infos = discord.ui.TextInput(
        label="Informations",
        style=discord.TextStyle.paragraph,
        placeholder=(
            "n:Dupont\n"
            "p:Damien\n"
            "a:15\n"
            "v:Paris\n"
            "25/03/2010"
        ),
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):

        texte = self.infos.value
        resultat = []

        for ligne in texte.splitlines():
            ligne = ligne.strip()

            if not ligne:
                continue

            # Nom
            if ligne.lower().startswith("n:"):
                valeur = ligne[2:].strip()
                resultat.append(f"**Nom :** {valeur}")

                        # Prénom
            elif ligne.lower().startswith("p:"):
                valeur = ligne[2:].strip()
                resultat.append(f"**Prénom :** {valeur}")

            # Âge
            elif ligne.lower().startswith("a:"):
                valeur = ligne[2:].strip()
                resultat.append(f"**Âge :** {valeur}")

            # Ville
            elif ligne.lower().startswith("v:"):
                valeur = ligne[2:].strip()
                resultat.append(f"**Ville :** {valeur}")

            # Date complète : 25/03/2010
            elif re.fullmatch(r"\d{2}/\d{2}/\d{4}", ligne):
                resultat.append(f"**Date de naissance :** {ligne}")

            # Seulement année : 2010
            elif re.fullmatch(r"\d{4}", ligne):
                resultat.append(f"**Année de naissance :** {ligne}")

            else:
                resultat.append(f"❓ **Inconnu :** {ligne}")

        await interaction.response.send_message(
            "\n".join(resultat),
            ephemeral=True
        )


@tree.command(
    name="add",
    description="Ajouter des informations"
)
async def add(interaction: discord.Interaction):

    await interaction.response.send_modal(AddModal())


@client.event
async def on_ready():

    try:
        await tree.sync()
        print(f"Bot connecté : {client.user}")
        print("Commande /add synchronisée !")

    except Exception as e:
        print(e)


client.run(TOKEN)

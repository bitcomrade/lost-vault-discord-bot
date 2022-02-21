# type: ignore
from typing import List

import nextcord
from nextcord.ext import commands

import process_data

TRIBES = process_data.TRIBE_NAME_ID


class ApplicationCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="vs", description="поиск цели для гвг / find opponents for gvg"
    )
    async def find_opponents(
        self,
        interaction: nextcord.Interaction,
        tribe: str = nextcord.SlashOption(
            name="tribe", description="название племени / tribe name"
        ),
    ) -> str:
        await interaction.response.send_message(process_data.get_vs(tribe))

    @find_opponents.on_autocomplete("tribe")
    async def fill_tribe_id_1(
        self, interaction: nextcord.Interaction, tribe: str
    ) -> List[str]:
        if not tribe:
            # send the full autocomplete list
            await interaction.response.send_autocomplete(TRIBES)
            return
        get_near_tribe = [
            name for name in TRIBES if name.startswith(tribe.lower())
        ]
        await interaction.response.send_autocomplete(get_near_tribe)

    @nextcord.slash_command(
        name="hello", description="приветствие / greetings"
    )
    async def send_hello_msg(self, interaction: nextcord.Interaction):
        """Replies to hello message with basic information"""
        await interaction.response.send_message(
            process_data.msg.hello_message()
        )

    @nextcord.slash_command(name="seekhelp", description="помощь / help")
    async def send_help_msg(self, interaction: nextcord.Interaction):
        """Replies with basic instructions and commands"""
        await interaction.response.send_message(
            process_data.msg.help_message()
        )

    @nextcord.slash_command(
        name="player", description="информация об игроке / player info"
    )
    async def send_player_info(
        self, interaction: nextcord.Interaction, player: str
    ):
        """
        Send player information from the API server to the channel
        """
        await interaction.response.send_message(
            process_data.player_info(player)
        )

    @nextcord.slash_command(
        name="tribe", description="информация о племени / tribe info"
    )
    async def send_tribe_info(
        self,
        interaction: nextcord.Interaction,
        tribe: str = nextcord.SlashOption(
            name="tribe", description="название племени / tribe name"
        ),
    ):
        """
        Send tribe information from the API server to the channel
        """
        await interaction.response.send_message(process_data.tribe_info(tribe))

    @send_tribe_info.on_autocomplete("tribe")
    async def fill_tribe_id_2(
        self, interaction: nextcord.Interaction, tribe: str
    ):
        if not tribe:
            # send the full autocomplete list
            await interaction.response.send_autocomplete(TRIBES)
            return
        get_near_tribe = [
            name for name in TRIBES if name.startswith(tribe.lower())
        ]
        await interaction.response.send_autocomplete(get_near_tribe)

    @nextcord.slash_command(
        name="players", description="сравнение игроков / compare players"
    )
    async def compare_player_info(
        self, interaction: nextcord.Interaction, player_1: str, player_2: str
    ):
        """
        Compare two players with higlighted differences
        """
        await interaction.response.send_message(
            process_data.compare_slash("players", player_1, player_2)
        )

    @nextcord.slash_command(
        name="tribes", description="сравнение племен / compare tribes"
    )
    async def compare_tribe_info(
        self,
        interaction: nextcord.Interaction,
        tribe_1: str = nextcord.SlashOption(
            name="tribe_1", description="племя 1 / tribe 1 name"
        ),
        tribe_2: str = nextcord.SlashOption(
            name="tribe_2", description="племя 2 / tribe 2 name"
        ),
    ):
        """
        Compare two tribes with higlighted differences
        """
        await interaction.response.send_message(
            process_data.compare_slash("guilds", tribe_1, tribe_2)
        )

    @compare_tribe_info.on_autocomplete("tribe_1")
    async def fill_tribe_id_3(
        self, interaction: nextcord.Interaction, tribe: str
    ):
        if not tribe:
            # send the full autocomplete list
            await interaction.response.send_autocomplete(TRIBES)
            return
        get_near_tribe = [
            name for name in TRIBES if name.startswith(tribe.lower())
        ]
        await interaction.response.send_autocomplete(get_near_tribe)

    @compare_tribe_info.on_autocomplete("tribe_2")
    async def fill_tribe_id_4(
        self, interaction: nextcord.Interaction, tribe: str
    ):
        if not tribe:
            # send the full autocomplete list
            await interaction.response.send_autocomplete(TRIBES)
            return
        get_near_tribe = [
            name for name in TRIBES if name.startswith(tribe.lower())
        ]
        await interaction.response.send_autocomplete(get_near_tribe)


def setup(bot):
    bot.add_cog(ApplicationCommandCog(bot))

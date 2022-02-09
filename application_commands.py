import nextcord
from nextcord.ext import commands
import process_data


TESTING_GUILD_ID = 937037847725236286
TRIBES = process_data.TRIBE_NAME_ID


class ApplicationCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @nextcord.slash_command(
        name='dbupdate', 
        description='force update db',
        guild_ids=[TESTING_GUILD_ID]
        )
    @commands.is_owner()
    async def force_db_update(self, interaction: nextcord.Interaction):
        await process_data.update_db()
        await interaction.response.send_message(
            "started db update"
            )
    
    @nextcord.slash_command(
        name='vs', 
        description = 'find worthy opponents for gvg', 
        guild_ids=[TESTING_GUILD_ID]
        )
    async def find_opponents(
        self, interaction: nextcord.Interaction, 
        tribe: str = nextcord.SlashOption(
            name="tribe",
            description="tribe name"
            )
        ):
        await interaction.response.send_message(process_data.get_vs(tribe))

    @find_opponents.on_autocomplete("tribe")
    async def fill_tribe_id(
        self, 
        interaction: nextcord.Interaction, 
        tribe: str
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
        name='language',
        description = 'change language', 
        guild_ids=[TESTING_GUILD_ID]
        )
    @commands.is_owner()
    async def set_language(
        self, interaction: nextcord.Interaction,
        lang: str = nextcord.SlashOption(
            name="language",
            description="choose language",
            choices={"English":"en", "Russian":"ru"}
            )
        ):
        process_data.msg.messages = process_data.msg.get_message_list(lang)
        await interaction.response.send_message(
            process_data.msg.hello_message()
            )

    @nextcord.slash_command(
        name="hello",
        description="sends hello message",
        guild_ids=[TESTING_GUILD_ID]
        )
    async def send_hello_msg(self, interaction: nextcord.Interaction):
        """Replies to hello message with basic information"""
        await interaction.response.send_message(
            process_data.msg.hello_message()
            )    
      
    @nextcord.slash_command(
        name="seekhelp",
        description="sends help message",
        guild_ids=[TESTING_GUILD_ID]
        )
    async def send_help_msg(self, interaction: nextcord.Interaction):
        """Replies with basic instructions and commands"""
        await interaction.response.send_message(
            process_data.msg.help_message()
            )

    @nextcord.slash_command(
        name="player",
        description="find player info",
        guild_ids=[TESTING_GUILD_ID]
        )
    async def send_player_info(
        self, interaction: nextcord.Interaction, 
        player: str
        ):
        """
        Send player information from the API server to the channel
        """ 
        await interaction.response.send_message(
            process_data.player_info(player)
            )
    
    @nextcord.slash_command(
        name="tribe",
        description="find tribe info",
        guild_ids=[TESTING_GUILD_ID]
        )
    async def send_tribe_info(
        self, interaction: nextcord.Interaction, 
        tribe: str = nextcord.SlashOption(
            name="tribe", description="name of the tribe"
            )
        ):
        """
        Send tribe information from the API server to the channel
        """
        await interaction.response.send_message(
            process_data.tribe_info(tribe)
            )    
          
    @send_tribe_info.on_autocomplete("tribe")
    async def fill_tribe_id(
        self, 
        interaction: nextcord.Interaction, 
        tribe: str
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
        name="players",
        description="compare two players",
        guild_ids=[TESTING_GUILD_ID]
        )
    async def compare_player_info(
        self, interaction: nextcord.Interaction, 
        player_1: str,
        player_2: str
        ):
        """
        Compare two players with higlighted differences
        """
        await interaction.response.send_message(
            process_data.compare_slash('players',player_1,player_2)
            )      

    @nextcord.slash_command(
        name="tribes",
        description="compare two tribes",
        guild_ids=[TESTING_GUILD_ID]
        )
    async def compare_tribe_info(
        self, interaction: nextcord.Interaction, 
        tribe_1: str = nextcord.SlashOption(
            name="tribe_1", description="tribe #1 name"
            ),
        tribe_2: str = nextcord.SlashOption(
            name="tribe_2", description="tribe #2 name"
            )
        ):
        """
        Compare two tribes with higlighted differences
        """
        await interaction.response.send_message(
            process_data.compare_slash('guilds',tribe_1,tribe_2)
            )      

    @compare_tribe_info.on_autocomplete("tribe_1")
    async def fill_tribe_id(
        self, 
        interaction: nextcord.Interaction, 
        tribe: str
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
    async def fill_tribe_id(
        self, 
        interaction: nextcord.Interaction, 
        tribe: str
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
import time
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import process_data

class BasicCommmands(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    @commands.cooldown(rate=1,per=3)
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()
        await message.edit(content=
                           (f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: "
                            f"{round((end_time - start_time) * 1000)}ms")
                           )
               
    @commands.command(name="hello")
    async def send_hello_msg(self, ctx: commands.Context):
        """Replies to hello message with basic information"""
        await ctx.send(process_data.hello_message())    
      
    @commands.command(name="seekhelp")
    async def send_help_msg(self, ctx: commands.Context):
        """Replies with basic instructions and commands"""
        await ctx.send(process_data.help_message())
        
    @commands.command(name="player")
    async def send_player_info(self, ctx: commands.Context, *, text: str):
        """Send player information from the API server to the channel

        Args:
            ctx (commands.Context): player name after !seekplayer command
            text (str): typehinting as string
        """ 
        await ctx.send(process_data.player_info(text))
    
    @commands.command(name="tribe")
    async def send_tribe_info(self, ctx: commands.Context, *, text: str):
        """Send tribe information from the API server to the channel

        Args:
            ctx (commands.Context): tribe name after !seektribe command
            text (str): typehinting as string
        """
        await ctx.send(process_data.tribe_info(text))      

    @commands.command(name="players")
    async def compare_player_info(self, ctx: commands.Context, *, text: str):
        """
        Compare two players with higlighted differences
        """
        await ctx.send(process_data.compare('players',text))      

    @commands.command(name="tribes")
    async def compare_tribe_info(self, ctx: commands.Context, *, text: str):
        """
        Compare two tribes with higlighted differences
        """
        await ctx.send(process_data.compare('guilds',text))      
    
    
def setup(bot: commands.Bot):
    bot.add_cog(BasicCommmands(bot))        
# type: ignore
import asyncio
import datetime

import nextcord
from nextcord.ext import commands

import process_data as data

GUILD_IDS = [395543532997181440, 906567855905062922]
SERVICE_ROLE = "LV bot trustworthy"
ADMIN_ROLE = "LV bot admin"
MENTION = {
    "Dakar": {
        "slug": "dakar",
        "role": 899556122564911124,
        "channel": 943498537008762960,
    },
    "Инфектед Машрум": {
        "slug": "guild-5",
        "role": 913869261389316106,
        "channel": 943498537008762960,
    },
    "Eclipse": {
        "slug": "eclipse",
        "role": 906577291566522428,
        "channel": 906584942555836467,
    },
    "Eclipse Academy": {
        "slug": "eclipse-academy",
        "role": 906819171000647733,
        "channel": 906584942555836467,
    },
}
ALERTS = [
    data.msg.timer_start_msg(),
    data.msg.timer_advance_msg(),
    data.msg.timer_attack_msg(),
]


class Timer:
    def __init__(
        self, name: str, callback, timeout: int = 28740, advance: int = 300
    ) -> None:
        self.name = name
        self.timeout = timeout
        self._start = datetime.datetime.now()
        self.finish = self._end_time(self._start, self.timeout)
        self._timecodes = [1, timeout - advance, advance]
        self.stage = 0
        self._callback = callback
        self._task = asyncio.create_task(self._job())

    async def _job(self) -> None:
        while self.stage < 3:
            await asyncio.sleep(self._timecodes[self.stage])
            await self._callback(self)
            self.stage += 1

    def _end_time(
        self, start_time: datetime.datetime, timeout: int
    ) -> datetime.datetime:
        timedelta = datetime.timedelta(seconds=+timeout)
        end_time = start_time + timedelta
        return end_time

    def cancel(self) -> None:
        self._task.cancel()

    def time_left(self) -> datetime.timedelta:
        current = datetime.datetime.now()
        if current >= self.finish:
            return datetime.timedelta
        else:
            return self.finish - current


class AttackTimer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timers = dict()

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(943549056972632065)
        await channel.send("checking for timers...")
        old_timers = data.get_timer_set_time()
        await channel.send("timers found")
        await channel.send("setting up timers...")
        for name, time in old_timers.items():
            if time:
                timer = Timer(name, self.notifications, timeout=time)
                self.timers[name] = timer
                await channel.send(f"set timer for {name} for {time} seconds")

    @nextcord.slash_command(
        name="gvg",
        description="таймер для гвг / sets timer for gvg",
        guild_ids=GUILD_IDS,
    )
    async def set_timer(
        self,
        interaction: nextcord.Interaction,
        tribe: str = nextcord.SlashOption(
            required=True,
            name="tribe",
            description="выберите племя / choose tribe",
            choices=["Dakar", "Eclipse", "Инфектед Машрум", "Eclipse Academy"],
        ),
    ):
        channel = self.bot.get_channel(MENTION[tribe]["channel"])
        if tribe not in self.timers:
            timer = Timer(tribe, self.notifications)
            self.timers[tribe] = timer
            await interaction.response.defer(
                ephemeral=True, with_message=False
            )
            data.write_timer_set_time(tribe, timer.timeout)
            await channel.send(data.msg.timer_new_msg().format(tribe))
        else:
            next_attack = self.timers[tribe].time_left()
            time_left = ":".join(str(next_attack).split(":")[:2])
            await interaction.response.defer(
                ephemeral=True, with_message=False
            )
            await channel.send(
                data.msg.time_left_msg().format(tribe, time_left)
            )

    @nextcord.slash_command(
        name="timers",
        description="список активных таймеров / active timers list",
        guild_ids=GUILD_IDS,
    )
    async def timers_list(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=False)
        for timer in self.timers.values():
            name = timer.name
            time_left = ":".join(str(timer.time_left()).split(":")[:2])
            channel = self.bot.get_channel(MENTION[name]["channel"])
            await channel.send(f"{name}: {time_left}")

    @nextcord.slash_command(
        name="change_timer",
        description="изменить таймер для гвг / change timer for gvg",
        guild_ids=GUILD_IDS,
    )
    async def change_timer(
        self,
        interaction: nextcord.Interaction,
        time: str,
        tribe: str = nextcord.SlashOption(
            required=True,
            name="tribe",
            description="выберите племя / choose tribe",
            choices=["Dakar", "Eclipse", "Инфектед Машрум", "Eclipse Academy"],
        ),
    ):
        if tribe not in self.timers:
            timer = Timer(tribe, self.notifications)
            self.timers[tribe] = timer
            obj = self.timers[tribe]
            secs_left = obj.timeout
        else:
            hours, minutes = (int(numbers) for numbers in time.split(":"))
            secs_left = (hours * 60 + minutes) * 60
            self.timers[tribe].cancel()
            timer = Timer(tribe, self.notifications, secs_left)
            self.timers[tribe] = timer
        data.write_timer_set_time(tribe, secs_left)
        await interaction.response.defer(ephemeral=True, with_message=False)

    async def notifications(self, timer: Timer) -> None:
        channel = self.bot.get_channel(MENTION[timer.name]["channel"])
        message = ALERTS[timer.stage]
        timedelta = timer.time_left()
        str_timedelta = ":".join(str(timedelta).split(":")[:2])
        output = message.format(timer.name, str_timedelta)
        await channel.send(output)
        if timer.stage == 2:
            role = MENTION[timer.name]["role"]
            await channel.send(f"<@&{role}>")
            await channel.send(data.get_vs(MENTION[timer.name]["slug"]))
            self.timers[timer.name].cancel()
            self.timers.pop(timer.name, None)


def setup(bot):
    bot.add_cog(AttackTimer(bot))

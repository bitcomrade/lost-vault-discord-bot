# type: ignore
import asyncio
import datetime

import nextcord
from nextcord.ext import commands

import process_data as data

SERVICE_ROLE = "LV bot trustworthy"
ADMIN_ROLE = "LV bot admin"
MENTION_ROLE = 899556122564911124
CHANNEL = 943498537008762960
ALERTS = [
    data.msg.timer_start_msg(),
    data.msg.timer_advance_msg(),
    data.msg.timer_attack_msg(),
]


class Timer:
    def __init__(
        self, name: str, callback, timeout: int = 28800, advance: int = 3600
    ) -> None:
        self.name = name
        self._timeout = timeout
        self._start = datetime.datetime.now()
        self.finish = self._end_time(self._start, self._timeout)
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
        self.channel = self.bot.get_channel(CHANNEL)

    @nextcord.slash_command(
        name="gvg", description="напоминалка для гвг / sets timer for gvg"
    )
    async def set_timer(
        self,
        interaction: nextcord.Interaction,
        tribe: str = nextcord.SlashOption(
            required=True,
            name="tribe",
            description="выберите племя / choose tribe",
            choices=["Dakar", "Инфектед Машрум"],
        ),
    ):
        channel = self.bot.get_channel(CHANNEL)
        if tribe not in self.timers:
            timer = Timer(tribe, self.notifications, 28800, 3600)
            self.timers[tribe] = timer
            await interaction.response.defer(
                ephemeral=True, with_message=False
            )
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
    )
    async def timers_list(self, interaction: nextcord.Interaction):
        channel = self.bot.get_channel(CHANNEL)
        await interaction.response.defer(ephemeral=True, with_message=False)
        for timer in self.timers.values():
            name = timer.name
            time_left = ":".join(str(timer.time_left()).split(":")[:2])
            await channel.send(f"{name}: {time_left}")

    @commands.command(name="gvgreset")
    @commands.has_any_role(SERVICE_ROLE, ADMIN_ROLE)
    async def force_set_timer(self, ctx: commands.Context, *, text: str):
        tribe, str_time = text.split(" == ")
        hours, minutes = (int(numbers) for numbers in str_time.split(":"))
        force_secs_left = (hours * 60 + minutes) * 60
        self.timers[tribe].cancel()
        timer = Timer(tribe, self.notifications, force_secs_left, 60)
        self.timers[tribe] = timer

    async def notifications(self, timer: Timer) -> None:
        channel = self.bot.get_channel(CHANNEL)
        message = ALERTS[timer.stage]
        timedelta = timer.time_left()
        str_timedelta = ":".join(str(timedelta).split(":")[:2])
        output = message.format(MENTION_ROLE, timer.name, str_timedelta)
        await channel.send(output)
        if timer.stage == 2:
            self.timers[timer.name].cancel()
            self.timers.pop(timer.name, None)


def setup(bot):
    bot.add_cog(AttackTimer(bot))

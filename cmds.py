import discord
from discord.ext.commands import command, check


def is_owner(ctx):
    return ctx.message.author.id == ctx.bot.owner


class CreationDate:
    def __init__(self, bot, config):
        self._bot = bot

        self.roles = config['roles']

    @property
    def bot(self):
        return self._bot

    async def _add_role(self, member):
        server = member.server

        bot_member = server.get_member(self.bot.user.id)
        perms = bot_member.server_permissions

        # If bot doesn't have manage roles no use in trying to add roles
        if not perms.administrator and not perms.manage_roles:
            return

        year = member.created_at.year
        role_id = str(self.roles.get(str(year)))
        role = discord.utils.find(lambda r: r.id == role_id, server.roles)
        if not role:
            print('Role with id {} not found'.format(role_id))
            return

        has_role = role in member.roles
        if has_role:
            return

        await self.bot.add_role(member, role)
        print('Added role {0.name} to {1}'.format(role, member))

    async def on_member_join(self, member):
        await self._add_role(member)

    @command(pass_context=True, ignore_extra=True, aliases=['add_roles'])
    @check(is_owner)
    async def give_missing_roles(self, ctx):
        """Adds roles based on account creation date to all members who don't have it"""
        server = ctx.message.server
        await self.bot.request_offline_members(server)
        members = list(server.members)
        for member in members:
            await self._add_role(member)


def setup(bot):
    bot.add_cog(CreationDate(bot, bot.config))

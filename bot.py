from discord.ext.commands import Bot


class BaseBot(Bot):
    def __init__(self, config,  command_prefix, *args, **kwargs):
        super(BaseBot, self).__init__(command_prefix, *args, **kwargs)
        self.config = config
        self.owner = str(config['owner'])

    async def on_ready(self):
        self.load_extension('cmds')
        print('Logged in as {0} {0.id}'.format(self.user))

    async def add_role(self, user, role, server=None):
        if not isinstance(user, str):
            user_id = user.id
            server_id = user.server.id

        else:
            user_id = user
            server_id = server.id if not isinstance(server, str) else server

        role_id = role.id if not isinstance(role, str) else role

        await self.http.add_role(server_id, user_id, role_id)

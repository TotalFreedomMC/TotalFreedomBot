from discord.ext import commands


class NoPermission(commands.MissingPermissions):
    pass


class notAdminCommand(Exception):
    def __init__(self,
                 message="The command you attempted does not exist or is not a whitelisted command for the adminconsole."):
        self.message = message
        super().__init__(self.message)


def is_staff():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id in [ctx.bot.admin, ctx.bot.senior_admin]:
                return True
        else:
            raise NoPermission(['IS_STAFF_MEMBER'])

    return commands.check(predicate)


def is_dev():
    def predicate(ctx):
        user = ctx.message.author
        if user.id in ctx.bot.devs:
            return True
        else:
            raise NoPermission(['BOT_DEVELOPER'])

    return commands.check(predicate)


def is_mod_or_has_perms(**permissions):
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id in [ctx.bot.discord_mod, ctx.bot.discord_admin] or permissions and all(
                    getattr(ctx.channel.permissions_for(ctx.author), name, None) == value for name, value in
                    permissions.items()):
                return True
        else:
            raise NoPermission(['IS_MOD_OR_HAS_PERMS'])

    return commands.check(predicate)


def is_executive():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id in [ctx.bot.executive, ctx.bot.asst_exec]:
                return True
        else:
            raise NoPermission(['IS_EXECUTIVE'])

    return commands.check(predicate)


def is_tf_developer():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == ctx.bot.developer:
                return True
        else:
            raise NoPermission(['IS_TOTALFREEDOM_DEVELOPER'])

    return commands.check(predicate)


def is_liaison():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == ctx.bot.server_liaison:
                return True
        else:
            raise NoPermission(['IS_SERVER_LIAISON'])

    return commands.check(predicate)


def is_creative_designer():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == ctx.bot.creative_designer:
                return True
        else:
            raise NoPermission(['IS_CREATIVE_DESIGNER'])

    return commands.check(predicate)


def is_smp_owner():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == ctx.bot.smp_owner_id:
                return True
        else:
            raise NoPermission(['IS_GMOD_OWNER'])

    return commands.check(predicate)


def is_gmod_owner():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == ctx.bot.gmod_owner_id:
                return True
        else:
            raise NoPermission(['IS_GMOD_OWNER'])

    return commands.check(predicate)


def is_senior():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == ctx.bot.senior_admin:
                return True
        else:
            raise NoPermission(['IS_SENIOR_ADMIN'])

    return commands.check(predicate)

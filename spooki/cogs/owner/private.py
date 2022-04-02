import discord

from discord.ext import commands

from spooki.utils.subclasses import SpookiContext


class PriavteMixin:
    bears = {
        # Quest Bears
        'black': 'https://media.discordapp.net/attachments/954065413602418739/954065623988723752/amongusbear.png',
        'mother': 'https://cdn.discordapp.com/attachments/954065413602418739/954078523188990073/onedaytheyalldissapearedwithoutatrace.png',
        'brown': 'https://media.discordapp.net/attachments/954065413602418739/954485368231714856/iwilltakeyourheartandeatitalive.png?width=694&height=671',
        'panda': 'https://media.discordapp.net/attachments/954065413602418739/954499048587554896/nsfw.png?width=694&height=671',

        'science': 'https://cdn.discordapp.com/avatars/799690383352791071/5459037a3bd2a2d21d504953c5d71782.png?size=2048',
        'dapper': '',
        'polar': 'https://cdn.discordapp.com/avatars/799684568860196874/8836a4e0593d440fba14378c0fd9284d.png?size=2048****',
        'spirit': 'https://cdn.discordapp.com/avatars/799734340933255189/60b92197d1ac4411076f7e27558b18ab.png?size=2048',
        # Travelling Bears
        'sun': 'https://cdn.discordapp.com/avatars/799735250619990026/dc82626329963e9b2b4a8ef50011cbca.png?size=2048',
        'gummy': 'https://cdn.discordapp.com/avatars/799395007060639805/9533e0268bf7a22fec6f24c536582214.png?size=2048',
        'bee': 'https://cdn.discordapp.com/avatars/797481327879389264/dfbb905efbda28c43498adfd6b58bed9.png?size=2048',
        # Shop Bears
        'noob': 'https://cdn.discordapp.com/avatars/799606573617512469/079efa303ad7d9f2c84c854f62aa730e.png?size=2048',
        'pro': 'https://cdn.discordapp.com/avatars/799689546186227783/424c37fb9e1a3c08e76ce9beaef0546c.png?size=2048',
        'top': 'https://cdn.discordapp.com/avatars/799689901599752203/dd3251aa7d936005349ee3c251e7fbde.png?size=2048',
        # Other Bears
        'tunnel': 'https://cdn.discordapp.com/avatars/800064309525872641/d29cd4e3e7b318ecf4ef0e354064431a.png?size=2048',
        'shadow': 'https://cdn.discordapp.com/avatars/799733002355343430/754329158e382a5f882f98d946c3b0ad.png?size=2048',
        'snow': 'https://cdn.discordapp.com/avatars/800062918417711104/a4498bdc2bad9e7de173c3b555620e8a.png?size=2048'
    }

    async def send_webhook_message(self, message: discord.Message):
        bot = message._state._get_client()
        split = message.content.split("b!")

        if split[0] not in bears:
            return await message.reply(":x: That bear doesn't exist, sorry!")
        
        webhooks = await message.channel.webhooks()
        for webhook in webhooks:
            if split[0].lower() == webhook.name.lower():
                await webhook.send(split[1])
                await message.delete()
                continue

            webhook = await message.channel.create_webhook(name=split[0].title(),
                                                           avatar=await bot.http.get_from_cdn(bears[split[0]]))
    

@_bot.listen('on_message')
async def bears(message):
    if not message.guild: return
    if not message.guild.id == 796764299749490759: return
    if "b!" not in message.content.lower(): return

    split = message.content.split("b!")
    if split[0] in bears:
        webhooks = await message.channel.webhooks()
        for webhook in webhooks:
            if split[0].lower() == webhook.name.lower():
                await webhook.send(split[1])
                await message.delete()
                continue
            webhook = await message.channel.create_webhook(name=split[0].title(),
                                                    avatar=await _bot.http.get_from_cdn(bears[split[0]]),
                                                    reason="Roleplay")
            await webhook.send(split[1])
            await message.delete()
            continue
#importing all pip downloaded
import discord
from discord.ext import commands, tasks
import youtube_dl

from random import choice


#coding youtube_dl
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


#bot prefix
client = commands.Bot(command_prefix='=')

#setting status
status = ['a Song!', 'Prefix: \'=\'', 'Musify yourself!']

@client.event
async def on_ready():
    change_status.start()
    print("Bot is Online")


#command section
@client.command(name= 'ping', help='This command shows Latency' )
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(name= 'invite', help='Invite link of this Bot')
async def invite(ctx):
    await ctx.send(f'https://discord.com/api/oauth2/authorize?client_id=799861280701153280&permissions=37013568&scope=bot')

@client.command(name='credits', help='This command shows credits')
async def credits(ctx):
    await ctx.send(f'The Bot is devloped by a school student.'
                   f'If you get any problem please join our Server \"https://discord.gg/jCCUkBbccW\"')




@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


client.run('Bot Token')

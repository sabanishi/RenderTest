import discord
import os
from keep_alive import keep_alive

# 必要なintentsを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容にアクセスできるようにする

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

async def reply(message):
    reply = f'{message.author.mention} さん、こんにちは！'
    await message.channel.send(reply)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    if client.user in message.mentions:
        await reply(message)

# Botの起動とDiscordサーバーへの接続
TOKEN = os.getenv('DISCORD_TOKEN')
keep_alive()
client.run(TOKEN)
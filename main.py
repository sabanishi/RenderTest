import discord
import os
import requests
import json
from keep_alive import keep_alive

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/dispatches"


# 必要なintentsを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容にアクセスできるようにする

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = os.getenv('OWNER')
REPO = os.getenv('REPO')

# Webhookで受け取るイベントデータを取得する関数
def get_webhook_data():
    return {"event_type": "trigger-workflow", "client_payload": {"key": "value"}}

def trigger_github_action(owner,repo):
    print(owner)
    print(repo)
    url = GITHUB_API_URL.format(owner=owner, repo=repo)

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = get_webhook_data()

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 204:
        print("GitHub Action has been triggered.")
    else:
        print(f"Failed to trigger GitHub Action. Status code: {response.status_code}")
        print(response.text)

@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

async def reply(message):
    #メッセージ中に「Android」という文字列が含まれているかをチェックする
    if 'Android' in message.content:
        print('Androidが含まれています')
        await message.add_reaction('👍')

        #Android用のGitHub Actionをトリガーする
        trigger_github_action(OWNER, REPO)
    else:
        reply = "zZz..."
        await message.channel.send(reply)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    if client.user in message.mentions:
        await reply(message)


# Botの起動とDiscordサーバーへの接続
keep_alive()
client.run(DISCORD_TOKEN)
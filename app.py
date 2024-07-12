import discord
from discord.ext import commands
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='?', intents=intents)

staff_voice_channel_id = 1260975048743714940
staff_text_channel_id = 1260975048395849859

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('crafty-hall-397304-c7c7303971e0.json', scope) 
client_sheets = gspread.authorize(creds)

sheet = client_sheets.open_by_url('https://docs.google.com/spreadsheets/d/1wQl4magQUiHB9pzy-hpdMJ6peft1OMlcbDNrd2KAlMI/edit?gid=0#gid=0').sheet1

@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')
    print(f'Token: {os.getenv("DISCORD_TOKEN")}')

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == staff_voice_channel_id:
        try:
            row = [member.name, member.id, str(discord.utils.utcnow())]
            sheet.append_row(row)
            print("Dados adicionados à planilha!")  # Log
        except Exception as e:
            print(f"Erro ao adicionar dados à planilha: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))

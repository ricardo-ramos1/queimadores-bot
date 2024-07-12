import discord
from discord.ext import commands
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

# Intents para o bot
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

# Criação do bot com prefixo "?"
bot = commands.Bot(command_prefix='?', intents=intents)

# IDs dos canais
staff_voice_channel_id = 1260975048743714940
staff_text_channel_id = 1260975048395849859

# Configuração do gspread para acessar a planilha
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('crafty-hall-397304-c7c7303971e0.json', scope)
client_sheets = gspread.authorize(creds)
sheet = client_sheets.open_by_url(
    'https://docs.google.com/spreadsheets/d/1wQl4magQUiHB9pzy-hpdMJ6peft1OMlcbDNrd2KAlMI/edit?gid=0#gid=0'
).sheet1


@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')
    print(f'Token: {os.getenv("DISCORD_TOKEN")}')


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == staff_voice_channel_id:
        try:
            utc_now = discord.utils.utcnow()
            brasilia_timezone = timezone(timedelta(hours=-3))
            now_brasilia = utc_now.replace(tzinfo=timezone.utc).astimezone(brasilia_timezone)

            formatted_date = now_brasilia.strftime("%d/%m/%Y")
            formatted_time = now_brasilia.strftime("%H:%M")

            row = [member.name, member.display_name, member.id, formatted_date, formatted_time]
            sheet.append_row(row)
            print("Dados adicionados à planilha!")
        except Exception as e:
            print(f"Erro ao adicionar dados à planilha: {e}")


@bot.command(name='boss')
async def boss(ctx):
    print("Comando ?boss detectado no canal:", ctx.channel.name)

    try:
        channel = bot.get_channel(staff_voice_channel_id)
        if channel:
            print(f"Canal encontrado: {channel}")
            members = channel.members

            if members:
                print(f"Membros no canal: {members}")
                staff_text_channel = bot.get_channel(staff_text_channel_id)

                if staff_text_channel:
                    print(f"Canal de texto encontrado: {staff_text_channel}")
                    member_list = "\n".join([f"{member.name} ({member.id})" for member in members])
                    await staff_text_channel.send(f'Membros online no canal da staff:\n{member_list}')
                    print("Mensagem enviada com sucesso!")

                    try:
                        print("Tentando adicionar dados à planilha...")
                        for member in members:
                            utc_now = discord.utils.utcnow()
                            brasilia_timezone = timezone(timedelta(hours=-3))
                            now_brasilia = utc_now.replace(tzinfo=timezone.utc).astimezone(brasilia_timezone)
                            formatted_date = now_brasilia.strftime("%d/%m/%Y")
                            formatted_time = now_brasilia.strftime("%H:%M")
                            row = [member.name, member.display_name, member.id, formatted_date, formatted_time]
                            sheet.append_row(row)
                            print(f"Dados do membro {member.name} adicionados à planilha!")
                    except Exception as e:
                        print(f"Erro ao adicionar dados à planilha: {e}")
                else:
                    print("Canal de texto da staff não encontrado")
                    await ctx.send("Canal de texto da staff não encontrado.")
            else:
                print("Não há membros no canal de voz da staff.")
                await ctx.send("Não há membros no canal de voz da staff.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))

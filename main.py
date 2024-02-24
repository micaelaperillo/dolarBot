import os
import requests
import discord
from datetime import datetime 
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!help'):
    await message.channel.send('''¡Hola! 👋 ¿Buscas información sobre el precio del dólar?
Simplemente escribe `!dolares` para obtener el precio de 7 tipos de dólares en pesos, tanto para compra como para venta.''')

  if message.content.startswith('!dolares'):
    dollars = requests.get("https://dolarapi.com/v1/dolares").json()
    msg = "💰 *Cotizacion del Dolar* 💰\n"
    for dolar in dollars:
      # Format: USD {Nombre} - Compra: {compra} - Venta: {venta}
      msg += f"- USD {dolar['nombre']} - Compra: ${dolar['compra']} - Venta: ${dolar['venta']}\n"

    # Convertir la cadena a un objeto datetime
    fecha_ultima_actualizacion = dollars[0]['fechaActualizacion']
    fecha_ultima_actualizacion = datetime.fromisoformat(
        fecha_ultima_actualizacion.replace("Z", "+00:00"))

    fecha_ultima_actualizacion = fecha_ultima_actualizacion.strftime(
        "%d/%m/%Y @ %H:%M:%S")
    msg += f"🕝 Ultima actualizacion: {fecha_ultima_actualizacion}"
    await message.channel.send(msg)

token = os.getenv(os.getenv(TOKEN)) or ""
client.run(token)

import os
from discord.ext import commands
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import discord
import inflect
import time
from datetime import datetime




p = inflect.engine()

#headers de acesso 
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

#define prefixo de chamada do bot
bot = commands.Bot(command_prefix='!')

@bot.group()


async def wh(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Comando Inválido')
#início do bot
@wh.command(name = "busca",pass_context=True,help=" ![prefixo] <busca> <termo de busca> ""\n""Exemplo: !wh busca guia de mago")
#bloqueia comandos do chat privado
@commands.guild_only()

#inicio busca
async def busca(ctx, *, termo):

    for guild in bot.guilds:
         if guild.name == GUILD:
               break

    print(
         f'{bot.user} Está conectado do servidor:\n'
         f'{guild.name}(id: {guild.id})\n'
    )
    
    await bot.change_presence(activity=discord.Game(name="World of Warcraft"))
    links =[]
    titulos = []
    url = ("https://www.wowhelp.com.br/?s=" + termo)
    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.content, 'html.parser')
    all_a = soup.select('.entry-title a')
    for t in all_a:
        b = t.text
        c = t.attrs['href']
        titulos.append(b)
        links.append(c)

    count = 0
    resultado = ""
    l = len(titulos)
    if ( l == 0):
        embed = discord.Embed(title="Resultados da busca para o termo: " + termo, colour=discord.Colour(0xd98a17),
                              url="https://www.wowhelp.com.br",
                              description="{0.mention} infelizmente não encontramos o que você procura.".format(ctx.message.author),
                              timestamp=ctx.message.created_at)

    else:
        while count < l:
            teste = p.number_to_words(count+1)
            if (teste == "ten"):
                teste = "keycap_ten"
            resultado +=  ":"+teste+": [" + titulos[count] + "](" + links[count] + ") \n"
            if count == 9:
                break
            count+=1
        
    embed = discord.Embed(title="Resultados da busca para o termo: " + termo, colour=discord.Colour(0xd98a17), url="https://www.wowhelp.com.br", description ="{0.mention}\n".format(ctx.message.author) + resultado, timestamp=ctx.message.created_at)
    embed.set_author(name="Wowhelp", url="https://www.wowhelp.com.br")
    embed.set_footer(text="Horário:")

    async with ctx.typing():
        time.sleep(1)
    await ctx.send(embed=embed)  # envia a mensagem no servidor
    await ctx.author.send(embed=embed) #envia a mensagem no privado

@wh.command(name="classes",help="![prefixo] <classes>""\n""Exemplo: !wh classes")

async def classes(ctx):
      class_guide = ("<:Bruxo:710340567883841536> [Bruxo](https://wowhelp.com.br/categoria/guias/classes/bruxo/) \n"
                     "<:Cacador:710340567791566880> [Caçador](https://wowhelp.com.br/categoria/guias/classes/cacador/) \n"
                     "<:Cacador_de_demonios:710340567607017473> [Caçador de Demônios](https://wowhelp.com.br/categoria/guias/classes/cacador-de-demonios/) \n"
                     "<:Cavaleiro_da_morte:710340567921590302> [Cavaleiro da Morte](https://wowhelp.com.br/categoria/guias/classes/cavaleiro-da-morte/) \n"
                     "<:Druida:710340568051482744> [Druida](https://wowhelp.com.br/categoria/guias/classes/druida/) \n"
                     "<:Guerreiro:710340567963402301> [Guerreiro](https://wowhelp.com.br/categoria/guias/classes/guerreiro/) \n"
                     "<:Ladino:710340568169054209> [Ladino](https://wowhelp.com.br/categoria/guias/classes/ladino/) \n'"
                     "<:Mago:710340568135237643> [Mago](https://wowhelp.com.br/categoria/guias/classes/mago/) \n"
                     "<:Monge:710340567682383894> [Monge](https://wowhelp.com.br/categoria/guias/classes/monge/) \n"
                     "<:Paladino:710340568189894666> [Paladino](https://wowhelp.com.br/categoria/guias/classes/paladino/) \n"
                     "<:Sacerdote:710340567850025002> [Sacerdote](https://wowhelp.com.br/categoria/guias/classes/sacerdote/) \n"
                     "<:Xama:710340568194088971> [Xamã](https://wowhelp.com.br/categoria/guias/classes/xama/) \n")

      embed = discord.Embed(title="Guias de Classe para: ", colour=discord.Colour(0xd98a17), url="https://www.wowhelp.com.br", description ="{0.mention}\n \n".format(ctx.message.author) + class_guide, timestamp=ctx.message.created_at)
      await ctx.send(embed=embed)
      #sent = await ctx.send(embed=embed)
      #emojis=['<:Xama:710340568194088971>']
      #for emoji in emojis:
      #    await sent.add_reaction(emoji)


async def get_api_token():
  url = "https://CLIENTKEY:SECRETKEY@us.battle.net/oauth/token"
  headers = {'grant_type': 'client_credentials'}
  requisicao_token = requests.get(url = url, params = headers)
  data = requisicao_token.json()
  access_token = data["access_token"]
  return access_token

#BOTS COM API DA BLIZZ
@wh.command(name="token",help="![prefixo] <token>""\n""Exemplo: !wh token")
async def get_token_value(ctx):
  access_token = await get_api_token()
  #print (access_token)
  token_valor_url = requests.get('https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token=%s'%access_token)
  token_dados = token_valor_url.json()
  token_valor_json = token_dados["price"]/10000
  formatacao_token=("{:3,.0f}".format(token_valor_json));
  token_hora = (token_dados["last_updated_timestamp"]/1000)
  token_hora_convert = (datetime.fromtimestamp(token_hora).strftime('%d/%m/%Y às %H:%M'))
  desc = ("O Valor atual do Token US é: "+formatacao_token+"g \n \n Última atualização: "+token_hora_convert+"\n \n")
  embed = discord.Embed(title="Valor do Token ", colour=discord.Colour(0xd98a17),url="https://www.wowhelp.com.br",description="{0.mention}\n \n".format(ctx.message.author) + desc,timestamp=ctx.message.created_at)

  await ctx.send(embed=embed)


bot.run(TOKEN)

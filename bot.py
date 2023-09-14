import discord
import random
from discord.ext import commands
from colorama import Fore, Back, Style
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import selenium
from selenium import webdriver
from getpass import getpass
import time
    
#region GetFruitList
def purifyFruit(fruitInput):
    fruits =[]
    for fruit in fruitInput:
        fruits.append(fruit.lower())
    output = []
    for fruit in fruits:
        if (fruit.endswith('ies')):
            output.append(fruit[:len(fruit)-3] + 'y')
        elif (fruit.endswith('s')):
            output.append(fruit[:len(fruit)-1])
        else:
            output.append(fruit)
    return output
    
my_url = 'https://www.halfyourplate.ca/fruits-and-veggies/fruits-a-z/'

#Opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#HTML parsing
page_soup = soup(page_html, "html.parser")

container = page_soup.find("ul", {"class":"fv-list"})
items = container.findAll("li")

fruits = []
fruitPics = []

for item in items:
    theAs = item.findAll("a")
    fruits.append(theAs[1].text)

    fruitPics.append(item.div.span.a.img['src'])

fruits = purifyFruit(fruits)
#endregion GetFruitList

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = 'minos-', intents=intents)

@client.event
async def on_ready():
    print(Fore.MAGENTA + Back.GREEN + '----------Bot is ready----------' + Style.RESET_ALL)

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

#region Commands
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {client.latency * 1000}ms')

@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
        responses = ['Judgement says it is certain.',
                    'Steve says it is decidedly so.',
                    'Without a doubt.',
                    'Yes - definitely',
                    'According to the Golem, you may rely on it',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Uumuu and Nosk believe so.',
                    'Reply hazy, try again',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again',
                    "Don't count on it.",
                    "Madeline's reply is no.",
                    'The Moon Lord says no.',
                    'Outlook not so good.',
                    'Very doubtful.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount=5):
    amount+=1
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
async def assignfruit(ctx):
    member_list = []
    for member in ctx.message.guild.members:
        member_list.append(member.display_name)
    
    vowels = ["a","e","i","o","u"]
    output = ''
    for m in member_list:
        for f in fruits:
            if(f.lower() in m.lower()):
                output = f
                break
            else:
                output = random.choice(fruits)

        if(output[0] in vowels):
            middle = ' is an '
        else:
            middle = ' is a '
        await ctx.send(m + middle + output)

        if(output == 'cherry'):
            await ctx.send('https://scontent-atl3-2.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/131379694_3537126179706385_6448360691970429570_n.jpg?_nc_ht=scontent-atl3-2.cdninstagram.com&_nc_cat=101&_nc_ohc=cST8_XwLIA4AX_Qomvd&tp=1&oh=0a89bdd818bc1202aba9cb255b9af189&oe=6062D99D')
        else:
            await ctx.send(fruitPics[fruits.index(output)])

@client.command()
async def getgrades(ctx, id, password):
    driver = webdriver.Chrome(executable_path="C:\\Users\\justi\\Desktop\\Personal\\WebDriver\\chromedriver.exe")
    driver.get("https://publish.gwinnett.k12.ga.us/gcps/home/gcpslogin")


    id_textbox = driver.find_element_by_id("portalUserID")
    id_textbox.send_keys(id)

    password_textbox = driver.find_element_by_id("portalPassword")
    password_textbox.send_keys(password)

    login_button = driver.find_element_by_id("_loginsubmit")
    login_button.click()

    driver.get("https://apps.gwinnett.k12.ga.us/spvue/SamlSSOPortal.aspx?whr=https://apps.gwinnett.k12.ga.us/sps/spvue/saml20")
    driver.get("https://apps.gwinnett.k12.ga.us/spvue/PXP2_Gradebook.aspx?AGU=0&studentGU=32740E4B-6C59-4791-AA7D-5318C6D54363")

    grades = driver.find_elements_by_class_name("mark")
    classes = driver.find_elements_by_class_name("btn.btn-link.course-title")

    for x in range(len(grades)):
        await ctx.send(classes[x].text + ": " + grades[x].text)
    
    driver.quit()

#endregion

client.run(*)

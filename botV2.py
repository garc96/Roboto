import discord
from discord.ext import commands
import asyncio
import variables as var

bot = commands.Bot(command_prefix='!',case_insensitive = True)

#db = var.got_database()

def get_roles(server):
    roles = []
    for role in list(server.roles):
        roles.append(str(role))
    return roles

def get_user(server, Name):
    for user in list(server.members):
        if user.display_name == Name:
            print(user.display_name)
            return user
    return None

def get_role(server, role):
    for r in list(server.roles):
        if str(r) == role:
            return r
    return None

def identify(server,string, toFind = ''):
    lstring = string.split(' ')
    for minidx in range(len(lstring)):
        for maxidx in range(len(lstring)):
            check = ' '.join(lstring[minidx:len(lstring)-maxidx])
            if toFind == 'Name':
                check = get_user(server,check)
            elif toFind == 'Categoria':
                check = get_role(server,check)
            
            if check != None:
                return check

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------\n')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles,name = "Aspirante")
    await bot.add_roles(member,role)
    await bot.send_message(member,var.got_message('greet','new').replace('user',str(member).split("#")[0]))

@bot.command(pass_context = True,brief = 'Vincula tus datos',help = "Te permite vincular tu cuenta de discord con tus datos de robota",description = 'Este comando te permite vincular tus datos en discord con los de Robota')
async def login(ctx,matricula):
    if ctx.message.channel.is_private == True:
        await bot.send_message(ctx.message.channel,var.got_message('error','wrongChannel'))
    else:
        await bot.delete_message(ctx.message)
        db = var.get_database("database")
        if matricula in db:
            
            name = [db[matricula]["Name"]["firstName"], db[matricula]["Name"]["firstLastName"], db[matricula]["Name"]["secondLastName"]]
            await bot.change_nickname(member = ctx.message.author,nickname = ' '.join(name))
            await bot.send_message(ctx.message.author,var.got_message('success','login').replace('user',str(ctx.message.author)))
            
            hc = var.get_database("baseData")["jerarquia"]

            if db[matricula]["status"] >= 2:

                for Rol in hc:
                    role = discord.utils.get(ctx.message.server.roles,name = Rol)
                    if hc.index(Rol) < 2 or Rol == "Lider de Categoria" or Rol not in hc[:db[matricula]["status"]]:
                        await bot.remove_roles(ctx.message.author,role)
                    elif Rol != "Lider de Categoria":
                        await bot.add_roles(ctx.message.author,role)

            elif db[matricula]["status"] < 2:
                while ctx.message.author.top_role != discord.utils.get(ctx.message.server.roles,name = hc[db[matricula]["status"]]):
                    await bot.remove_roles(ctx.message.author,ctx.message.author.top_role)
                
                if ctx.message.author.top_role != discord.utils.get(ctx.message.server.roles,name = hc[db[matricula]["status"]]):
                    role = discord.utils.get(ctx.message.server.roles,name = hc[db[matricula]["status"]])
                    await bot.add_roles(ctx.message.author,role)

            for categoria in db[matricula]["categorias"]:
                roles = get_roles(ctx.message.server)
                if categoria.title() in roles:
                    role = discord.utils.get(ctx.message.server.roles,name = categoria.title())
                    await bot.add_roles(ctx.message.author,role)
                else:
                    Categoria = categoria
                    Role = categoria
                    Roles = get_roles(ctx.message.server)
                    if Role not in Roles:
                        await bot.create_role(ctx.message.server,mentionable = True, colour = discord.utils.get(ctx.message.server.roles,name = "Aspirante").colour ,hoist = False, name = Role)

                        everyonePerms = discord.PermissionOverwrite(read_messages=False, send_messages=False, create_instant_invite=False, manage_channel=False, manage_permissions=False, manage_webhooks=False, send_TTS_messages=False, manage_messages=False, embed_links=False, attach_files=False, read_message_history=False, mention_everyone=False, use_external_emojis=False, add_reactions=False)
                        membersPerms = discord.PermissionOverwrite(read_messages=True, send_messages=True, create_instant_invite=False, manage_channel=False, manage_permissions=False, manage_webhooks=False, send_TTS_messages=True, manage_messages=False, embed_links=True, attach_files=True, read_message_history=True, mention_everyone=True, use_external_emojis=True, add_reactions=True)

                        await bot.create_channel(ctx.message.server,Categoria,(ctx.message.server.default_role, everyonePerms),(discord.utils.get(ctx.message.server.roles,name = Role),membersPerms))
                        await bot.send_message(ctx.message.channel,'La categoria ' + str(Role) + ' ha sido creada con exito.')
                        
                        await bot.add_roles(ctx.message.author,discord.utils.get(ctx.message.server.roles,name = Role))

                        print(discord.utils.get(ctx.server.channels,name = Categoria))
                        await bot.move_channel(discord.utils.get(ctx.server.channels,name = Categoria),5)    


                if db[matricula]["categorias"][categoria]["status"] == 1:
                    role = discord.utils.get(ctx.message.server.roles,name = "Lider de Categoria")
                    await bot.add_roles(ctx.message.author,role)
        else:
            await bot.send_message(ctx.message.author,var.got_message('error','noRegistry'))

@bot.command(pass_context=True,hidden = True)
async def purge(ctx):
    if ctx.message.author.top_role > discord.utils.get(ctx.message.server.roles,role = "Directiva"):
        for channel in list(ctx.message.server.channels):
            #await bot.delete_channel(channel)
            print(channel)
    else:
        await bot.send_message(ctx.message.channel,var.got_message("error","saved",False))

@bot.command(pass_context=True,hidden =True)
async def purgeCat(ctx):
    for role in list(ctx.message.server.roles):
        if str(role) == 'Trash Gang > All !':
            await bot.delete_role(ctx.message.server,role)

@bot.command(pass_context = True, brief = 'Muestra las categorias disponibles' ,help = "Muestra las categorias disponibles")
async def categorias(ctx):
    if ctx.message.channel.is_private == True:
        await bot.send_message(ctx.message.channel,var.got_message('error','wrongChannel'))
    else:
        roles = get_roles(ctx.message.server)[8:]
        await bot.send_message(ctx.message.channel,'\n'.join(roles))

@bot.command(pass_context = True, brief = 'Te permite ingresar a una categoria',help = "Te permite ingresar a una categoria, solo funciona si eres lider de categoria")
async def agregar(ctx,Nombre,Categoria):
    if ctx.message.channel.is_private == True:
        await bot.send_message(ctx.message.channel,var.got_message('error','wrongChannel'))
    else:
        if ctx.message.author.top_role >= discord.utils.get(ctx.message.server.roles,name = "Lider De Categoria"):
            user,role = identify(ctx.message.server,ctx.message.clean_content,'Name'),identify(ctx.message.server,ctx.message.clean_content,'Categoria')
            if user != None and role != None:
                await bot.add_roles(user,role)
            else:
                await bot.send_message(ctx.message.channel,var.got_message('error','notFound'))


@bot.command(pass_context = True,brief = 'Permite crear una categoria' ,help = "Permite crear una categoria, solo sirve si eres lider de categoria o directiva, asegurate de que el nombre de la persona sea la que se muestra en la lista de miembros" ,description = 'Este comando permite a los lideres de categoria crear una categoria')
async def crearCategoria(ctx,Categoria):
    if ctx.message.channel.is_private == True:
        await bot.send_message(ctx.message.channel,var.got_message('error','wrongChannel'))
    else:
        Categoria = '-'.join(ctx.message.clean_content.split(' ')[1:])
        Role = Categoria.replace('-',' ').title()
        Roles = get_roles(ctx.message.server)
        if Role not in Roles:
            await bot.create_role(ctx.message.server,mentionable = True, colour = discord.utils.get(ctx.message.server.roles,name = "Aspirante").colour ,hoist = False, name = Role)

            everyonePerms = discord.PermissionOverwrite(read_messages=False, send_messages=False, create_instant_invite=False, manage_channel=False, manage_permissions=False, manage_webhooks=False, send_TTS_messages=False, manage_messages=False, embed_links=False, attach_files=False, read_message_history=False, mention_everyone=False, use_external_emojis=False, add_reactions=False)
            membersPerms = discord.PermissionOverwrite(read_messages=True, send_messages=True, create_instant_invite=False, manage_channel=False, manage_permissions=False, manage_webhooks=False, send_TTS_messages=True, manage_messages=False, embed_links=True, attach_files=True, read_message_history=True, mention_everyone=True, use_external_emojis=True, add_reactions=True)

            await bot.create_channel(ctx.message.server,Categoria,(ctx.message.server.default_role, everyonePerms),(discord.utils.get(ctx.message.server.roles,name = Role),membersPerms))
            await bot.send_message(ctx.message.channel,'La categoria ' + str(Role) + ' ha sido creada con exito.')
            
            await bot.add_roles(ctx.message.author,discord.utils.get(ctx.message.server.roles,name = Role))

            #await bot.move_channel(discord.utils.get(ctx.message.server.channels,name = Categoria),5)

bot.run(var.get_token())
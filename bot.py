import discord 
import asyncio

client = discord.Client()

def this_channel(server, channelName):
    server.channels
    for channel in list(server.channels):
        print(str(channel),channelName)
        if str(channel) == channelName:
            return channel

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    server = list(client.servers)[0]

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles,name = "Aspirante")
    await client.add_roles(member,role)

@client.event
async def on_message(message):
    
    roles = []

    server = list(client.servers)[0]
    for role in server.role_hierarchy:
        roles.append(str(role))

    if message.author ==  client.user:
        return
    
    if message.content.startswith('!hola'):
        msg = "Hola {0.author.mention}".format(message)
        await client.send_message(message.channel,msg)

    elif message.content.startswith("!help"):
        msg = 'Puedo realizar las siguientes funciones: '
        await client.send_message(message.channel,msg)

    elif message.content.startswith("!beep"):
        await client.send_message(message.channel,'beep boop beep')

    elif message.content.startswith("!ping"):
        await client.send_message(message.channel,'Pong')

    elif message.content.startswith("!admin") and message.author.top_role >= discord.utils.get(list(client.servers)[0].roles, name = "Lider de categoria"):
        parametros = str(message.content).split(" ")
        if len(parametros) >= 3:
            if parametros[1] == 'crearCategoria':
                roleName = ' '.join(parametros[2:])

                if roleName not in roles:

                    await client.create_role(list(client.servers)[0],mentionable = True, colour = discord.utils.get(list(client.servers)[0].roles,name = "Batalla").colour ,hoist = False, name = roleName)
                    
                    channelName = str('-'.join(parametros[2:]))

                    everyonePerms = discord.PermissionOverwrite(read_messages=False, send_messages=False, create_instant_invite=False, manage_channel=False, manage_permissions=False, manage_webhooks=False, send_TTS_messages=False, manage_messages=False, embed_links=False, attach_files=False, read_message_history=False, mention_everyone=False, use_external_emojis=False, add_reactions=False)
                    membersPerms = discord.PermissionOverwrite(read_messages=True, send_messages=True, create_instant_invite=False, manage_channel=False, manage_permissions=False, manage_webhooks=False, send_TTS_messages=True, manage_messages=False, embed_links=True, attach_files=True, read_message_history=True, mention_everyone=True, use_external_emojis=True, add_reactions=True)
                    #catLeaderPerms = discord.PermissionOverwrite(read_messages=True, send_messages=True, create_instant_invite=True, manage_channel=True, manage_permissions=False, manage_webhooks=True, send_TTS_messages=True, manage_messages=True, embed_links=True, attach_files=True, read_message_history=True, mention_everyone=True, use_external_emojis=True, add_reactions=True)
                    
                    await client.create_channel(server,channelName,(server.default_role, everyonePerms),(discord.utils.get(server.roles,name = roleName),membersPerms))
                    await client.send_message(message.channel,'La categoria ' + str(roleName) + ' ha sido creada con exito.')    

                else:
                    await client.send_message(message.channel,'La categoria ' + str(roleName) + ' ya existe.')    
    
    elif message.content.startswith("!member") and message.author.top_role >= discord.utils.get(list(client.servers)[0].roles, name = "Miembro Activo"):
        msg = str(message.author) + " summon this !member\n"
        try:
                parametros = str(message.content).split(" ")
                if parametros[1][0] == '-':
                    role = discord.utils.get(message.server.roles,name = parametros[1][1:].capitalize())
                    await client.remove_roles(message.author,role)
                    await client.send_message(message.channel,("{0.author.mention} fuiste removido de la categoria " + str(role)).format(message))

                else:
                    role = discord.utils.get(message.server.roles,name = parametros[1].capitalize())
                    if role != None:
                        if role < message.server.role_hierarchy[roles.index("Miembro Activo")]:
                            await client.add_roles(message.author,role)
                            await client.send_message(message.channel,("{0.author.mention} ahora perteneces a la categoria " + str(role)).format(message))

                            msg += str(message.author) + ' added a new role as ' + str(role)
                        else:
                            msg += str(message.author) + ' tried but didnt got permission ' + str(role)
                            await client.send_message(message.channel,'No tienes los permisos necesarios para otorgarte el rol de ' + parametros[1])

                    else:
                        if parametros[1] == 'help':
                            msg += str(message.author.top_role) + " asked help"
                            await client.send_message(message.channel,'Prueba usando el comando: \n!member <Nombre de categoria>')
                            await client.send_message(message.channel,'Categorias disponibles: '+'\n'.join(roles[roles.index('Aspirante')+1:len(roles)-1]))
                        elif parametros[1] == 'nick':
                            name = str(message.author).split('#')[0]
                            nick = ' '.join(parametros[2:])
                            await client.send_message(message.channel,'Tu nombre a sido cambiado de ' + name + ' a ' + nick)
                            await client.change_nickname(message.author,nick)                    
                        else:
                            msg += str(message.author.top_role) + " tried with a wrong category or option"
                            await client.send_message(message.channel,'Ingresaste una categoria no valida, para revisar las categorias usa !member help')
        except AttributeError:
            msg += str(message.author) + ' tried to summon in user to user channel'
            await client.send_message(message.channel,'Solo puedes usar los comandos de este bot dentro del servidor Robota, porfavor dirigete a @general o @aspirantes')
        print(msg+'\n')

    elif message.content.startswith("!aspirante"):
        msg = str(message.author) + " summon this !aspirante\n"
        try:
            if str(message.author.top_role) == "Aspirante" and len(list(message.author.roles)) == 2:
                parametros = str(message.content).split(" ")
                role = discord.utils.get(message.server.roles,name = parametros[1].capitalize())
                if role != None:
                    if role < message.server.role_hierarchy[roles.index("Aspirante")]:
                        await client.add_roles(message.author,role)
                        await client.send_message(message.channel,("{0.author.mention} ahora perteneces a la categoria " + str(role)).format(message))

                        msg += str(message.author) + ' added a new role as ' + str(role)
                    else:
                        msg += str(message.author) + ' tried but didnt got permission ' + str(role)
                        await client.send_message(message.channel,'No tienes los permisos necesarios para otorgarte el rol de ' + parametros[1])

                else:
                    if parametros[1] == 'help':
                        msg += str(message.author.top_role) + " asked help"
                        await client.send_message(message.channel,'Prueba usando el comando: \n!aspirantes <Nombre de categoria>')
                        await client.send_message(message.channel,'Categorias disponibles: '+'\n'.join(roles[roles.index('Aspirante')+1:len(roles)-1]))
                    elif parametros[1] == 'nick':
                        name = str(message.author).split('#')[0]
                        nick = ' '.join(parametros[2:])
                        await client.send_message(message.channel,'Tu nombre a sido cambiado de ' + name + ' a ' + nick)
                        await client.change_nickname(message.author,nick)                    
                    else:
                        msg += str(message.author.top_role) + " tried with a wrong category or option"
                        await client.send_message(message.channel,'Ingresaste una categoria no valida, para revisar las categorias usa !aspirantes help')

            else:
                x = discord.utils.get(server.roles, name = 'Aspirante')
                if message.author.top_role <= discord.utils.get(server.roles, name = 'Aspirante'):
                    await client.send_message(message.channel,'Ya fuiste asignado a una categoria, si deseas ingresar a otra contactate con un lider de categoria')
                else: 
                    await client.send_message(message.channel,'Eres miembro activo de robota, por favor intenta usar !member <Nombre de categoria>')

        except AttributeError:
            msg += str(message.author) + ' tried to summon in user to user channel'
            await client.send_message(message.channel,'Solo puedes usar los comandos de este bot dentro del servidor Robota, porfavor dirigete a @general o @aspirantes')
        print(msg+'\n')


client.run('NTM5MjYwMTgyMjQ1NTM5ODQw.Dy_w0Q.DIH1pLfTyj7tE2Xo-GU-XtsjybY')
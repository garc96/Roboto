import json

route = 'C:\\Users\\Kevin\\Documents\\Projects\\DiscordBot'

def get_token():
    with open(route + '\\auth.json') as f:
        token = json.load(f)['token']
    return token

def get_database(name):
    with open(route + '\\' + name + '.json') as f:
        db = json.load(f)
    return db

def got_message(category,name):
    msg = []
    with open(route + '\\messages\\'+category+'\\'+name+'.txt') as f:
        for line in f:
            msg.append(line.replace('Â',''))
    with open(route + '\\messages\\'+category+'\\base.txt') as f:
        i=0
        for line in f:
            if i == 0:
                msg.append('\n'+line.replace('Â',''))
            else:
                msg.append(line.replace('Â',''))
            i+=1
    return ''.join(msg)
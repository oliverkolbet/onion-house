# onion.py

# This is the onion house game!

#Imports for randomness and delays
from time import sleep
from random import randint, choice, shuffle
from os import system

#Inventory items have a limited amount of usage.
inventory={}

warningSigns=['TURN BACK','CERTAIN DEATH LIES AHEAD','20% OFF SALE SPECIAL','DO NOT PASS','DO NOT READ THIS SIGN','AUTHORIZED PERSONNEL ONLY','BEING IS NOT ALLOWED','NO','THIS WAY (NOT)','BEWARE','STOP','YEAH NOPE']

# Special Item Variables
panelGot=False
cupboardOpen=False
# Current location
current='Tutorial'

# What items read
writing={
    'onion':'Seriously? Reading an onion?',
    'purple':'Purple',
    'wooden-key':'The key reads: "Cupboard"',
    'iron-key':'It says: "Freezer Door"',
    'banner':'The banner is completely smooth and silky.',
    'onionomicon':'The onionomicon glows for a second.'
}

sias={
'get':['banner','onion'],
'use':['purple','door','panel','cupboard','onion'],
'fight':[],
'read':['onionomicon']
}

mRooms=['Main Hall','Freezer','Closet','Closet Crawlspace','North Hall','Kitchen','Purple Room']

room = {
    'Tutorial':{
        'go':{
            'south':'Foyer'
        },
        'items':{
            'onion':'get'
        },
        'entrance-desc':{
            'north':'To the north you see the path you have traveled by.',
            'east':'You see a sign reading '+choice(warningSigns)+' to the east.',
            'south':'To the south is a large iron door.',
            'west':'There is a small stone pedestal to the west. On it is an onion for some reason.',
            'up':'You can barely see the sun through the thick vegetation.',
            'down':'Dirt.'
            
        },
        'monster':False
    },
    'Foyer':{
        'go':{
            'north':'Uhh... that\'s the locked exit',
            'east':'Purple Room',
            'south':'North Hall',
            'west':'wall',
            'up':'You bang your head on the ceiling',
            'down':'The floor is as hard as a rock.'
        },
        'items':{
            'banner':'get'
        },
        'entrance-desc':{
            'north':'There is a locked steel door there',
            'east':'You see a huge purple door. It appears to be made of stone. (?)',
            'south':'To the south there is a dark narrow hall leading forever... (maybe)',
            'west':'The west wall has a picture of the house on it, a red banner, and some nice blue wallpaper.',
            'up':'The lights on the ceiling momentarily blind you.',
            'down':'The floor is tiled dark wood flooring with a large red mat on it.'
        },
        'monster':False
    },
    'Kitchen':{
        'go':{
            'north':'wall',
            'east':'Foyer',
            'south':'Freezer',
            'west':'wall',
            'up':'You bang your head on the cold ceiling',
            'down':'Yes, that is a floor'
        },
        'items':{
            'oven':'use'
        },
        'entrance-desc':{
            'north':'To the north you see a large counter and three fancy sinks.',
            'east':'That is the door to the Foyer.',
            'south':'To the south there is a huge studded door and a large refrigerator',
            'west':'There is an oven on the west wall and a large stovetop with many massive pots hanging above',
            'up':'The lights on the ceiling momentarily blind you.',
            'down':'The floor is very clean studded metal'
        },
        'monster':False
    },
    'North Hall':{
        'go':{
            'north':'Foyer',
            'east':'Closet',
            'south':'Main Hall',
            'west':'That is a wall.',
            'up':'You can\'t reach or see anything on the ceiling.',
            'down':'The floor is just a simple carpet.'
        },
        'items':{},
        'entrance-desc':{
            'north':'That is the Foyer.',
            'east':'You see a light-colored wooden door. It smells bad in there.',
            'south':'To the south the hall widens into a massive room.',
            'west':'That\'s a wall',
            'up':'You can\'t see anything up there.',
            'down':'The carpet smells a little.'
        },
        'monster':False
    },
    'Purple Room':{
        'go':{
            'north':'Purple',
            'east':'Purple',
            'south':'Purple',
            'west':'Foyer',
            'up':'Purple',
            'down':'Purple'
        },
        'items':{
            'purple':'use'
        },
        'entrance-desc':{
            'north':'Purple',
            'east':'Purple',
            'south':'Purple',
            'west':'That is the Foyer',
            'up':'Purple',
            'down':'Purple'
        },
        'monster':False
    },
    'Closet':{
        'go':{
            'west':'North Hall',
            'east':'wall',
            'south':'wall',
            'north':'wall',
            'up':'You can barely look up in the short room.',
            'down':'Closet Crawlspace'},
        'items':{},
        'entrance-desc':{
            'north':'You see a wall.',
            'east':'You see a wall',
            'south':'You see a wall',
            'west':'That is the North Hall.',
            'up':'That is the ceiling',
            'down':'You see a small, dark trapdoor'}
    },
    'Closet Crawlspace':{
        'go':{
            'west':'North Hall',
            'east':'wall',
            'south':'wall',
            'north':'wall',
            'up':'Closet',
            'down':'There is nothing below you.'},
        'items':{},
        'entrance-desc':{
            'north':'You see a wall.',
            'east':'You see a wall',
            'south':'You see a wall',
            'west':'You see a wall',
            'up':'That is the Closet',
            'down':'Nothing.'}
    },
    'Main Hall':{
        'go':{
            'north':'North Hall',
            'east':'East Hall',
            'south':'South Hall',
            'west':'West Hall',
            'up':'You can\'t even see the ceiling, it\'s so tall.',
            'down':'There is only a carpeted floor there.'
        },
        'items':{
            'fireplace':'use',
            'table':'use'
        },
        'entrance-desc':{
            'north':'Main Hall',
            'south':'Main Hall'
        }
    },
    'Freezer':{
        'go':{
            'north':'Uh-oh! The door is locked!',
            'east':'wall',
            'south':'wall',
            'west':'wall',
            'up':'You hit your head on the ceiling. It hurts!',
            'down':'There are only dark metal panels on the floor.'
        },
        'items':{
            'door':'use',
            'cupboard':'use',
            'panel':'use'
        },
        'entrance-desc':{
            'north':'You see a closed door leading to the kitchen.',
            'east':'To the east are shelves with various food items.',
            'south':'On the southern wall there is a small metal panel.',
            'west':'There is a locked cupboard to the west.',
            'up':'Nothing up there.',
            'down':'There are only dark metal panels on the floor.'
        }
    }
}

#Rainbowfy text!
colors=['\033[91m','\033[92m','\033[93m','\033[94m','\033[95m','\033[96m','\033[97m']
def rainbowfy(string):
    complete=''
    for letter in string:
        complete += (choice(colors)+letter)
    return complete


# Monster fight section:
monsterItems={'Spider':'spider-fang','Dust Bunny':'dustball','Meatball':'meat','Robot':'gear','Onion Ghost':'onion'}
monsters=['Spider','Dust Bunny','Meatball','Robot','Onion Ghost']
atkItems={
    'onion':2,
    'banner':0,
    'fist':1,
    'punch':1,
    'purple':20
}
def monster(m=choice(monsters)):
    print('Uh-oh! There\'s a '+m+'!')
    if randint(0,1) == 0:
        print('It doesn\'t look like it has noticed you yet...')
    else:
        while True:
            print('It sees you!')
            sleep(2)
            if randint(0,14) == 0:
                print('Now it looks like it\'s too tired to do anything.')
                break
            print('What do you do? [Attack/Run]')
            ar=input('>')
            if 'r' in ar:
                print('You turn to flee...')
                if purple in inventory:
                    print('But wait! You use the purple and the '+m+' is down!')
                    del inventory['purple']
                    sleep(3)
                    print('You got a '+monsterItems[m]+'!')
                    inventory[monsterItems[m]] = 'use'
                    break
                rc=randint(0,2)
                if rc == 0:
                    print('Quick! Which direction do you want to go?')
                    dir=input('>')
                    goto(dir)
                    return
                elif rc == 1:
                    print('Oof, too late! It already has you trapped!')
                    sleep(1)
                    print('Game Over...')
                    exit()
                elif rc == 2:
                    print('You drop all your items... And run away! Which way do you want to go?')
                    room[current]['entrance-desc']['down'] = 'You see your items: [ '
                    for item in inventory.keys():
                        room[current]['items'][item] = 'get'
                        room[current]['entrance-desc']['down'] += item+' '
                        room[current]['entrance-desc']['down'] += ']'
                    dir=input('>')
                    goto(dir)
                    break
            else:
                print('What do you want to use to attack?')
                atki=''
                while True:
                    atki = input('>')
                    if atki=='?' or atki=='help':
                        print('Inventory: '+', '.join(inventory.keys()))
                    elif (atki in inventory.keys() and atki in atkItems.keys()) or atki == 'fist' or atki == 'punch':
                        break
                    else:
                        print('Sorry, you can\'t use the '+atki)
                siatk = sia(atki, 'fight')
                if siatk == 'defeated':
                    del room[current]['monster']
                    sleep(2)
                    print('You got a '+monsterItems[m]+'!')
                    inventory[monsterItems[m]] = 'use'
                    break
                if atkItems[atki] >= randint(0,5):
                    print('Wow, the '+m+' is down!')
                    del room[current]['monster']
                    sleep(2)
                    print('You got a '+monsterItems[m]+'!')
                    inventory[monsterItems[m]] = 'use'
                    break
                else:
                    if randint(0,2) != 0:
                        print('The monster is still up!')
                    else:
                        print('Oof, the '+m+' clobbered you! Game Over!')
                        exit()
                if randint(0,1) == 0:
                    print('The '+atki+' broke! Oof!')
                    del inventory[atki]
                if randint(0,12) != 0:
                    room[choice(room.keys())]['monster'] = True # Monster moves to a random room

def goto(dir):
    global current
    if current == 'Tutorial':
        print('As you walk through, the onion vibrates and the door slams shut. You jiggle the handle, but it is locked. What do you do?')
    if dir=='bananas':
        while True:
            try:
                print(rainbowfy('G O   B A N A N A S !'))
                sleep(0.05)
            except KeyboardInterrupt:
                break
        print('\033[00m', end='')
        return
    try:
        way = room[current]['go'][dir]
    except KeyError:
        print('You can\'t go that way.')
        return
    if way in room.keys():
        current = way
        print("You have entered the "+current+"...")
        sleep(2)
        print(room[current]['entrance-desc'][dir])
        if room[current]['monster'] == True:
            monster()
    elif way == "locked":
        print("That door is locked!")
    elif way == "wall":
        print("That is a wall.")
    else:
        print(way)

lookList=['north','south','east','west','up','down']
def lookat(dir):
    if dir in lookList:
        print(room[current]['entrance-desc'][dir])
    else:
        print('You can\'t look that direction.')

remainingPages=['teleport','portal','duplicate','banish']
onionPages=[]

def sia(it,mode): # Special Item Action
    global panelGot, cupboardOpen, onionPages, remainingPages
    if it not in sias[mode]:
        return
    if mode == 'get':
        if it == 'banner':
            print('As you grab the banner it falls down, revealing a sturdy white door.')
            room['Foyer']['go']['west'] = 'Kitchen'
            room['Foyer']['entrance-desc']['west'] = 'There is a sturdy white door, a painting of the house, and some pretty wallpaper on the west wall.'
        elif it == 'onion':
            print('You snatch the onion and the shed seems to rumble for a moment.')
            inventory['onion']='use'
        elif it == 'page':
            if 'onionomicon' not in inventory.keys():
                print('You have nothing to put the pages in.')
                del inventory['page']
                room[current]['item']['page'] = 'get'
                return
            rPageChoice=choice(remainingPages)
            remainingPages.remove(rPageChoice)
            print('As you pick up the page, it glows, rumbles, and glides into the onionomicon.')
            sleep(2)
            print('The page reads "'+rPageChoice+'"')00000
    elif mode == 'use':
        if it == 'purple':
            print('Purple activated and in your inventory! Use the purple against monsters!')
            inventory['purple'] = 'get'
            del room['Purple Room']['items']['purple']
        elif it=='onion':
            sias['use'].remove('onion')
            sias['get'].remove('onion')
            print('You start to peel the onion... the ground seems to rumble for a minute... then the door begins to shake wildly!')
        if current=='Freezer':
            if it=='panel':
                if panelGot==False:
                    print('You open up the panel... and... There\'s a key!')
                    sleep(2)
                    print('You grab the key... what next?')
                    inventory['wooden-key'] = 'get'
                    panelGot=True
                else:
                    print('There is nothing else in the panel.')
            elif it=='cupboard':
                if cupboardOpen == False:
                    if 'wooden-key' in inventory.keys():
                        print('You slip the wooden key into the cupboard\'s keyhole and it slides open.')
                        sleep(2)
                        print('Inside the cupboard, you see a large iron key.')
                        sleep(2)
                        print('You grab the key... Now what?')
                        inventory['iron-key'] = 'get'
                        cupboardOpen=True
                    else:
                        print('You pull the cupboard handle but it appears to be locked.')
                else:
                    print('The cupboard is already open and empty.')
            elif it=='door':
                print('You jam the iron key into the door\'s keyhole and it swings open.')
                room['Freezer']['go']['north'] = 'Kitchen'
    elif mode == 'fight':
        pass
    elif mode == 'read':
        if it=='onionomicon':
            if len(onionPages) <= 0:
                print('There are no pages in the Onionomicon, you need to find more!')
                return
            print('What page of the Onionomicon would you like to read?')
        i=1
        for page in onionPages:
            print(str(i)+': '+page)
            i+=1
        try:
            pageChoice = int(input('>'))
        except TypeError:
            print('That is not a number.')
            return
        evaluateOnionPages(pageChoice)

def evaluateOnionPages(page):
    if page == 'teleport':
        print('Where do you want to teleport?')

def get(i):
    if i in room[current]['items']:
        if room[current]['items'][i] == 'get':
            del room[current]['items'][i]
            inventory[i] = 'get'
            sia(i,'get')
        else:
            print('Sorry, this item is not gettable.')
    else:
        print("Sorry, you can't get the "+i+".")

def read(i):
    if i in inventory.keys() or i in room[current]['items'].keys():
        print(writing[i])
        sia(i, 'read')
    else:
        print('The '+i+' isn\'t here.')

def use(i):
    if i in room[current]['items']:
        if room[current]['items'][i] == 'use':
            sia(i,'use')
        else:
            print('Sorry, this item is not usable.')
    elif i in inventory.keys():
        if inventory[i] == 'use':
            sia(i,'use')
        else:
            print('Sorry, this item is not usable now.')
    else:
        print("Sorry, you can't use the "+i+".")
            
def help():
    print('COMMAND HELP:')
    sleep(2)
    print('To go in a direction: "go [DIRECTION]". Directions are north, east, south, west, up, and down.')
    sleep(3)
    print('To see where you are, type "where"')
    sleep(2)
    print('To use, get, and read items use "use [ITEM]","get [ITEM]", and "read [ITEM]" respectively.')
    sleep(2)
    print('To look somewhere, use "look [DIRECTION]"')

def evaluate(c):
    if c[0] == 'i' or c[0] == 'inventory' or c[0] == 'stuff':
        if len(inventory.keys()) > 0:
            print('Inventory: '+', '.join(inventory.keys()))
        else:
            print('Your inventory is currently empty.')
    elif c[0] == 'go' or c[0] == 'cd':
        if len(c) >= 2:
            goto(c[1])
        else:
            print("Go where?")
            go = input('>')
            goto(go)
    elif c[0] == 'get':
        if len(c) >= 2:
            get(c[1])
        else:
            print("Get what?")
            iget=input(">")
            get(get)
    elif c[0] == 'where' or c[0] == 'pwd':
        print("You are in the "+current)
    elif c[0] == 'look' and len(c) >= 2:
        lookat(c[1]) 
    elif c[0] == 'use' and len(c) >= 2:
        use(c[1])
    elif c[0] == 'read' and len(c) >= 2:
        read(c[1])
    elif c[0] == 'di':
        if debugLevel >= 1:
            print(inventory)
    elif c[0] == 'dr':
        if debugLevel >= 2:
            print(room[current])
    elif c[0] == 'dm' and len(c) >= 2:
        if len(c) >= 3:
            try:
                debugMode(c[1], int(c[2]))
            except TypeError:
                print('The second argument for debugMode must be an integer value.')
        else:
            debugMode(c[1])
    elif c[0] == 'clear':
        system('clear')
    elif c[0] == 'rainbowify' and len(c) >= 2:
        del c[0]
        print(rainbowfy(' '.join(c))+'\033[00m')
    elif c[0] == 'help' or c[0] == '?':
        help()


def tutorial():
    print('COMMAND TUTORIAL')
    sleep(2)
    print('The first command is the "where" command.')
    sleep(2)
    print('Try using it now.')
    command=''
    while command != 'where':
        command=input('>')
    evaluate(['where'])
    sleep(2)
    print('The where command tells you which room you are in, and the next one is the look command.')
    sleep(2)
    print('You can look these ways: north, east, south, west, up, down.')
    sleep(2)
    print('Try it out now, using "look [DIRECTION]". Once you are done, type "done"')
    while True:
        while 'look' not in command and 'done' not in command:
            command=input('>')
        if command == 'done':
            print('Done.')
            break
        else:
            if len(command) >= 2:
                command=command.split(' ')
                lookat(command[1])
            else:
                print('You need to specify a direction.')
            command=''
    sleep(2)
    print('The next command is very simple. If you looked around all the way in the last step, you may have seen a stone pedestal to the west.')
    sleep(3)
    print('On top of the pedestal was an onion. In this step, we will be getting the onion.')
    sleep(2)
    print('Use the "get [OBJECT]" command to get the onion.')
    command=''
    while command != 'get onion':
        command=input('>')
    get('onion')
    sleep(1)
    print('Well, now the onion is in our inventory. To see what is in there, we will use a new command.')
    sleep(2)
    print('This command is "inventory". it tells us what is in there. Since this takes a while to type out, you can also type "i".')
    sleep(1)
    command=''
    while command != 'inventory' and command != 'i':
        command=input('>')
    evaluate(['inventory'])
    print('Aha! We have the onion. This item, like many others, is usable. To use an item, type "use [ITEM]". Do that with the onion now.')
    command=''
    while command != 'use onion':
        command=input('>')
    use('onion')
    sleep(1)
    print('That was weird... Anyway, another very useful command is the "help" command. It provides help overall for the game. If you get stuck, type "help".')
    sleep(3)
    print('Our next command is the "read" command. We can read items that may be readable with this command.')
    sleep(3)
    print('By the way, we don\'t need to test that one out, so let\'s move on to the FINAL AND MOST IMPORTANT command.')
    sleep(3)
    print('This is the "go" command. Just like looking in a direction, we can also go a direction.')
    sleep(3)

def debugMode(level='startLowest', nLevel=0):
    global debugLevel
    if level == 'startLowest':
        debugLevel=0
        return
    elif level == 'level': 
        debugLevel=nLevel+0
        print('Debug level set to'+str(nLevel))
    elif level == 'lowest':
        debugLevel=0
        print('Debug level is lowest.')
    elif level == 'low':
        debugLevel=1
        print('Debug level is low.')
    elif level == 'data':
        debugLevel=2
        print('Debug level is full data')
    elif level == 'sudo':
        debugLevel=3
        print('Debug level is full sudo')

def begin():
    debugMode()
    global warningSigns
    print('Onion house BETA started.')
    sleep(2)
    print('You have searched for this place for years. As you walk through the dense vegetation, you see many signs of warning:')
    sleep(4)
    shuffle(warningSigns)
    print(warningSigns[0])
    sleep(1)
    print(warningSigns[1])
    sleep(1)
    print(warningSigns[2])
    sleep(1)
    print(warningSigns[3])
    sleep(1)
    print('You push on, ending at what appears to be a small stone building')
    sleep(3)
    print('Walking around it, it appears to be some sort of shed. You open the door and look down a massive hallway. How is this even possible?')
    sleep(3)
    print('Before you enter the room, would you like the command tutorial?')
    tutorialTrue=input('>')
    if 'y' in tutorialTrue:
        tutorial()
    else:
        print("OK.")
        inventory['onion']='use'
        sleep(2)
        print('You pick up an onion sitting on a stone pedestal to your left.')
        sleep(2)
    monsters.remove(choice(monsters))
    monsters.remove(choice(monsters))
    monsters.remove(choice(monsters))
    for rm in mRooms:
        if randint(0,2) == 0:
            room[rm]['monster'] = True
        else:
            room[rm]['monster'] = False
    print('Start the game by going south, into the house...')

def main():
    begin()
    prevcm='rainbowify There is no previous command.'
    while True:
        try:
            cm = input(">")
        except KeyboardInterrupt:
            try:
                input('\nInterrupt again if you want to quit.')
            except KeyboardInterrupt:
                print('\nAlright, Game Over!')
                exit()
        if "&&" in cm:
            cm = cm.lower().strip().split("&&")
        else:
            cmbak = cm[:].lower().strip()
            cm = []
            cm.append(cmbak)
        for command in cm:
            command = command.strip().split(' ')
            evaluate(command)
        prevcm=' '.join(cm)
if __name__ == '__main__':
    main()

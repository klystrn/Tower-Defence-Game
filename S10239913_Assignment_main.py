#REGINALD HUEY TAN IAN JAY (S10239913) - IT01 (P01)

#============================== IMPORTING RESOURCES ===============================
import random, math, time
import os, asyncio
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #hide pygame initialisation message
from pygame import mixer
from S10239913E_Assignment_gameData import game_vars, defender_list, monster_list, defenders, monsters, alphabet, field, turnEvents

#=============================== GAME FUNDAMENTALS ================================
def initialize_game(): #Initializes all the game variables for a new game
    game_vars['turn'] = 1
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 10
    game_vars['max_threat'] = 10
    game_vars['danger_level'] = 1
def show_main_menu(): #Displays the main menu & all of its options
    print()
    print(f'{" MAIN MENU ":-^55}') #f-formatting to show header of main menu
    print("1. Start new game       2. Load saved game")
    print("3. Alter game options   4. Show unit information")
    print("5. Timed Game Mode      6. Quit game")
    print('-' * 55) #f-formatting to end start of main menu
def show_combat_menu(game_vars, back): #Displays the main menu & all of its options
    if back == False:
        print(f'  Turn {game_vars.get("turn")} \t Threat = {threat_bar(game_vars)} \t Danger Level = {game_vars.get("danger_level")}') #Displays game status: Turn, Threat Metre, Danger Level
        print(f'  Gold = {game_vars.get("gold")} \t Monsters killed = {game_vars.get("monsters_killed")}/{game_vars.get("monster_kill_target")}') #Displays game status: Gold, Number of Monster Kills out of the Target Monster Kills
        print()
    print(f'{" COMBAT MENU ":-^55}') #f-formatting to show header of combat menu
    print("1. Buy unit          2. End turn")
    print("3. Upgrade Archers   4. Upgrade Walls")
    print("5. Save game         6. Quit")
    print('-'*55) #f-formatting to show end of combat menu
def alter_game_options(): #function to display alter game options menu
    print(f'{" ALTER GAME OPTIONS ":-^55}')  # f-formatting to show header of alter game options menu
    print("1. Field Size                  2. Defender Spawn Area")
    print("3. Number of Kills to Win      4. Gold Increase per Turn")
    print('-' * 55)  # f-formatting to end start of alter game options menu
def draw_field(field): #Draws the field of play
    columnHeader, divisor = '', '  +'
    for i in range(game_vars.get('defender_spawn_boundary', 3)): columnHeader += f'{i+1:6}' #concatenates a string to be the headers for the columns (1,2,3)
    fieldLength, fieldWidth = len(field[0]), len(field) #declaring dimensions of field
    for j in range(fieldLength): divisor += '-----+' #for loop to concatenate a string to be the horizontal divisor
    print(f'{columnHeader}\n{divisor}') #outputs the column headers and 1 horizontal divisor
    for lane in range(fieldWidth): #iterates through field with iterator, lane
        nameLane, hpLane = f'{alphabet[lane]} |', f'  |' #declares 2 strings, one for unit name, and one for unit hp
        for tile in range(fieldLength): #nested loop to iterate through lane with iterator, tile
            if field[lane][tile] == [None, None]: #checks that tile is emptyr
                nameLane += f'{"":5}|' #adds 5 blank spaces to unit name string since tile is empty
                hpLane += f'{"":5}|' #adds 5 blank spaces to unit hp string since tile is empty
            else: #tile is not empty
                nameLane += f'{field[lane][tile][0]:5}|' #adds name to unit name string using f-formatting to centralise name in string
                hpLane += f'{field[lane][tile][1]:^5}|' #adds hp to unit hp string using f-formatting to centralise hp in string
        print(f'{nameLane}\n{hpLane}\n{divisor}') #outputs the unit name string, creates a new line, outputs the unit hp string, creates a new line, outputs 1 horizontal divisor
def quit_game():
    #Function prints a default message whenever game is quit
    print('\nTHANKS FOR PLAYING! :)')
    print('CLOSING GAME', end='')
    time.sleep(0.25)
    for i in range(3): #loop to add a . to "CLOSING GAME" every 0.25s, gives a sense of progression
        print('.', end='')
        time.sleep(0.25)
    print()
    quit() #Exits code in interpreter

#================================ GAME SAVE & LOAD ================================
def save_game(): #Saves the game in the file 'save.txt'
    save_file = open("save.txt", "w")
    save_file.write(f'{game_vars["turn"]+1}\n') #stores game variable "turn" in 'save.text'
    save_file.write(f'{game_vars["monster_kill_target"]}\n') #stores game variable "monster_kill_target" in 'save.text'
    save_file.write(f'{game_vars["monsters_killed"]}\n') #stores game variable "monsters_killed" in 'save.text'
    save_file.write(f'{game_vars["num_monsters"]}\n') #stores game variable "num_monsters" in 'save.text'
    save_file.write(f'{game_vars["gold"]}\n') #stores game variable "gold" in 'save.text'
    save_file.write(f'{game_vars["threat"]}\n') #stores game variable "threat" in 'save.text'
    save_file.write(f'{game_vars["max_threat"]}\n') #stores game variable "max_threat" in 'save.text'
    save_file.write(f'{game_vars["danger_level"]}\n') #stores game variable "danger_level" in 'save.text'

    for lane in range(len(field)): #for loop that iterates through each tile in field, saving the tile data in a specified format
        for tile in range(len(field[0])):
            if field[lane][tile] is not None:
                save_file.write(f'{lane}|{tile}|{field[lane][tile][0]}|{field[lane][tile][1]}')
                save_file.write('\n')

    save_file.close()
    print("GAME SAVED")
def load_game(game_vars): #Loads the game data from 'save.txt'
    filename = 'save.txt'
    save_file = open(filename, "r")
    firstLine = save_file.readline() #stores first line of file in case it needs to be used multiple times
    if firstLine == '': #check if file is empty
        print(f'FILE <{filename}> IS EMPTY')
        quit_game()
    else:
        print('LOADING SAVED GAME', end='')
        time.sleep(0.25)
        for i in range(3): #loop to add a . to "LOADING SAVED GAME" every 0.25s, gives a sense of progression
            print('.', end='')
            time.sleep(0.25)
        print()
        game_vars["turn"] = int(firstLine) #stores game variable "turn" in game_vars dictionary
        game_vars["monster_kill_target"] = int(save_file.readline()) #stores game variable "monster_kill_target" in game_vars dictionary
        game_vars["monsters_killed"] = int(save_file.readline()) #stores game variable "monsters_killed" in game_vars dictionary
        game_vars["num_monsters"] = int(save_file.readline()) #stores game variable "num_monsters" in game_vars dictionary
        game_vars["gold"] = int(save_file.readline()) #stores game variable "gold" in game_vars dictionary
        game_vars["threat"] = int(save_file.readline()) #stores game variable "threat" in game_vars dictionary
        game_vars["max_threat"] = int(save_file.readline()) #stores game variable "max_threat" in game_vars dictionary
        game_vars["danger_level"] = int(save_file.readline()) #stores game variable "danger_level" in game_vars dictionary

        for line in save_file: #nested loop that iterates line by line through save.txt and obtains field data
            line = line.strip("\n")
            item = line.split("|")
            if [item[2], item[3]] == ['None', 'None']:
                field[int(item[0])][int(item[1])] = [None, None]
            else:
                field[int(item[0])][int(item[1])] = [item[2], item[3]]
    save_file.close()

#=================================== GAME LOGIC ===================================
def navigate_main_menu(choice, field): #Function to navigate main menu
    if choice == 1: #check to start new game
        initialize_game() #reset the game variables data to ensure a new game
        run_game(game_vars, field, monster_list, turnEvents) #begin the game, incrememnting by turns and ending when the monsters killed is equal to the monster kills target
    elif choice == 2: #load most recent saved game
        load_game(game_vars)
        run_game(game_vars, field, monster_list, turnEvents) #begin the game, incrememnting by turns and ending when the monsters killed is equal to the monster kills target
    elif choice == 3:
        alter_game_options()
        while True:
            choice = get_input('alter-game-settings')
            if choice == 1: #change field size
                field = change_field_size()
                draw_field(field)
            elif choice == 2: game_vars['defender_spawn_boundary'] = get_input('defender-spawn-area') #change defender spawn boundary
            elif choice == 3: game_vars['monster_kill_target'] = get_input('kills-to-win') #change number of kills required to win
            elif choice == 4: game_vars['gold_increase_by_turn'] = get_input('gold_increase_by_turn') #change the gold increase every turn
            playGame = get_input('play-game')
            if playGame == True: break #start game or alter more settings
            if playGame == False: alter_game_options()
        run_game(game_vars, field, monster_list, turnEvents) #begin the game, incrememnting by turns and ending when the monsters killed is equal to the monster kills target
    elif choice == 4: unit_information(defenders, monsters)
    elif choice == 5:
        game_vars['timed'] = get_input('timed')
        if game_vars['timed'] == True: print('TIMED MODE - ON')
        else: print('TIMED MODE - OFF')
    elif choice == 6: quit_game() #quit game
def navigate_combat_menu(choice): #Function to navigate combat menu
    if choice == 1: buy_unit() #allows player to choose which unit they want to buy and where to place it
    elif choice == 3: upgrade_archers(game_vars, field, turnEvents)
    elif choice == 4: upgrade_walls(game_vars, field, turnEvents)
    elif choice == 5:
        save_game()  # saves game progress in 'save.txt'
        quit_game()  # calls function to close game
    elif choice == 6: quit_game()  # calls function to close game
    elif choice == 2: pass  # end turn
def check_spawn(game_vars): #function to check spawn requirements
    if game_vars.get('threat') >= game_vars.get('max_threat'): #checks if the threat level is greater than the maximum threat level
        game_vars['threat'] -= game_vars.get('max_threat')
        return True #returns True, which is used to confirm the spawn of monsters when function is called
    elif game_vars['num_monsters'] == 0: return True #returns True, which is used to confirm the spawn of monsters when function is called
    else: return False #returns False, which prevents the spawn of monsters when function is called
def check_place(field, placement):
    selectedLane, selectedTile  = alphabet.index(placement[0]), int(placement[1]) #obtains data on placement argument
    if field[selectedLane][selectedTile-1] == [None, None]: return True #checks if the placement tile is empty
    else: return False
def buy_unit(): #function to handle the purchasing
    i = 0
    for unit, info in defenders.items():  # loop to iterate through defenders dictionary
        print(
            f'{i + 1}. {info.get("name").capitalize():6} {"-" * 15} {info.get("price")} Gold')  # outputs unit number, unit name, and unit cost
        i += 1  # counts for unit number
    print(
        f"{i + 1}. Don't Purchase")  # outputs a 'cancel' option that allows user to not purchase anything and skip the turn
    choice = get_input('buy-unit')  # obtains validated input on which unit to buy
    flag = True
    while True:
        if choice <= len(defender_list) and flag is True:  # checks if user purchased a defender
            unitName = defender_list[choice - 1]
            if game_vars["gold"] < defenders[unitName].get("price"):
                print('NOT ENOUGH GOLD')  # validates if there is enough gold
                show_combat_menu(game_vars, True)
            else:
                game_vars["gold"] -= defenders[unitName].get("price")
                for unit, info in defenders.items():  # loop to obtain unit name and max hp for placing
                    if unitName == unit:
                        hp = f"{info.get('maxHP')}/{info.get('maxHP')}"
                        break
                place_unit(field, unitName, hp)
            break
        elif choice == len(
                defender_list) + 1:  # changes option number for dont purchase depending on number of defenders
            print('NO PURCHASE')  # checks if user cancelled purchase
            show_combat_menu(game_vars, True)  # displays combat menu again
            flag = False
        choice = get_input('combat')  # obtains validated input on combat menu navigation
        if choice == 2: break  # special exception for end turn
        navigate_combat_menu(choice)  # calls function to navigate combat menu
def place_unit(field, unitName, hp): #function to check if user-chosen placement space is available
    while True:
        placement = get_input('place-unit')  # obtains validated input on where to place unit
        if check_place(field, placement) == True:  # if True, defender will be placed there
            selectedLane, selectedTile = alphabet.index(placement[0]), int(placement[1])
            field[selectedLane][selectedTile - 1] = [unitName, hp]  # changes placement tile data
            break
        else:
            print('POSITION ERROR: POSITION ALREADY OCCUPIED')  # outputs error message if the placement tile is already occupied
def spawn_monster(field, monster_list, turnEvents): #function to spawn in monsters
    while True: #infinite loop to check if position is empty
        spawnPosition = random.randint(0,len(field)-1) #generates a random number within the number of lanes
        placement = f'{alphabet[spawnPosition]}{len(field[0])}'
        if check_place(field, placement) == True: #calls function, check_place(), to verify that placement tile is empty
            selectedLane  = alphabet.index(placement[0])
            monsterName = monster_list[random.randint(0,len(monster_list)-1)] #generates a monster from monster_list
            hp = f"{monsters[monsterName].get('maxHP')}/{monsters[monsterName].get('maxHP')}" #generates the monster at full HP
            field[selectedLane][-1] = [monsterName, hp] #replaces the placement tile with randomly generated monster name and monster HP
            break
    game_vars['num_monsters'] += 1 #adds to the total number of monsters alive on the field
    turnEvents += [f'A monster has spawned in Lane {alphabet[selectedLane]}'] #adds string to turnEvents to be output as a turn event
def monster_advance(field, turnEvents): #function that advances monster & deals damage
    for lane in field: #iterates through field
        for tile in lane:
            if tile[0] in monster_list:
                speed = monsters[tile[0]].get('moves') #obtains how many tiles a monster can move at once from monsters dictionary
                monsterPosition = tile
                i, j = lane.index(tile) - speed, lane.index(tile) #intended tile to advance to, current tile
                flag = False
                for index in range(j-i):
                    if lane[i + index][0] in defender_list:
                        flag = True
                        break
                if flag is False and i < 0:
                    game_vars['game_lost'] = True
                    game_vars['monster_end_game'] = monsters[tile[0]].get("name")
                for index in range(j - i):
                    if lane[i + index][0] in defender_list:
                        monsterDamage = random.randint(monsters[tile[0]].get('min_damage'), monsters[tile[0]].get('max_damage'))
                        if tile[0] == 'ZOMBI': #special string for zombies, as they bite
                            turnEvents += [f'{monsters[tile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterPosition)+1} bites {defenders[lane[i][0]].get("name")} for {monsterDamage} damage!'] #adds string to turnEvents to be output as a turn event
                        else:
                            turnEvents += [f'{monsters[tile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterPosition) + 1} hits {defenders[lane[i+index][0]].get("name")} for {monsterDamage} damage!'] #adds string to turnEvents to be output as a turn event
                        unitTotalHp = lane[i+index][1].split('/')
                        unitHp = int(unitTotalHp[0])
                        unitHp -= monsterDamage
                        if unitHp <= 0:  #checks if the defender died to monster
                            turnEvents += [f'{defenders[lane[i+index][0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterPosition) + 1} was slain by {monsters[tile[0]].get("name")}'] #adds string to turnEvents to be output as a turn event
                            lane[i+index] = [None, None] #resets the tile
                            lane[i+index], lane[j] = lane[j], lane[i+index]  # swaps tiles to advance monster
                        else:  #change the defender HP after being attacked
                            unitTotalHp = f'{unitHp}/{defenders[lane[i+index][0]].get("maxHP")}'
                            lane[i+index][1] = unitTotalHp
                    elif lane[i][0] in monster_list and lane[j][0] in monster_list: #monster is blocked by a monster in front
                        if lane[i + index][0] is None:
                            lane[i + index], lane[j] = lane[j], lane[i + index]  # swaps tiles to advance monster
                            turnEvents += [f'{monsters[tile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterPosition) + 1} is blocked from advancing!']  # adds string to turnEvents to be output as a turn event
                            break
                    else:  #advance monster by speed
                        if lane[i][0] in monster_list and lane[j][0] in monster_list: #checks if the unit in tiles are monsters
                            turnEvents += [f'{monsters[tile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterPosition) + 1} is blocked from advancing'] #adds string to turnEvents to be output as a turn event
                        else: #monster can advance
                            if monsters[tile[0]].get("moves") > 1:
                                turnEvents += [f'{monsters[tile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterPosition)+1} advances by {monsters[tile[0]].get("moves")} spaces!'] #adds string to turnEvents to be output as a turn event
                            else:
                                turnEvents += [f'{monsters[tile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterPosition) + 1} advances!'] #adds string to turnEvents to be output as a turn event
                            lane[i + index], lane[j] = lane[j], lane[i + index]  # swaps tiles to advance monster
                            break
def defender_attack(field, turnEvents): #function to handle the attacks of the defenders
    for lane in field: #iterates through field
        defenderName, damageDealt = '', 0 #protects code from crashes due to undeclared variables
        for defenderTile in lane[:game_vars.get('defender_spawn_boundary', 3)]: #iterates through the defenders spawn area
            if defenderTile[0] in defender_list: #checks if the iterated tile is a defender
                if defenderTile[0] == 'CANON':
                    defenderName = defenders[defenderTile[0]].get('name')
                    damageDealt = random.randint(defenders[defenderTile[0]].get('min_damage'), defenders[defenderTile[0]].get('max_damage'))
                    for monsterTile in lane: #iterates through lane to detect first monster
                        if monsterTile[0] in monster_list:  # checks if the iterated tile is a monster
                            if damageDealt != 0 and defenderName != '':  # prevents turn events that show 0 damage was done
                                if defenderName == 'Cannon':
                                    turnEvents += [f'{defenderName} in Lane {alphabet[field.index(lane)]} shot a cannonball at {monsters[monsterTile[0]].get("name")} for {damageDealt} damage!']  # adds string to turnEvents to be output as a turn event
                                if game_vars.get('turn') % 2 == 0:
                                    hp = monsterTile[1].split('/')  # obtains the HP of unit
                                    monsterHp = int(hp[0]) - damageDealt  # subtracts damage dealt from unit HP
                                    if monsterHp <= 0:  # MONSTER DIES
                                        turnEvents += [f'{defenderName} in Lane {alphabet[field.index(lane)]} slays {monsters[monsterTile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterTile) + 1}!']
                                        turnEvents += [f'You gain {monsters[monsterTile[0]].get("reward")} gold for slaying a {monsters[monsterTile[0]].get("name")}!']
                                        game_vars['monsters_killed'] += 1  # increases monsters_killed game variable by 1 every time a monster is killed
                                        game_vars['gold'] += monsters[monsterTile[0]].get('reward')  # increases gold game variable by monster reward every time a monster is killed
                                        game_vars['threat'] += monsters[monsterTile[0]].get('reward')  # increases threat level game variable by monster reward every time a monster is killed
                                        spawn_monster(field, monster_list, turnEvents)  # spawns a new monster to compensate for death of monster
                                        game_vars['num_monsters'] -= 1  # decreases total number of monsters by 1 every time a monster is killed
                                        monsterTile[0], monsterTile[1] = None, None  # resets the tile to be empty
                                    else:
                                        monsterTile[1] = f'{str(monsterHp)}/{hp[1]}'  # changes the tile data to show the monster HP after being damaged
                                    chance = random.randint(0,1)
                                    if chance == 1: #knockback monsters in lane by 1
                                        for index in range(len(lane)):
                                            if lane[index][0] in monster_list and lane[index+1][0] is None:
                                                lane[index+1] = lane[index]
                                                lane[index] = [None, None]
                                                break
                                    break
                else:
                    defenderName = defenders[defenderTile[0]].get('name')
                    damageDealt = random.randint(defenders[defenderTile[0]].get('min_damage'), defenders[defenderTile[0]].get('max_damage'))
                    for monsterTile in lane: #iterates through lane to detect first monster
                        if monsterTile[0] in monster_list: #checks if the iterated tile is a monster
                            if damageDealt != 0 and defenderName != '': #prevents turn events that show 0 damage was done
                                if defenderName == 'Archer': turnEvents += [f'{defenderName} in Lane {alphabet[field.index(lane)]} fires an arrow at {monsters[monsterTile[0]].get("name")} for {damageDealt} damage!'] #adds string to turnEvents to be output as a turn event
                                elif defenderName == 'Ninja': turnEvents += [f'{defenderName} in Lane {alphabet[field.index(lane)]} throws a shuriken at {monsters[monsterTile[0]].get("name")} for {damageDealt} damage!'] #adds string to turnEvents to be output as a turn event
                                else: turnEvents += [f'{defenderName} in Lane {alphabet[field.index(lane)]} deals {damageDealt} damage to {monsters[monsterTile[0]].get("name")}!'] #adds string to turnEvents to be output as a turn event
                            hp = monsterTile[1].split('/') #obtains the HP of unit
                            monsterHp = int(hp[0]) - damageDealt #subtracts damage dealt from unit HP
                            if monsterHp <= 0:  # MONSTER DIES
                                turnEvents += [f'{defenderName} in Lane {alphabet[field.index(lane)]} slays {monsters[monsterTile[0]].get("name")} on {alphabet[field.index(lane)]}{lane.index(monsterTile) + 1}!']
                                turnEvents += [f'You gain {monsters[monsterTile[0]].get("reward")} gold for slaying a {monsters[monsterTile[0]].get("name")}!']
                                game_vars['monsters_killed'] += 1 #increases monsters_killed game variable by 1 every time a monster is killed
                                game_vars['gold'] += monsters[monsterTile[0]].get('reward') #increases gold game variable by monster reward every time a monster is killed
                                game_vars['threat'] += monsters[monsterTile[0]].get('reward') #increases threat level game variable by monster reward every time a monster is killed
                                spawn_monster(field, monster_list, turnEvents) #spawns a new monster to compensate for death of monster
                                game_vars['num_monsters'] -= 1 #decreases total number of monsters by 1 every time a monster is killed
                                monsterTile[0], monsterTile[1] = None, None #resets the tile to be empty
                            else: monsterTile[1] = f'{str(monsterHp)}/{hp[1]}' #changes the tile data to show the monster HP after being damaged
                            break
def run_game(game_vars, field, monster_list, turnEvents): #runs game, each iteration counts as 1 turn
    while True:  #infinite loop, each iteration of the loop counts as 1 turn
        if game_vars.get('game_lost') is True: #checks if game has been lost
            print(f'A {game_vars["monster_end_game"]} has reached the city! All is lost!')
            print('You have lost the game :(')
            quit_game() #calls function to close game

        if game_vars['timed'] is True:
            start_time = time.time()

        if check_spawn(game_vars) is True: spawn_monster(field, monster_list, turnEvents) #spawns a monster if spawn conditions are met
        defender_attack(field, turnEvents) #defenders attack monsters
        game_transcript(turnEvents) #outputs all of the events that occured over the turn

        if game_vars.get('monsters_killed') >= game_vars.get('monster_kill_target'): #checks if game has been won
            print('You have protected the city! You win!')
            quit_game() #calls function to close game

        draw_field(field) #displays updated field
        show_combat_menu(game_vars, False) #displays combat menu

        choice = get_input('combat') #obtains validated user input to use for combat menu navigation
        navigate_combat_menu(choice) #calls function to navigate combat menu
        monster_advance(field, turnEvents)

        if game_vars['timed'] is True:
            end_time = time.time()
            if timer(start_time, end_time) > 12.5:
                if game_vars.get('time_out_chance') == 0:
                    print('You ran out of time!')
                    print('You have lost the game :(')
                    quit_game()  # calls function to close game
                else:
                    game_vars['time_out_chance'] -= 1
                    print('You ran out of time!')
                    print(f'{game_vars.get("time_out_chance")} chances left!')

        game_vars['turn'] += 1 #increases game variable 'turn' by 1
        game_vars['gold'] += game_vars.get('gold_increase_by_turn') #increases game variable 'gold' by the game variable 'gold_increase_by_turn'
        game_vars['threat'] += random.randint(1, game_vars.get('danger_level')) #increases threat level by a random number between 1 and danger level (inclusive)

        if (game_vars.get('turn') % 12) == 0 and (game_vars.get('turn') != 0): #checks if conditions are met for a danger level increase
            danger_level_increase(game_vars, turnEvents)

#=========================== EXTRA & ADVANCED FUNCTIONS ===========================
def timer(start, end): #function to record time taken for something (can only be used one at a time as there is no threading)
    sec = math.floor(end - start)
    return sec
def change_field_size(): #changes number of lanes and number of tiles per lane
    field = []
    dimensions = get_input('change-field-size') #return as a list instead of string in case of double digit dimensions
    fieldWidth, fieldLength = dimensions[0], dimensions[1]
    for i in range(fieldWidth): #iterates the number of times the player defined the number of lanes in field
        row = [] #declares an empty lane for every iteration of a lane
        for j in range(fieldLength): row.append([None, None]) #iterates the number of times the player defined the length of each lane
        field.append(row) #adds the updated lane for every iteration of a lane
    return field #outputs the new player-defined field
def threat_bar(game_vars): #concatenates strings to form the threat bar used in combat menu game status
    threatLevel = '['
    threatLevel += '-' * game_vars.get('threat', 0) #.get() second parameter to handle data file errors
    threatLevel += ' ' * (game_vars.get('max_threat', 10) - game_vars.get('threat', 0)) #.get() second parameter to handle data file errors
    threatLevel += ']'
    return threatLevel
def upgrade_archers(game_vars, field, turnEvents): #function to upgrade archers
    if game_vars['gold'] >= defenders['ARCHR']['upgrade_cost']:
        game_vars['gold'] -= defenders['ARCHR']['upgrade_cost']
        defenders['ARCHR']['maxHP'] += 1
        defenders['ARCHR']['min_damage'] += 1
        defenders['ARCHR']['max_damage'] += 1
        defenders['ARCHR']['upgrade_cost'] += 2
        defenders['ARCHR']['level'] += 1
        turnEvents += [f"Archers upgraded to Level {defenders['ARCHR'].get('level', 1)}!"]  # adds string to turnEvents to be output as a turn event
        for lane in field:
            for tile in lane:
                if tile[0] == 'ARCHR':
                    unitHp = tile[1].split('/')
                    tile[1] = f'{int(unitHp[0])+1}/{defenders["ARCHR"].get("maxHP")}'
    else:
        print('NOT ENOUGH GOLD')
        show_combat_menu(game_vars, True)
def upgrade_walls(game_vars, field, turnEvents): #function to upgrade walls
    if game_vars['gold'] >= defenders['WALL']['upgrade_cost']:
        game_vars['gold'] -= defenders['WALL']['upgrade_cost']
        defenders['WALL']['maxHP'] += 5
        defenders['WALL']['upgrade_cost'] += 2
        defenders['WALL']['level'] += 1
        turnEvents += [f"Walls upgraded to Level {defenders['WALL'].get('level', 1)}!"]  # adds string to turnEvents to be output as a turn event
        for lane in field:
            for tile in lane:
                if tile[0] == 'WALL':
                    unitHp = tile[1].split('/')
                    tile[1] = f'{int(unitHp[0]) + 5}/{defenders["WALL"].get("maxHP")}'
    else:
        print('NOT ENOUGH GOLD')
        show_combat_menu(game_vars, True)
def unit_information(defenders, monsters): #function to output all information on both defenders and monsters
    print(f'{"Defenders":~^55}', end='')
    for unit, unitInfo in defenders.items():
        print()
        print(f'Name: {unitInfo.get("name")}')
        print(f'CodeName: {unit}')
        print(f'Full HP: {unitInfo.get("maxHP")}')
        print(f'Min-Max Damage: {unitInfo.get("min_damage")}-{unitInfo.get("max_damage")} ')
        print(f'Price: {unitInfo.get("price")}')
    print(f'{"Monsters":~^55}', end ='')
    for unit, unitInfo in monsters.items():
        print()
        print(f'Name: {unitInfo.get("name")}')
        print(f'CodeName: {unit}')
        print(f'Full HP: {unitInfo.get("maxHP")}')
        print(f'Min-Max Damage: {unitInfo.get("min_damage")}-{unitInfo.get("max_damage")} ')
        print(f'Speed: {unitInfo.get("moves")}')
        print(f'Rewards: {unitInfo.get("rewards")}')
    print('~' * 55)
def get_input(menuClass): #function to obtain input and validate it, menuClass parameter identifies which input it is obtaining and validating accordingly, depending on function arguments
    x = 1
    while True: #input loop
        if menuClass == 'main' or menuClass == 'combat': choice = input('>>> Your choice: ')
        elif menuClass == 'buy-unit': choice = input('>>> Unit to Purchase: ')
        elif menuClass == 'place-unit': choice = input('>>> Position to Place Unit: ')
        elif menuClass == 'alter-game-settings': choice = input('>>> Your choice: ')
        elif menuClass == 'change-field-size':
            while True:
                fieldWidth = input('>>> Number of Lanes: ')
                if fieldWidth.isnumeric() is not True: print('INPUT TYPE ERROR: NUMBER OF LANES SHOULD BE A NUMBER')
                elif int(fieldWidth) == 0: print('RANGE ERROR: NUMBER OF LANES CANNOT BE 0')
                elif int(fieldWidth) < 3: print('RANGE ERROR: NUMBER OF LANES CANNOT BE LESS THAN 3')
                elif int(fieldWidth) > 26: print('RANGE ERROR: NUMBER OF LANES CANNOT BE GREATER THAN 26')
                else: break
            while True:
                fieldLength = input('>>> Number of Tiles in Each Lane: ')
                if fieldLength.isnumeric() is not True: print('INPUT TYPE ERROR: NUMBER OF TILES PER LANE SHOULD BE A NUMBER')
                elif int(fieldLength) == 0: print('RANGE ERROR: NUMBER OF TILES PER LANE CANNOT BE 0')
                elif int(fieldLength) < 5: print('RANGE ERROR: NUMBER OF TILES PER LANE CANNOT BE LESS THAN 5')  #CHANGE LATER
                else: break
        elif menuClass == 'defender-spawn-area': boundary = input('>>> New Furthest Tile for Defender Spawn: ')
        elif menuClass == 'kills-to-win': kills = input('>>> New Monster Kills Target: ')
        elif menuClass == 'gold_increase_by_turn': gold = input('>>> New Gold Increase per Turn: ')
        elif menuClass == 'play-game': choice = input('>>> Start Game? [Y/n]: ')
        elif menuClass == 'timed': time = input('>>> Timed Mode? [On/Off]: ')
        else: #in case function is called with an incorrect menuClass, prevents crashes with expansion of program
            print('PROGRAM ERROR: "menuClass" VARIABLE UNDETECTED')
            menuClass = input('>>> PLEASE MANUALLY INPUT "menuClass" VARIABLE: ')
            if x == 3:
                print('\nGAME SHUT DOWN DUE TO REPEATED ERROR', end='')
                quit_game()
            x += 1

        if menuClass == 'main': #data validation for main menu
            if not choice.isnumeric():
                print('TYPE ERROR: PLEASE ENTER A NUMBER')
                continue #prevents a ValueError because of the type casting on the next line
            choice = int(choice)
            if not (choice >= 1 and choice <= 6): print('RANGE ERROR: PLEASE ENTER A NUMBER BETWEEN 1 TO 6')
            else:
                output = choice
                break
        elif menuClass == 'combat': #data validation for combat menu
            if not choice.isnumeric():  # check for number
                print('INPUT TYPE ERROR: PLEASE ENTER A NUMBER')
                continue #prevents a ValueError because of the type casting on the next line
            choice = int(choice)
            if not (choice >= 1 and choice <= 6): print('RANGE ERROR: PLEASE ENTER A NUMBER BETWEEN 1 TO 6')
            else:
                output = choice
                break
        elif menuClass == 'buy-unit': #data validation for purchasing defenders
            if choice.isalpha() is True:
                defenderFullName = []
                for unit, info in defenders.items(): defenderFullName += [info.get('name').upper()] #loop to iterate through defenders dictionary and obtain names, capitalise them, and add them to the list, defenderFullName
                if choice.upper() in defenderFullName:
                    output = defenderFullName.index(choice.upper()) + 1
                    break
                else: print("INPUT ERROR: PLEASE ENTER UNIT NAME CORRECTLY")
            elif choice.isnumeric():
                output = int(choice)
                if output <= len(defender_list): break
                elif output == len(defender_list)+1: break
                else: print("INPUT ERROR: PLEASE ENTER UNIT NUMBER CORRECTLY")
        elif menuClass == 'place-unit':  # data validation for placing of purchased defenders
            if not choice.isalnum():
                print('TYPE ERROR: PLEASE ENTER ALPHANUMERIC CHARACTERS')
            else:
                choice = choice.capitalize()
            if len(choice) != 2:
                print('LENGTH ERROR: PLEASE INPUT USING THE FOLLOWING FORMAT: LaneColumn (e.g. A1)')
            elif (not choice[0].isalpha()) and (not choice[1].isnumeric()):
                print('FORMAT ERROR: PLEASE INPUT USING THE FOLLOWING FORMAT: LaneColumn (e.g. A1)')
            elif alphabet.index(choice[0]) >= alphabet.index(alphabet[len(field)]):
                print(f'RANGE ERROR: PLEASE ENSURE LANE LETTER COMES BETWEEN A & {alphabet[len(field)-1]}')
            elif int(choice[1]) > game_vars.get('defender_spawn_boundary', 3):
                print(f'RANGE ERROR: PLEASE ENSURE SELECTED TILE IS BETWEEN 1 & {game_vars.get("defender_spawn_boundary", 3)} (INCLUSIVE)')
            else:
                output = choice
                break
        elif menuClass == 'alter-game-settings':
            if not choice.isnumeric():
                print('TYPE ERROR: PLEASE ENTER A NUMBER')
                continue #prevents a ValueError because of the type casting on the next line
            choice = int(choice)
            if not (choice >= 1 and choice <= 4): print('RANGE ERROR: PLEASE ENTER A NUMBER BETWEEN 1 TO 4')
            else:
                output = choice
                break
        elif menuClass == 'change-field-size':
            output = [int(fieldWidth), int(fieldLength)]
            break
        elif menuClass == 'defender-spawn-area':
            if not boundary.isnumeric():
                print('INPUT TYPE ERROR: PLEASE ENTER A NUMBER')
                continue #prevents a ValueError because of the type casting on the next line
            elif int(boundary) == 0: print('RANGE ERROR: DEFENDER SPAWN BOUNDARY CANNOT BE 0')
            elif int(boundary) < 3: print('RANGE ERROR: DEFENDER SPAWN BOUNDARY CANNOT BE LESS THAN 3')
            else:
                output = int(boundary)
                break
        elif menuClass == 'kills-to-win':
            if kills.isnumeric() is not True: print('INPUT TYPE ERROR: PLEASE INPUT A NUMBER')
            elif int(kills) == 0:
                print('RANGE ERROR: MONSTER KILLS TARGET CANNOT BE 0')
            elif int(kills) < 5:
                print('RANGE ERROR: MONSTER KILLS TARGET CANNOT BE LESS THAN 5')
            else:
                output = int(kills)
                break
        elif menuClass == 'gold_increase_by_turn':
            if gold.isnumeric() is not True: print('INPUT TYPE ERROR: PLEASE INPUT A NUMBER')
            elif int(gold) == 0: print('RANGE ERROR: GOLD INCREASE PER TURN CANNOT BE 0')
            else:
                output = int(gold)
                break
        elif menuClass == 'play-game':
            if choice.isalpha() is not True: print('INPUT TYPE ERROR: PLEASE INPUT "YES" OR "NO"')
            elif choice.upper() == 'YES' or choice.upper() == 'Y':
                output = True
                break
            elif choice.upper() == 'NO' or choice.upper() == 'N':
                output = False
                break
            else: print('INPUT ERROR: PLEASE INPUT "YES" OR "NO"')
        elif menuClass == 'timed':
            if time.isalpha() is not True: print('INPUT TYPE ERROR: PLEASE INPUT "ON" OR "OFF"')
            elif time.upper() == 'ON':
                output = True
                break
            elif time.upper() == 'NO':
                output = False
                break
            else: print('INPUT ERROR: PLEASE INPUT "ON" OR "OFF"')

    return output #returns user input after validation
def game_transcript(turnEvents): #outputs all the events that occured in a single turn
    header = f' TURN {game_vars.get("turn")} EVENTS: ' #f-formatting to make the header for each time function is called
    print(f'{header:~^55}') #f-formatting to show header of turn events
    while turnEvents != []: #iterates through turnEvents while removing elements
        print(turnEvents[0])
        turnEvents.pop(0)
    print('~' * 55) #f-formatting to show end of main menu
def danger_level_increase(game_vars, turnEvents): #changes game data every time danger level increases
    game_vars['danger_level'] += 1 #increases game variable 'danger_level' by 1 every time the function is called
    turnEvents += ['The evil grows stronger!'] #adds string to turnEvents to be output as a turn event
    for mob in monster_list: #iterates through monster_list to obtain each element inside
        monsters[mob]['maxHP'] += 1 #increases every monsters maximum HP by 1 every time the function is called
        monsters[mob]['min_damage'] += 1 #increases every monsters minimum damage by 1 every time the function is called
        monsters[mob]['max_damage'] += 1 #increases every monsters maximum damage by 1 every time the function is called
        monsters[mob]['reward'] += 1 #increases every monsters reward by 1 every time the function is called
async def play_music(): #asynchronous function to play background music 'evolution.mp3'
    mixer.init()
    mixer.music.load("evolution.mp3")
    mixer.music.set_volume(0.15)
    mixer.music.play(10)

#================================= START PROGRAM ==================================
asyncio.run(play_music()) #running the asynchronous function for background music
print(f'{"="*55}\n{"Desperate Defenders":^55}\n{"Defend the city from undead monsters!":^55}\n{"="*55}') #display start of game header
while True:
    show_main_menu()  # show start menu options
    choice = get_input('main') #obtain validated input to use as navigation
    navigate_main_menu(choice, field)

#==================================== CREDITS =====================================
#Music I Used: https://www.bensound.com/free-music-for-videos

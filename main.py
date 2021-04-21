from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# print("\n\n")
# print("NAME                     HP                                         MP")
# print("                         -------------------------                  ----------")
# print("Ben:         460/460     |████████████████████████|         65/65   |█████████|")

# print("\n\n")

# create black magic
fire  = Spell("Fire", 25, 600, "black")
thunder  = Spell("Thunder", 25, 600, "black")
blizzard  = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake  = Spell("Quake", 15, 140, "black")

# create white magic
cure = Spell("Cure", 25, 600, "white")
cura = Spell("Cura", 50, 1200, "white")



#create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 Hp", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
Megaelixer = Item("Megaelixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item" : potion, "quantity" : 15}, {"item" : hipotion, "quantity" : 5},
                {"item" : superpotion, "quantity": 5}, {"item" : elixer, "quantity" : 5},
                {"item" : Megaelixer, "quantity": 2}, {"item" : grenade, "quantity": 5}]


# instantiate people
player1 = Person("Ben ", 4160, 800, 120, 34, player_spells, player_items)
player2 = Person("Paul", 4160, 800, 120, 34, player_spells, player_items)
player3 = Person("Trev", 3089, 800, 120, 34, player_spells, player_items)


enemy2 = Person("Imp1   ", 1250, 130, 560, 325, enemy_spells, [])
enemy1 = Person("Magnus ", 18200,700,525,25, enemy_spells, [])
enemy3 = Person("Imp2   ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i=0


while running:
    print("=========================================")

    print("NAME                     HP                                      MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    print(bcolors.FAIL +bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

    for player in players:  

        player.choose_action()
        choice = input("choose action")
        print ("you chose", choice)
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies [enemy].take_damage(dmg)
            print("you attacked " + enemies[enemy].name + "for", dmg, "points of damage. Enemy hp:", enemies[enemy].get_hp())

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]


        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = player.magic[magic_choice].generate_damage()
            current_mp = player.get_mp()
            
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot  enough magic points\n"+ bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal (magic_dmg)
                print (bcolors.OKBLUE + "\n" + spell.name + " heals for " , str(magic_dmg), "HP" + bcolors.ENDC)
            
            elif spell.type == "black":
                
                enemy = player.choose_target(enemies)

                enemies [enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals ", str(magic_dmg), " Points of damage to " + enemies[enemy].name +bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]


        elif index == 2:
            player.choose_item()
            item_choice = int (input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.OKFAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name +  "heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixer":
                if item.name == "Megaelixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "fully restored HP/MP" + bcolors.ENDC)
                
            
            elif item.type == "attack":

                enemy = player.choose_target(enemies)

                enemies [enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + "deals", str(item.prop), "Points of damage to" + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    # check if battle is over 

    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "you win!" + bcolors.ENDC)
        running = False
        
    # check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "you died! enemy wins!" + bcolors.ENDC)
        running = False 

    print("\n")
    # Enemy attack  phase
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0:
            # Choose  attack 
            target = random.randrange(0,3)
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name + " attacked" +  players[target].name +  "for", enemy_dmg, "points of damage. Enemy hp:", enemy.get_hp())

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal (magic_dmg)
                print (bcolors.OKBLUE  + spell.name + " heals "+ enemy.name +"for " , str(magic_dmg), "HP" + bcolors.ENDC)
            
            elif spell.type == "black":
                
                target = random.randrange(0,3)

                players [target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name + spell.name + " deals ", str(magic_dmg), " Points of damage to " + players[target].name +bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[player]


    print("--------------------------------------")
    # print("Enemy hp:", bcolors.FAIL + str(enemies[enemy].get_hp()) + "/" + str (enemies[enemy].get_max_hp()) + bcolors.ENDC + "\n")
    # print("your Hp:", bcolors.OKGREEN +str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC + "\n")
    # print("your Mp:", bcolors.OKBLUE +str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC + "\n")



    


    # running = False

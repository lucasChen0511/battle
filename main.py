from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 400, 1200, "black")
thunder = Spell("Thunder", 450, 1224, "black")
blizzard = Spell("Blizzard", 380, 1196, "black")
meteor = Spell("Meteor", 420, 1210, "black")
quake = Spell("Quake", 520, 1290, "black")

# Create White Magic
cure = Spell("Cure", 520, 1220, "white")
cura = Spell("Cura", 580, 1500, "white")

# Create some Item
potion = Item("Potion", "potion", "Heal 50 HP", 250)
hipotion = Item("Hi-Potion", "potion", "Heal 100 HP", 300)
superpotion = Item("Super Potion", "potion", "Heal 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 1500)


# Instantiate People
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

player1 = Person("Valos:", 3260, 1200, 500, 34, player_spells, player_items)
player2 = Person("Peter:", 4160, 3500, 600, 34, player_spells, player_items)
player3 = Person("Nick:", 3509, 2000, 300, 34, player_spells, player_items)
enemy = Person("Boss :", 9200, 6000, 700, 25, [], [])

players = [player1, player2, player3]

runing = True
i = 0

while runing:
    print("======================")
    print("NAME              HP                                                               MP")
    for player in players:
        player.get_status()
    print()
    enemy.get_enemy_status()

    for player in players:
        player.choose_action()
        choice = input("  Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You attacked for ", dmg, "points of damage.")
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("  Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_choice)
                print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage" + bcolors.ENDC)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("  Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage", bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemy.generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!", bcolors.ENDC)
        runing = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        runing = False

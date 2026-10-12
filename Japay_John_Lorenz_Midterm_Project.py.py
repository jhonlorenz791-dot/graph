import random
from collections import deque

class Room:
    """Node for Binary Tree - Dungeon/Map Structure"""
    def __init__(self, name, description, level=0):
        self.name = name
        self.description = description
        self.left = None
        self.right = None
        self.level = level
        self.is_exit = False
        self.has_item = None
        self.has_enemy = None
        self.visited = False
        self.is_locked = False

class DungeonGame:
    def __init__(self):
        # Data Structures
        self.current_room = None
        self.inventory = []  
        self.history = []    
        self.events = deque() 
        
        self.player_hp = 100
        self.keys = 0
        self.escaped = False
        self.turns = 0
        
        self.build_dungeon()
        self.current_room = self.root
        self.current_room.visited = True
        
       
        self.events.append("Goblin")
        self.events.append("Skeleton")
        self.events.append("Dark Mage")
        self.events.append("Orc")
        self.events.append("Troll")
    
    def build_dungeon(self):
        """Build 10-level deep dungeon"""
        rooms = {}
        
        
        room_names = [
            # Level 0
            ("Entrance", "Dark entrance with stone steps"),
            # Level 1
            ("Hall", "Long hallway with torches"),
            ("Chamber", "Large chamber with pillars"),
            # Level 2
            ("Library", "Old books and dust"),
            ("Armory", "Rusty weapons hang"),
            ("Kitchen", "Cold ovens and pots"),
            ("Barracks", "Old beds and lockers"),
            # Level 3
            ("Treasury", "Gold and jewels!"),
            ("Cells", "Rows of empty cells"),
            ("Altar", "Dark altar with candles"),
            ("Vault", "Heavy iron door"),
            ("Crypt", "Sarcophagi and bones"),
            # Level 4
            ("Throne Room", "Ancient throne stands"),
            ("Dragon Lair", "Smells of fire"),
            ("Temple", "Stone gods watch"),
            ("War Room", "Maps on the table"),
            ("Garden", "Dead plants and thorns"),
            # Level 5
            ("Catacombs", "Long tunnels of bones"),
            ("Mage Tower", "Magic books and orbs"),
            ("Prison", "Iron bars and chains"),
            ("Forge", "Cold anvils and hammers"),
            # Level 6
            ("Shadow Realm", "Darkness everywhere"),
            ("Elemental Chamber", "Fire and ice swirl"),
            ("Observatory", "Stars on the ceiling"),
            # Level 7
            ("Abyss", "Bottomless pit below"),
            ("Sanctuary", "Peaceful and quiet"),
            # Level 8
            ("Nexus", "Center of all magic"),
            # Level 9
            ("Ascension Chamber", "Glowing with power"),
            # Level 10
            ("Exit", "DOOR TO FREEDOM!", True)
        ]
        
        
        def create_rooms(index=0):
            if index >= len(room_names):
                return
            name, desc, *exit_flag = room_names[index]
            room = Room(name, desc, min(index // 3, 10))
            if exit_flag and exit_flag[0]:
                room.is_exit = True
                room.is_locked = True
            rooms[name] = room
            create_rooms(index + 1)  
        
        create_rooms()
        
       
        self.root = rooms["Entrance"]
        
        # Level 1
        self.root.left = rooms["Hall"]
        self.root.right = rooms["Chamber"]
        
        # Level 2
        rooms["Hall"].left = rooms["Library"]
        rooms["Hall"].right = rooms["Armory"]
        rooms["Chamber"].left = rooms["Kitchen"]
        rooms["Chamber"].right = rooms["Barracks"]
        
        # Level 3
        rooms["Library"].left = rooms["Treasury"]
        rooms["Library"].right = rooms["Cells"]
        rooms["Armory"].left = rooms["Altar"]
        rooms["Armory"].right = rooms["Vault"]
        rooms["Kitchen"].left = rooms["Crypt"]
        rooms["Kitchen"].right = rooms["Throne Room"]
        
        # Level 4
        rooms["Treasury"].left = rooms["Dragon Lair"]
        rooms["Treasury"].right = rooms["Temple"]
        rooms["Cells"].left = rooms["War Room"]
        rooms["Cells"].right = rooms["Garden"] 
        
        # Level 5
        rooms["Dragon Lair"].left = rooms["Catacombs"]
        rooms["Dragon Lair"].right = rooms["Mage Tower"]
        rooms["Temple"].left = rooms["Prison"]
        rooms["Temple"].right = rooms["Forge"]
        
        # Level 6
        rooms["Catacombs"].left = rooms["Shadow Realm"]
        rooms["Catacombs"].right = rooms["Elemental Chamber"]
        rooms["Mage Tower"].left = rooms["Observatory"]
        
        # Level 7
        rooms["Shadow Realm"].left = rooms["Abyss"]
        rooms["Elemental Chamber"].right = rooms["Sanctuary"]
        
        # Level 8
        rooms["Abyss"].left = rooms["Nexus"]
        rooms["Sanctuary"].right = rooms["Ascension Chamber"]
        
        # Level 9
        rooms["Nexus"].right = rooms["Exit"]
        
        
        enemy_rooms = [rooms["Hall"], rooms["Armory"], rooms["Cells"], 
                      rooms["Dragon Lair"], rooms["Catacombs"]]
        enemies = ["Goblin", "Skeleton", "Dark Mage", "Orc", "Troll"]
        
        def place_enemies(index=0):
            if index >= len(enemy_rooms):
                return
            enemy_rooms[index].has_enemy = enemies[index]
            place_enemies(index + 1) 
        
        place_enemies()
        
        
        item_rooms = [
            (rooms["Library"], "Ancient Book"),
            (rooms["Treasury"], "Gold Coins"),
            (rooms["Vault"], "Ancient Key"),
            (rooms["Mage Tower"], "Magic Wand"),
            (rooms["Forge"], "Iron Sword")
        ]
        
        def place_items(index=0):
            if index >= len(item_rooms):
                return
            room, item = item_rooms[index]
            room.has_item = item
            place_items(index + 1) 
        
        place_items()
        
       
        rooms["Altar"].has_item = "Ancient Key"
        rooms["Temple"].has_item = "Ancient Key"
        
        
        print(f"Dungeon Depth: {self.get_depth(self.root)} levels")
    
    def get_depth(self, room, depth=0):
        """Verify dungeon depth"""
        if not room:
            return depth
        return max(self.get_depth(room.left, depth+1), 
                  self.get_depth(room.right, depth+1))
    
    def display_status(self):
        """Show player status"""
        print("\n" + "="*40)
        print(f"❤️ HP: {self.player_hp}")
        print(f"🗝️ Keys: {self.keys}/3")
        print(f"⏱️ Turns: {self.turns}")
        print(f"🎒 Items: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print("="*40)
        print(f"📍 {self.current_room.name} (Level {self.current_room.level})")
        print(self.current_room.description)
    
    def show_exits(self):
        """Show available exits"""
        exits = []
        if self.current_room.left:
            exits.append("left")
        if self.current_room.right:
            exits.append("right")
        if self.history:
            exits.append("back")
        
        if exits:
            print(f"🚪 Exits: {', '.join(exits)}")
        else:
            print("🚫 No exits found!")
    
    def show_room_details(self):
        """Show items and enemies in room"""
        if self.current_room.has_item:
            print(f"📦 You see: {self.current_room.has_item}")
        
        if self.current_room.has_enemy:
            print(f"⚠️ Enemy here: {self.current_room.has_enemy}")
        
        if self.current_room.is_exit:
            if self.current_room.is_locked:
                print("🔒 Door is LOCKED! Need 3 keys")
            else:
                print("🔓 Door is UNLOCKED! Type 'escape' to leave!")
    
    def take_item(self):
        """Take item from room"""
        if self.current_room.has_item:
            item = self.current_room.has_item
            self.inventory.append(item)
            print(f"✅ Took {item}")
            self.current_room.has_item = None
            return True
        print("❌ No item here")
        return False
    
    def fight(self):
        """Fight enemy in room """
        if not self.current_room.has_enemy:
            print("❌ No enemy here")
            return True
        
        enemy = self.current_room.has_enemy
        enemy_hp = random.randint(20, 40)
        
        print(f"\n⚔️ FIGHTING {enemy}!")
        
        def combat_round(enemy_hp):
            
            if enemy_hp <= 0:
                print(f"🎉 Defeated {enemy}!")
                self.current_room.has_enemy = None
                if random.random() < 0.3:
                    self.keys += 1
                    print("🔑 Found an Ancient Key!")
                return True
            
            if self.player_hp <= 0:
                print("💀 You died!")
                return False
            
            # Player attack
            damage = random.randint(10, 20)
            if "Iron Sword" in self.inventory:
                damage += 10
                print("⚔️ Iron Sword active!")
            
            enemy_hp -= damage
            print(f"💥 Dealt {damage} damage to {enemy} (HP: {enemy_hp})")
            
            if enemy_hp <= 0:
                print(f"🎉 Defeated {enemy}!")
                self.current_room.has_enemy = None
                if random.random() < 0.3:
                    self.keys += 1
                    print("🔑 Found an Ancient Key!")
                return True
            
            # Enemy attack
            enemy_damage = random.randint(5, 15)
            self.player_hp -= enemy_damage
            print(f"💢 {enemy} deals {enemy_damage} damage!")
            
            if self.player_hp <= 0:
                print("💀 You died!")
                return False
            
            return combat_round(enemy_hp)  
        
        # FIX: Store and return the result
        result = combat_round(enemy_hp)
        return result
    
    def move(self, direction):
        """Move to another room"""
        if direction == "left" and self.current_room.left:
            self.history.append(self.current_room)
            self.current_room = self.current_room.left
            self.current_room.visited = True
            self.turns += 1
            print(f"\n➡️ You move to: {self.current_room.name}")
            return True
        
        elif direction == "right" and self.current_room.right:
            self.history.append(self.current_room)
            self.current_room = self.current_room.right
            self.current_room.visited = True
            self.turns += 1
            print(f"\n➡️ You move to: {self.current_room.name}")
            return True
        
        elif direction == "back" and self.history:
            self.current_room = self.history.pop()
            self.turns += 1
            print(f"\n⬅️ You go back to: {self.current_room.name}")
            return True
        
        print("❌ Can't go that way!")
        return False
    
    def escape(self):
        """Try to escape"""
        if self.current_room.is_exit:
            if not self.current_room.is_locked:
                self.escaped = True
                print("\n🎉🎊 YOU ESCAPED! 🎊🎉")
                return True
            elif self.keys >= 3:
                self.current_room.is_locked = False
                print("🔓 You unlocked the door with 3 keys!")
                print("🎉🎊 YOU ESCAPED! 🎊🎉")
                self.escaped = True
                return True
            else:
                print(f"🔒 Need 3 keys. You have {self.keys}")
        else:
            print("🚪 No exit here")
        return False
    
    def show_map(self):
        """Show discovered rooms"""
        print("\n🗺️ DUNGEON MAP (✨=Visited)")
        self.print_tree(self.root)
    
    def print_tree(self, room, prefix="", is_left=True):
        """Print binary tree map"""
        if room:
            marker = "◉" if room == self.current_room else ("✨" if room.visited else "○")
            print(f"{prefix}{'└── ' if not is_left else '├── '}{marker} {room.name}")
            
            if room.left or room.right:
                self.print_tree(room.left, prefix + ("    " if is_left else "│   "), True)
                self.print_tree(room.right, prefix + ("    " if is_left else "│   "), False)
    
    def play(self):
        """Main game loop """
        print("="*40)
        print("🏰 DUNGEON EXPLORER 🏰")
        print("="*40)
        print("Find 3 Ancient Keys to escape!")
        print("Explore all 10 levels!")
        print("Type 'help' for commands\n")
        
        def game_turn():
            if self.escaped or self.player_hp <= 0:
                return  # Base case: game over
            
            self.display_status()
            self.show_exits()
            self.show_room_details()
            
            cmd = input("\n> ").lower().strip()
            
            if cmd in ["left", "l"]:
                self.move("left")
            elif cmd in ["right", "r"]:
                self.move("right")
            elif cmd in ["back", "b"]:
                self.move("back")
            elif cmd in ["look", "view"]:
                pass
            elif cmd in ["take", "get"]:
                self.take_item()
            elif cmd in ["inventory", "inv", "i"]:
                print(f"🎒 Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
            elif cmd in ["fight", "attack"]:
                # FIX: Check if player died in fight
                if not self.fight():
                    return  # Exit game loop if player died
            elif cmd in ["map", "m"]:
                self.show_map()
            elif cmd in ["escape", "exit"]:
                # FIX: Check if player escaped
                if self.escape():
                    return  # Exit game loop if escaped
            elif cmd == "help":
                print("Commands: left/right/back, look, take, inventory, fight, map, escape, help")
            else:
                print("❌ Unknown command. Type 'help'")
            
            game_turn()  
        
        game_turn()  
        
        # Game over
        if self.escaped:
            print(f"\n⭐ FINAL SCORE: {self.turns} turns, {len(self.inventory)} items")
        else:
            print("\n☠️ GAME OVER")

# Run the game
if __name__ == "__main__":
    game = DungeonGame()
    game.play()
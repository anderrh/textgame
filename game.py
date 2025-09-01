import os
import sys
import json
import random

def main():
  print("\n"*50)
  with open("world_modern.json", "r") as world_file:
    world = json.loads(world_file.read())
  
  game(world)



def get_room_by_id(world, current_room):
  rooms = world["world"]
  for i in range (len(rooms)):
    if (rooms[i]["id"] == current_room):
      return rooms[i]
  assert False



def find_exits(room):
  exits = ""
  
  for exit_name in room['exits']:
    
    
    exits += "\n "
    exits += exit_name
    for specific_exit in room['exits'][exit_name]:
      short_desc = specific_exit["short_desc"]
      exits += " - " + short_desc
  return exits



def describe_room(world,current_room):
  room = get_room_by_id(world,current_room)

  returns = (room['name'] + "\n-----------------\n" +room['description'])
  if ((len (room['exits'])) == 1):
    returns += " There is 1 destination:"
  else:
    returns += (" There are " + str(len (room['exits'])) + " destinations:")
  
  returns += find_exits(room)

  return returns

def d20():
  return random.randrange(1,21)

def has_requires(inventory,requires):
  for i in range (len(requires)):
    found = False
    for j in range (len(inventory)):
      
      if requires[i] == inventory[j]['name'] or requires[i] == inventory[j]['type']:
        found = True
        break
    if not found:
      return False
  return True
      
      


def go(world,inventory,room,direction):
  fail_text = "you can't go that way"
  if direction not in room["exits"]:
    return room["id"] , fail_text
    
  else:
    for path in reversed(room["exits"][direction]):
      if has_requires(inventory,path['requires']):
        return path["to"], ("\n"*5) + path['traversal']
      else:
        fail_text = path['blocked_text']
  return room["id"] , fail_text
  

def difficulty_check(diff:float,advantage:bool,disadvantage:bool):
  first_roll = d20()
  second_roll = d20()
  goal = diff + 10

  if advantage == disadvantage:
    return first_roll >= goal
  if advantage:
    return max(first_roll,second_roll) >= goal
  if disadvantage:
    return min(first_roll,second_roll) >= goal

def find_types(inventory):
  found_types = set()
  for i in range(len(inventory)):
    item = inventory [i]
    type = item['type']
    found_types.add(type)
  return found_types

def game(world):
  current_room = random.choice(world["meta"]["spawn_points"])
  do_exit = False
  inventory = []

  while (not do_exit):
    print(describe_room(world,current_room))
    text = input(">>> ")
    print("\n"* 5)
    if not text:
      continue
    command = text.split()[0].upper()

    if command == "EXIT":
      do_exit = True
    
    if command == "RESTART":
      os.execv(sys.executable, ['python'] + sys.argv)
      return
    
    if command == "GO":
      if not len (text.split()) == 1:
        current_room,text = go(world,inventory,get_room_by_id(world,current_room),text.split()[1].upper())
        print(text + "\n")
      else:
        print("you can't go that way\n")

    if command == "GET":
      room = get_room_by_id(world, current_room)
      item_to_get = " ".join(text.split()[1:])
      has_found = False
      for i in reversed (range (len(room['items']))):
        item = room['items'][i]
        if (item_to_get.upper() == item['name'].upper() ):
          inventory.append(item)
          room['items'] = room['items'][:i]+room['items'][i+1:]
          has_found = True
          print(f"You take the {item['name']}\n")
      if not has_found:
        print (f"You search and you cannot find the {item_to_get}\n") 

    if command == "LOOK":
      my_types = find_types(inventory)
      room = get_room_by_id(world, current_room)
      found_items = []
      inventory_desc = ""
      for i in reversed (range (len(room['items']))):
        item = room['items'][i]
        adv:bool = False
        dis:bool = False
        advantage_if_types = set(item.get('check', {}).get('advantage_if_types' ,[]))
        disadvantage_if_missing_types = set(item.get('check', {}).get('disadvantage_if_missing_types' ,[]))
        if my_types & advantage_if_types == advantage_if_types:
          adv = True
        if disadvantage_if_missing_types and not (my_types & disadvantage_if_missing_types):
          dis = True

        found_item:bool = difficulty_check(item.get('find_difficulty' , 0),adv,dis)
        if item.get('found',False):
          found_item:bool = True
        if found_item or item.get("found"):
          inventory_desc += item["name"]
          inventory_desc += (" - ")
          inventory_desc += item["notice"]
          inventory_desc += ("\n")
          item["found"] = True
      print(inventory_desc)
      

      
                                           



    

      
        
      
    if command == 'I':

      inventory_desc = ""

      for inventory_item in sorted(inventory,key=lambda item: item["name"]):
        
        inventory_desc += inventory_item["name"]
        inventory_desc += (" - ")
        inventory_desc += inventory_item.get('check', {}).get("notes", "Normal item")
        inventory_desc += ("\n")


        
      print (inventory_desc)
      print('')










if __name__ == "__main__":
  main()

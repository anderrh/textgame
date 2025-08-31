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


def go(world,inventory,room,direction):
  if direction not in room["exits"]:
    return room["id"] , "you can't go that way"
  else:
    for path in reversed(room["exits"][direction]):
      # look at requires later
      return path["to"], ("\n"*5) + path['traversal']
  return room["id"] , "you can't go that way"
  



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
      current_room,text = go(world,inventory,get_room_by_id(world,current_room),text.split()[1].upper())
      print(text + "\n")
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
    

      
        
      
    if command == 'I':

      inventory_desc = ""

      for inventory_item in sorted(inventory,key=lambda item: item["name"]):
        
        inventory_desc += inventory_item["name"]
        inventory_desc += (" - ")
        inventory_desc += inventory_item['check']["notes"]
        inventory_desc += ("\n")


        
      print (inventory_desc)
      print('')










if __name__ == "__main__":
  main()

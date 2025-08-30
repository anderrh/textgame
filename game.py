import json
import random

def main():
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
  for (index, exit_name) in enumerate(room['exits']):
    if index == 0:
      exits += exit_name
    else:
      exits += "," + exit_name
  return exits



def describe_room(world,current_room):
  room = get_room_by_id(world,current_room)
  return (room['name'] + "\n-----------------\n" +room['description'] + " There are " + str(len (room['exits'])) + " exits: " + find_exits(room) + '.')



def game(world):
  current_room = random.choice(world["meta"]["spawn_points"])
  do_exit = False
  while (not do_exit):
    print(describe_room(world,current_room))
    do_exit = True








if __name__ == "__main__":
  main()

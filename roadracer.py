from ursina import *  # Import all modules from the ursina library
import random  # Import the random module

app = Ursina()  # Create an instance of the Ursina application
camera.orthographic = True  # Set the camera mode to orthographic
camera.fov = 10  # Set the camera field of view to 10 degrees

# Create the player's car entity with a quad model, car texture, box collider, scale, rotation, position, and color
car = Entity(model='quad', texture='assets\car', collider='box', scale=(2,1), rotation_z=-90, y=-3, color=color.white)

# Create the first road entity with a quad model, road texture, color, scale, and position
road1 = Entity(model='quad', texture='assets\\road',color=color.black, scale=15, z=1)

# Duplicate the first road entity to create the second road entity with the same properties but different position
road2 = duplicate(road1, y=15, color=color.red)

# Store both road entities in a list
pair = [road1, road2]

enemies = []  # empty list to store enemy entities

# Define a function to create new enemy entities with random properties
def newEnemy():
    val = random.uniform(-2,2)  # Generate a random x-position for the enemy
    new = duplicate(car, texture='assets\enemy', x=2*val, y=25, color=color.random_color(),
                    rotation_z=90 if val < 0 else -90)  # Duplicate the player's car with enemy properties
    enemies.append(new)  # Add the new enemy entity to the list
    invoke(newEnemy, delay=0.5)  # Call the newEnemy function recursively with a delay of 0.5 seconds

newEnemy()  # Call the newEnemy function to start creating enemies

# Define the update function that runs every frame
def update():
    car.x -= held_keys['a'] * 5 * time.dt  # Move the car left if the 'a' key is held
    car.x += held_keys['d'] * 5 * time.dt  # Move the car right if the 'd' key is held

    # Move both road entities downwards and reset their position if they go off-screen
    for road in pair:
        road.y -= 6 * time.dt
        if road.y < -15:
            road.y += 30

    # Move each enemy entity downwards and remove it if it goes off-screen
    for enemy in enemies:
        if enemy.x < 0:
            enemy.y -= 10 * time.dt
        else:
            enemy.y -= 5 * time.dt
        if enemy.y < -10:
            enemies.remove(enemy)
            destroy(enemy)

    # Shake the car if it intersects with any other entity
    if car.intersects().hit:
        car.shake()

app.run()  # Run the Ursina application

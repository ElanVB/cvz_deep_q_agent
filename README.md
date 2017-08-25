# Design Process:
1. Write piece of code
2. Write unit tests for code
3. Change code or unit test until both are working correctly
4. Repeat

# Top Down Design:
* Environment - how things react with each other
* Entities - the things that move and react with the Environment
* Update functions - the base functions that control the Entities

# Bottom up implementation
* Coord class - an entity that stores a position
+ function to calculate Distance from other Coord
* Moveable class : extends Coord - an entity that can move
- a range variable that represents the farthest a Moveable can move
+ function that updates the position of a Moveable
* Zombie class : extends Moveable - an entity that moves towards the closest
human
- a radius variable that represents the range of the zombie
+ function that moves Zombie towards closest human
* Human class : extends Coord - an entity that stays in place
* Ash/Shooter : extends Moveable - an entity that can be moved by the player
+ function that moves Shooter towards target Coord
- a radius variable that represents the range of the shooter
* Environment - contains all Entities and facilitates reactions between them
- variables that define the size of the Environment
- variable to store the score of the current state
+ function that updates all Entities
+ function that checks for collisions (in range to shoot / zombie eats human)
+ function that forces all Entities to stay in bounds
+ function to calculate the score

* MacOSX
    * install homebrew: `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)”`
* Python 3.6.1+
    * Ubuntu 16.04
        * `sudo add-apt-repository ppa:jonathonf/python-3.6`
        * `sudo apt-get update`
        * `sudo apt-get python3.6`
        * `sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1`
        * `sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2`
        * `sudo update-alternatives --config python3`
    * MacOSX
        * `brew install python3`
* git
    * Ubuntu 16.04
        * `sudo add-apt-repository ppa:git-core/ppa`
        * `sudo apt-get update`
        * `sudo apt-get install git-all`
    * MacOSX
        * `brew install git`
        * `vim .bash_profile` - add line `PATH="/usr/local/Cellar/git/2.14.1/bin/:$PATH”` where 2.14.1 is the version of git
        * need to restart / new-window terminal
* pip3
    * Ubuntu 16.04
        * `sudo apt-get update`
        * `sudo apt-get -y install python3-pip`
    * MacOSX
        * comes installed with python 3.4+
    * update pip: `sudo pip3 install --upgrade pip`
* all other dependancies can be installed by running the `sudo pip3 install -r requirements.txt` command from the `python` folder
    * keras
        * tensorflow
            * numpy
            * six
            * wheel?
        * scipy
        * scikit-learn
        * pillow
        * h5py
    * pygame

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

# Agent Features:
* Experienced replay
+ Priority sampling?
* Q update delay
* Frame skip learning
* Observation replay loop
* Off-policy learning
* On-policy play
* Multiple state sequence input mode
* Reward limiting?
* Back prop error limiting?
* Try make Q learning continuous with the outputs being GMMs?

+ Tweak reward values to have the agent learn faster?
- Or would it be an achievement to have it learn from un-tweaked rewards?

# Goal:
## Random Play:
* Over 100k games with humans and zombies RV = [1, 100]
+ Average score:  518668.4794
* Over 100k games with humans and zombies = 1
+ Average score: 6.553

# Basic logic:
* Continuous zombie chaser
+ Average score:  9.0587
* Continuous human protector
+ Average score:  9.0967
* Discretized zombie chaser
+ Average score:  8.8774
* Discretized human protector
+ Average score:  8.8816

## DQN Experienced replay:
* 100k frames, lr = 2.5e-4, 10k episodes of test
+ Average score: 6.89
* 100k frames, lr = 1e-3, 10k episodes of test
+ Average score: 6.73

* 552900 episodes of observing lr = 1.53816352537e-4
+ Average score = 6.07, 1k test
+ Average score = 5.9, 10k test

* 445900 episodes of self_taught lr = 1.53816352537e-4
+ Average score = 8.78, 1k test
+ Average score = 8.985, 10k test
+ Average score = 8.827, 10k test
- Action distrabution = [0.1849, 0.1038, 0.1555, 0.2052, 0.3504]

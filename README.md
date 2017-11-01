# Deep Q learning Agent for Code vs Zombies problem (found on CodinGame.com)

## Usage example:
### Use default hyper-parameters:
`from interface import Interface`
`i = Interface()`
`i.train_agent()`
`print("Test score: {}".format(i.test_agent()))`
`i.demo_agent()`

### Use own hyper-parameters:
`from interface import Interface`
`i = Interface(`
    `learning_rate=0.001, hidden_layers=(512, 512, 256, 64),`
    `training_episodes=5000, epsilon_decay=2.25e-4,`
    `max_humans=1, max_zombies=1`
`)`
`i.train_agent(save_file="custom_params", config=[`
	`"network_update_delay",`
	`"frame_skip"`
`])`
`print("Test score: {}".format(i.test_agent()))`
`i.demo_agent()`

## Installation Instructions:
* MacOSX - Package manager
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
* all other dependancies can be installed by running the `sudo pip3 install -r requirements_XXX.txt` command from the `python` folder, where XXX is cpu or gpu
    * keras
        * tensorflow
            * numpy
            * six
            * wheel
        * scipy
        * pyyaml
        * setuptools
        * h5py
	* bleach
	* protobuf
	* tensorflow-tensorboard
	* html5lib
	* markdown
	* werkzeug
    * pygame

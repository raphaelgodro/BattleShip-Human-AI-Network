# BattleShip-Human-AI-Network

A first trimester software engineering final project coded in Python during a rush of exams.

Authors:

 - Guillaume Chevalier
 - Raphaël Gaudreault


## Launching the game
A scientific Python 3 installation is required (e.g.: Anaconda).

### Play against the computer as a human:
> python3 main.py -u Your_username

### Play an accelerated match as the computer, against the computer:
> python3 main.py -u Your_username -c

Sample output:

> COMPUTER Your_username READY TO PLAY

> COMPUTER False READY TO PLAY

> GAME DONE:

> P1 remaining boat count: 2

> P2 remaining boat count: 0

> Number of exchanged shots: 36

### Network

It was possible to play against a friend as yourself or as the computer (AI), but this was using the university's servers, they might be down and we do not have the backend code that managed matches.

### Other configuration

See:
> python3 main.py --help


### Bugs

- We began with camelCase for local variables, but we switched at midway to the end of the project to lower_underscore. We had not the time to fix everything in the end. This project, as sad as it can be, was only worth a small 5% of the course.
- There is no special color for a sank boat on the player 1's self grid on the left side. However, its boats will appear "touched" as expected when hit, so this is not quite important as player 1 can see its boats.
- Playing on network, if an opponent is not found within 3 seconds, the game freezes.


## Screenshots

![Game Screenshot 1](https://github.com/raphaelgodro/BattleShip-Human-AI-Network/blob/master/screenshot_1.png "Game Screenshot 1")

![Game Screenshot 2](https://github.com/raphaelgodro/BattleShip-Human-AI-Network/blob/master/screenshot_2.png "Game Screenshot 2")

![Game Screenshot 3](https://github.com/raphaelgodro/BattleShip-Human-AI-Network/blob/master/screenshot_3.png "Game Screenshot 3")

![Game Screenshot 4](https://github.com/raphaelgodro/BattleShip-Human-AI-Network/blob/master/screenshot_4.png "Game Screenshot 4")

![Game Screenshot 5](https://github.com/raphaelgodro/BattleShip-Human-AI-Network/blob/master/screenshot_5.png "Game Screenshot 5")

![Game Screenshot 6](https://github.com/raphaelgodro/BattleShip-Human-AI-Network/blob/master/screenshot_6.png "Game Screenshot 6")

![Game Screenshot 7](https://github.com/raphaelgodro/BattleShip-Human-AI-Network/blob/master/screenshot_7.png "Game Screenshot 7")

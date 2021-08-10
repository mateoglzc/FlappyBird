# Flappy Bird Game

We all know the infamous game Flappy Bird. In which you take control of a little bird and try to pass through as many green pipes as possible. 

This is a recreation of that game made in Python using the Pygame library. 

With this game I also made a version in which an AI learns to play. The algorithm that I used to train the AI is called NEAT, which is basicly trains neuronetworks to play via evolution. To see more about this version of the game you can click [here](./FlappyAI/README.md)

## Installation

To play the game we first need to download it.

If you would only like to play the game and are not interested in the AI model, just download the folder [Normal Flappy](./NormalFlappy). 

On the other hand if you are only interested in the AI model, just download the folder [Flappy AI](./FlappyAI). 

If you would like to have both feel free to download the whole repository.

To run it you'll need to have python installed. You can install it in the [official python website](https://www.python.org/).

It's important to point out that both the game and the AI require some dependencies to run. This are listed in the requirements text file inside each project. You can install this dependencies using this command.

```powershell
pip install -r requirements.txt
```
Once installed, to run **only** the game you must be inside the **NormalFlappy** folder and run this command in any terminal.

```powershell
python main.py
```

As well, to run **only** the AI game you must be inside the **FlappyAI** folder and run this command in any terminal.

```powershell
python main.py
```

## How to play

[How to play Instructions for Normal Flappy](./NormalFlappy/README.md)

[How to play Instructions for Flappy AI](./FlappyAI/README.md)
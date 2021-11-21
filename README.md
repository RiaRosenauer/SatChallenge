# SatChallenge
Sat-Challenge of HackaTUM2021 (Rohde-Schwarz)
# Project Description
This project prvides a working solution and some intermidiate simulation tools to the Sat-Challenge of HackaTUM2021 (prvided by Rohde-Schwarz). 

# Project Structure
In this repo are two visualisation tools:
1. 2D
- GroundTrack.py: script for plotting the GroundTracks of sattelites with adjustable height
- animation.py: script to create animations of the time evolution of a given sattelite distribution and the area that is covered by those sattelites
2. 3D

# Installation
1. 2D
```console
    foo@bar:~$ git clone https://github.com/RiaRosenauer/SatChallenge.git
    foo@bar:~$ cd SatChallenge/2d
    foo@bar:~$ conda create --name HackaTUM21 --file requirements.yml
    foo@bar:~$ conda activate HackaTUM21
    foo@bar:~$ pip install -r requirements.txt   
```

# Usage
1. 2D
- GroundTrack.py
Starting in line 87 of the file, simply put in the parameters of the satellite track that you would like to see and run the python script. The output
should be something like this:
![2D_Groundtrack](image/2DGroundTrack.png)
- animation.py
In lines 148-159 and 221-226, adjust the animation and sattelite parameters to your needs. Also outcomment the uncomment the functions that are highlighted as different modi according to your wishes.
The output is a mp4 file, looking similar too:
![2D_Ganimation](image/2DAnimation.png)
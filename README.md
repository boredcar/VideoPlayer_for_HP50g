# VideoPlayer_for_HP50g
a video player for hp50g calculator  

bin_image.py: This script convert the normal video file to the .bin file that will be played by player.hp. 
The function new16video() is the only useful function for the up-to-date player.c. 
requirement: numpy matplotlib.pyplot cv2

player.c should be complied by hpgcc2

## How to use:

1.Install: 
	After compile the program with hpgcc2, you'll get the player.hp. Copy the player.hp file to the root of HP50g's SD card.
 
2.Use bin_image.py: 

	Run and input the video file's name and the output .bin file's name. Put the .bin file into the root of HP50g's SD card. 
 
	There is a variable called N in new16video(). One frame from every N frames will be written to the .bin file. Change it to get the appropriate frame rate when playing video on the calculator.
 
3.Play video: 

	Run the player.hp with ARM ToolBox provided by hpgcc. And you will see the screen frozen with the busy signal displayed and the program seemed crashed, but in fact it didn't crash actually. 
 
	Just type in the .bin file's name(example 5.bin ) and you'll see the inputed characters on the upper left corner of the screen. When you finish, press [ENTER]. If everything works just fine, you'll see the video played on the screen. 
 
4.Control the playback speed: 

	Press [LEFT] or [RIGHT] to make the video play slower or faster. Press [UP] to play with the original speed. Press other keys to quit.
 

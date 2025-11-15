Welcome to our workshop! Today we are going to learn about Steganography with a little exercise.
This script lets you hide and extract secret messages inside images using LSB steganography in both the RGB (Red, green blue) and HSV (Hue, Saturation or Value (brightness) components) domains.  
You have to choose one of the images by typing in a number, then choose the channel you want to embed the secret message in, a bit (we recommend lower bits, because they remain hidden, rather than higher bits) and then choose the secret message. 
Then you are able to see the image from the folder you ran the commands I'm going to mention below.
You can also extract the message by doing the same commands as above. 

## Commands to run:
- You first need to have docker updated.
- Then you can pull the image created by us! Run this through your terminal from the Documents folder or create a folder to run them in. 
	docker pull alessandraiorga2003/stego-tool:latest
- Then, you have to run the script:
	- For Windows:
		docker run -it --rm -v %cd%:/app/output alessandraiorga2003/stego-tool:latest
	- For Linux and Mac:
		docker run -it --rm -v "$(pwd):/app/output" alessandraiorga2003/stego-tool:latest

Use these commands to run the steganography tool inside the Docker container, this also saves all generated images in the folder you run the command into (current folder) on the host machine. 

Enjoy embedding messages and extracting them!
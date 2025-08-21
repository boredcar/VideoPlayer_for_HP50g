import numpy as np
import matplotlib.pyplot as plt
import cv2
import struct

FakekeyfBool=True

def byteread(byte):
	bit=[]
	masklist=[128, 64, 32, 16, 8, 4, 2, 1]
	masklist.reverse()
	for i in range(8):
		bit.append((byte&masklist[i])>>(i))
	return bit
def unbyteread(bit):
	result=0
	for i in range(8):
		if bit[i]:
			result+=2**(i)
	return result
def unbyteread16(bit2):
	#print(bit2[0]//16,bit2[1]//16,bit2[0]//16+(bit2[1]//16)**(16))
	return bit2[0]//16+(bit2[1]//16)*(16)
def draw():
	plt.figure(figsize=(8, 6), facecolor='#FFF0F5') 
	data=0
	x,y=13,78*5+5
	posi=11+1040*0
	file=open("r3.bin",'rb')
	file.seek(posi,0)

	perline=np.array([byteread(i) for i in file.read(x)],dtype=np.uint8).ravel()
	data=perline

	#read

	for _ in range(y):
		perline=np.array([byteread(i) for i in file.read(x)],dtype=np.uint8).ravel()
		#print(perline)
		data=np.vstack((data,perline))


	#show
	plt.imshow(data,cmap='gray')
	plt.axis('off')
	plt.show()
	file.close()
def newvideo():

	newmatrix=np.zeros((80,13))

	#print(newmatrix)
	#ffmpeg -i 3.mov -vcodec h264 -acodec mp2 3.mp4
	videoname="./3.mp4"
	file=open("3.bin","wb")
	#file.write(struct.pack('=B',255)*0)
	capture=cv2.VideoCapture(videoname)
	ret,img=capture.read()
	if capture.isOpened():
		while True:
			ret,img=capture.read()
			if not ret:break
			#cv2.imshow("1",img)
			gray_img=255-img
			#gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			#cv2.imshow("1",gray_img)
			#retval,threshold_img = cv2.threshold(gray_img,20,255,cv2.THRESH_BINARY)
			# 自适应阈值
			#adaptive_threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 3)		# 可以用 cv2.imshow() 查看这一帧，也可以逐帧保存
			adaptive_threshold_img=cv2.resize(gray_img,(104,64),interpolation=cv2.INTER_LANCZOS4)
			adaptive_threshold_img=cv2.cvtColor(adaptive_threshold_img,cv2.COLOR_BGR2GRAY)
			adaptive_threshold_img = cv2.adaptiveThreshold(adaptive_threshold_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 3)		# 可以用 cv2.imshow() 查看这一帧，也可以逐帧保存
			#cv2.imshow("q",adaptive_threshold_img)
			#cv2.waitKey()
			matrix=np.array(adaptive_threshold_img)
			print(matrix)
			for y in range(64):
				#print(newmatrix)
				for x in range(13):
					#newmatrix[y][x]=unbyteread(matrix[y][x*8:x*8+8])
					file.write(struct.pack('=B',unbyteread(matrix[y][x*8:x*8+8])))
					#file.write(struct.pack('i',i))
					#print(str(unbyteread(matrix[y][x*8:x*8+8])))
					#print(unbyteread(matrix[y][x*8:x*8+8]))"""
					pass
			plt.imshow(matrix,cmap='gray')
			#plt.axis('off')
			plt.show()
			file.write(struct.pack('=B',255)*13*16)
	else:
		print('failed')
	file.close()
def new16video(videoname,outname):
	N=4

	newmatrix=np.zeros((80,13))
	n=0
	#print(newmatrix)
	#ffmpeg -i 3.mov -vcodec h264 -acodec mp2 3.mp4
	#videoname="./3.mp4"
	file=open(outname,"wb")
	#file.write(struct.pack('=B',255)*0)
	capture=cv2.VideoCapture(videoname)
	ret,img=capture.read()
	if capture.isOpened():
		while True:
			ret,img=capture.read()
			if not ret:break
			if n>0:
				n=n-1
				continue
			gray_img=255-img

			adaptive_threshold_img=cv2.resize(gray_img,(104,64),interpolation=cv2.INTER_LANCZOS4)
			adaptive_threshold_img=cv2.cvtColor(adaptive_threshold_img,cv2.COLOR_BGR2GRAY)
			matrix=np.array(adaptive_threshold_img)

			for y in range(64):
				for x in range(52):
					file.write(struct.pack('=B',unbyteread16(matrix[y][x*2:x*2+2])))
			file.write(struct.pack('=B',255)*13*16*4)
			n=N
	else:
		print('failed')
	file.close()

getvideo=input("the video file(example: ./3.mp4 ): ")
setout=input("the output bin file(example: ./5.bin ): ")
new16video(getvideo,setout)


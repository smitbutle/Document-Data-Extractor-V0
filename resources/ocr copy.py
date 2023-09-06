from PIL import Image
import pytesseract
import cv2
import os
import time
import json

def preprocess(image,args="thresh"):
	# load the example image and convert it to grayscale
	# image = img
	try:
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		if args == "thresh":
			gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	 
		elif args == "blur":
			gray = cv2.medianBlur(gray, 3)
	
	except:
		gray = image

	filename = "{}.jpg".format(os.getpid())
	cv2.imwrite(filename, gray)

	# return gray
	return filename

def ocr(filename):
	
	im = Image.open(filename)
	
	obj= pytesseract.image_to_string(im)
	print(obj)
	os.remove(filename)

def main():
	im = cv2.imread("/home/smit/DEV/MP/Alt/output/fig3.jpg")
	x = preprocess(im)
	ocr(x)

if __name__ == '__main__':
	main()
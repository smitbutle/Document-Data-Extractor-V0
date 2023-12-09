from PIL import Image
import pytesseract
import os
from scan import scanDoc
from pytesseract import Output
import argparse


import cv2

image = cv2.imread("./fig3.jpg")

min_conf=0
     
def ocr(path):
	
	im = Image.open(path)

	current_entity = ""
	merged_entities = []
	prev_word_coords = None
	merged_text = ""
	results = pytesseract.image_to_data(im, output_type= Output.DICT)

	# loop over each of the individual text localizations
	for i in range(0, len(results["text"])):
		# extract the bounding box coordinates of the text region from
		# the current result
		x = results["left"][i]
		y = results["top"][i]
		w = results["width"][i]
		h = results["height"][i]
		# extract the OCR text itself along with the confidence of the
		# text localization
		text = results["text"][i]
		conf = int(results["conf"][i])
		# filter out weak confidence text localizations
		
		if conf > min_conf:
			if prev_word_coords is None:
				prev_word_coords = (x, y, w, h)
				print(prev_word_coords)
				merged_text = text
			else:
				# Check if the current word is adjacent to the previous word
				if x > prev_word_coords[0] + prev_word_coords[2]:
					# Draw bounding box and text for the merged multi-word entity
					cv2.rectangle(image, (prev_word_coords[0], prev_word_coords[1]),
								(x + w, y + h), (0, 255, 0), 2)
					cv2.putText(image, merged_text, (prev_word_coords[0], prev_word_coords[1] - 10),
								cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
					
					prev_word_coords = (x, y, w, h)
					merged_text = text
				else:
					prev_word_coords = (x, y, w + x - prev_word_coords[0], max(h, prev_word_coords[3]))
					merged_text += " " + text
                
	# Display the last merged multi-word entity
	if prev_word_coords is not None:
		cv2.rectangle(image, (prev_word_coords[0], prev_word_coords[1]),(prev_word_coords[0] + prev_word_coords[2], prev_word_coords[1] + prev_word_coords[3]), (0, 255, 0), 2)
		cv2.putText(image, merged_text, (prev_word_coords[0], prev_word_coords[1] - 10),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
			

	if current_entity:
		merged_entities.append(current_entity)
	
	if image is not None and image.shape[0] > 0 and image.shape[1] > 0:
		cv2.imwrite("output.jpg", image)
	else:
		print("Error: Invalid image dimensions")


def main():

	cwd= os.getcwd()


	input_folder_path = cwd+'/input'
	input_folder_path = os.listdir(input_folder_path)

	for i in input_folder_path:
		scanDoc(i)
	
	output_folder_path = cwd+'/output'
	output_folder_contents = os.listdir(output_folder_path)
	
	for i in output_folder_contents:
		print(ocr(output_folder_path+'/'+i))

if __name__ == '__main__':
	main()
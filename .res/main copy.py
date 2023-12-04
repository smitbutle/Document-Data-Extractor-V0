from PIL import Image
import pytesseract
import os
from scan import scanDoc
from pytesseract import Output


import cv2

cwd= os.getcwd()

input_folder_path = cwd+'/input'
input_folder_path = os.listdir(input_folder_path)

output_folder_path = cwd+'/output'
output_folder_contents = os.listdir(output_folder_path)

image = cv2.imread("./fig3.jpg")

min_conf=0
     
def ocr(imgName):
	path= output_folder_path+'/'+imgName
	im = Image.open(path)

	current_entity = ""
	merged_entities = []
	prev_word_coords = None
	merged_text = ""
	results = pytesseract.image_to_data(im, output_type= Output.DICT)
	# obj=pytesseract.image_to_string(im)
	# print(obj)
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
		
	# 	if conf > min_conf:
	# 		if prev_word_coords is None:
	# 			prev_word_coords = (x, y, w, h)
	# 			print(prev_word_coords)
	# 			merged_text = text
	# 		else:
	# 			# Check if the current word is adjacent to the previous word
	# 			if x > prev_word_coords[0] + prev_word_coords[2]:
	# 				# Draw bounding box and text for the merged multi-word entity
	# 				cv2.rectangle(image, (prev_word_coords[0], prev_word_coords[1]),
	# 							(x + w, y + h), (0, 255, 0), 2)
	# 				cv2.putText(image, merged_text, (prev_word_coords[0], prev_word_coords[1] - 10),
	# 							cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
					
	# 				prev_word_coords = (x, y, w, h)
	# 				merged_text = text
	# 			else:
	# 				prev_word_coords = (x, y, w + x - prev_word_coords[0], max(h, prev_word_coords[3]))
	# 				merged_text += " " + text
                
	# # Display the last merged multi-word entity
	# if prev_word_coords is not None:
	# 	cv2.rectangle(image, (prev_word_coords[0], prev_word_coords[1]),(prev_word_coords[0] + prev_word_coords[2], prev_word_coords[1] + prev_word_coords[3]), (0, 255, 0), 2)
	# 	cv2.putText(image, merged_text, (prev_word_coords[0], prev_word_coords[1] - 10),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
		if conf > min_conf:
			# strip out non-ASCII text so we can draw the text on the image
			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()

			if current_entity and ' ' in text:
                # Merge with the current entity if it's a multi-word key
				current_entity += ' ' + text
			else:
                # Start a new entity
				if current_entity:
					merged_entities.append(current_entity)
				current_entity = text
		
			# display the confidence and text to our terminal
			# print("Confidence: {}".format(conf))
			# print("Text: {}".format(text))
			# print("")

			# using OpenCV, then draw a bounding box around the text along
			# with the text itself
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
			

	if current_entity:
		merged_entities.append(current_entity)
	
	if image is not None and image.shape[0] > 0 and image.shape[1] > 0:
		cv2.imwrite("output.jpg", image)
		cv2.imshow("Image", image)
		cv2.waitKey(1)
	else:
		print("Error: Invalid image dimensions")

	return 0
	# return merged_entities
	# print(obj)


def main():
	for i in input_folder_path:
		scanDoc(i)
	for i in output_folder_contents:
		print(ocr(i))

if __name__ == '__main__':
	main()
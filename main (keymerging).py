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
	image = cv2.imread(path)

	prev_word_coords = None
	merged_text = ""
	results = pytesseract.image_to_data(im, output_type= Output.DICT)
	extracted_data=[]

	current_entity = ""
	# loop over each of the individual text localizations
	for i in range(0, len(results["text"])):
		# extract the bounding box coordinates of the text region from
		# the current result
		if results["text"][i] == " " or results["text"][i] == "" or results["text"][i] == "  ":
			continue
		# if i==5:
			# break
		x = results["left"][i]
		y = results["top"][i]
		w = results["width"][i]
		h = results["height"][i]
		# extract the OCR text itself along with the confidence of the
		# text localization
		text = results["text"][i]

		# print(text,x,y,w,h)
		extracted_data.append({
			"word":text,
			"coordinates":(x,y,w,h)
		})
		# conf = int(results["conf"][i])
		# # filter out weak confidence text localizations
		# # print(conf)
		# if conf > min_conf:
		# 	if prev_word_coords is None:
		# 		prev_word_coords = (x, y, w, h)
		# 		# print(prev_word_coords)
		# 		merged_text = text
		# 	else:
		# 		# Check if the current word is adjacent to the previous word
		# 		if x > prev_word_coords[0] + prev_word_coords[2]:
		# 			# Draw bounding box and text for the merged multi-word entity
		# 			cv2.rectangle(image, (prev_word_coords[0], prev_word_coords[1]),
		# 						(x + w, y + h), (0, 255, 0), 2)
		# 			cv2.putText(image, merged_text, (prev_word_coords[0], prev_word_coords[1] - 10),
		# 						cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
					
		# 			prev_word_coords = (x, y, w, h)
		# 			merged_text = text
		# 		else:
		# 			prev_word_coords = (x, y, w + x - prev_word_coords[0], max(h, prev_word_coords[3]))
		# 			merged_text += " " + text
	# for i in extracted_data:
	# 	print(i)

	merged_keys = {}
	current_key = []
	
	for word_info in extracted_data:
		word = word_info['word']
		x1, y1, w, h = word_info['coordinates']
		x2=x1+w
		y2=y1+h
		# Check if the current word is adjacent to the previous word
		if current_key and abs(current_key[-1][1]+current_key[-1][3] - x1) <= 30 :
			current_key.append((word, x1, y1, x2, y2))
		else:
			if current_key:
				merged_key = ' '.join([w[0] for w in current_key])
				merged_keys[merged_key] = current_key
			current_key = [(word, x1, y1, w, h)]

		if prev_word_coords is None:
			prev_word_coords = (x, y, w, h)
			# print(prev_word_coords)
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
	# Process the last current_key
	if current_key:
		merged_key = ' '.join([w[0] for w in current_key])
		merged_keys[merged_key] = current_key

	merged_extracted_data = []
	for merged_key, words_info in merged_keys.items():
		merged_extracted_data.append({'word': merged_key, 'coordinates': words_info[0][1:]})

	# Print or use the merged_extracted_data as needed
	for i in merged_extracted_data:
		print(i)


	prev_word_coords = None
	merged_entities = []


	if prev_word_coords is not None:
		cv2.rectangle(image, (prev_word_coords[0], prev_word_coords[1]),(prev_word_coords[0] + prev_word_coords[2], prev_word_coords[1] + prev_word_coords[3]), (0, 255, 0), 2)
		cv2.putText(image, merged_text, (prev_word_coords[0], prev_word_coords[1] - 10),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
	

	# Display or save the image with bounding boxes and text
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
		ocr(output_folder_path+'/'+i)

if __name__ == '__main__':
	main()
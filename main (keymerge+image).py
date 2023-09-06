from PIL import Image
import pytesseract
import os
from scan import scanDoc
from pytesseract import Output


import cv2
# image = cv2.imread("./fig3.jpg")

min_conf=0
     
def ocr(path, file_name):
	
	im = Image.open(path)
	image = cv2.imread(path)
	print(path,file_name)
	results = pytesseract.image_to_data(im, output_type= Output.DICT)
	extracted_data=[]
	space_width = -1
	# loop over each of the individual text localizations
	for i in range(0, len(results["text"])):
		# extract the bounding box coordinates of the text region from
		# the current result
		if(space_width==-1 and (results["text"][i] == " " or results["text"][i] == "  ")):
			space_width = results["width"][i]
			print(space_width)
		if results["text"][i] == " " or results["text"][i] == "" or results["text"][i] == "  ":
			continue
		# if i==5:
			# break
		x = results["left"][i]
		y = results["top"][i]
		w = results["width"][i]
		h = results["height"][i]
		x2=x+w
		y2=y+h
		# extract the OCR text itself along with the confidence of the
		# text localization
		text = results["text"][i]

		# print(text,x,y,w,h)
		extracted_data.append({
			"word":text,
			"coordinates":(x,y,x2,y2)
		})
		
		# cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		# cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
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
	
	# merged_keys = {}
	merged_keys = []
	current_key = []
	# merged_coordinates = (float('inf'), float('inf'), float('-inf'), float('-inf'))
	for word_info in extracted_data:
		word = word_info['word']
		x1, y1, x2, y2 = word_info['coordinates']

		# Check if the current word is adjacent to the previous word
		if current_key and (abs(current_key[-1][3] - x1) <= 3*space_width and abs(current_key[-1][2] - y1) <= space_width) :
			current_key.append((word, x1, y1, x2, y2))			

		else:
			if len(current_key)>0:
				min_x1 = min(item[1] for item in current_key)
				min_y1 = min(item[2] for item in current_key)
				max_x2 = max(item[3] for item in current_key)
				max_y2 = max(item[4] for item in current_key)

				merged_coordinates = (min_x1, min_y1, max_x2, max_y2)
				merged_key = ' '.join([w[0] for w in current_key])
				
				merged_keys.append( {
				"word":merged_key,
				"coordinates":merged_coordinates
				})
				# print(current_key)
				# print(merged_key)	

			current_key = [(word, x1, y1, x2, y2)]
			
	if len(current_key)>0:
		min_x1 = min(item[1] for item in current_key)
		min_y1 = min(item[2] for item in current_key)
		max_x2 = max(item[3] for item in current_key)
		max_y2 = max(item[4] for item in current_key)
		merged_coordinates = (min_x1, min_y1, max_x2, max_y2)
		merged_key = ' '.join([w[0] for w in current_key])
		
		merged_keys.append( {
		"word":merged_key,
		"coordinates":merged_coordinates
		})
		# print(current_key)
		# print(merged_key)	
	current_key = [(word, x1, y1, x2, y2)]
		
	# print(merged_keys)
	# print(current_key)
	# for i in extracted_data:
	# 	print(i)
	# for key, value in merged_keys.items():
	# 	print(f"{key}: {value}")	
	# for i in merged_keys.values():
	# 	print(i)	

	for i in merged_keys:
		word,x1,y1,x2,y2=i['word'],i['coordinates'][0],i['coordinates'][1],i['coordinates'][2],i['coordinates'][3] 
		cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw a green rectangle
		# Put text label near the box
		cv2.putText(image, word, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

	
	if image is not None and image.shape[0] > 0 and image.shape[1] > 0:
		cv2.imwrite("./output_annoted/"+file_name, image)
		# cv2.imshow("Image", image)
		# cv2.waitKey(1)
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
		ocr(output_folder_path+'/'+i, i)

if __name__ == '__main__':
	main()
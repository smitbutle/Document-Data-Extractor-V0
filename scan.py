import os
import csv
import cv2
import imutils
from skimage.filters import threshold_local
from transform import perspective_transform

def empty_folder(folder_path):
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                empty_folder(item_path)
                os.rmdir(item_path)
    except Exception as e:
        print(f"Error emptying folder: {e}")

def create_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"[Log] Created folder: {folder_path}")
    except Exception as e:
        print(f"Error creating folder: {e}")

def create_csv(csv_path):
    try:
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["filename", "text"])
    except Exception as e:
        print(f"Error creating csv: {e}")


create_folder('./output')
empty_folder('./output')


def scanDoc(image):
    try:
        original_img = cv2.imread("./input/"+image)
        copy = original_img.copy()
        # cv2.waitKey(1)

        ratio = original_img.shape[0] / 500.0
        img_resize = imutils.resize(original_img, height=500)
        # cv2.imshow('Resized image', img_resize)
        # cv2.waitKey(1)

        gray_image = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Grayed Image', gray_image)
        # cv2.waitKey(1)

        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        edged_img = cv2.Canny(blurred_image, 75, 200)
        # cv2.imshow('Image edges', edged_img)
        # cv2.waitKey(1)

        cnts, _ = cv2.findContours(edged_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                doc = approx
                break

        p = []
        for d in doc:
            tuple_point = tuple(d[0])
            cv2.circle(img_resize, tuple_point, 3, (0, 0, 255), 4)
            p.append(tuple_point)
        # cv2.imshow('Circled corner points', img_resize)
        # cv2.waitKey(1)

        warped_image = perspective_transform(copy, doc.reshape(4, 2) * ratio)
        warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Warped Image", imutils.resize(warped_image, height=650))
        # cv2.waitKey(1)

        T = threshold_local(warped_image, 11, offset=10, method="gaussian")
        warped = (warped_image > T).astype("uint8") * 255

        max_allowed_difference = int(original_img.shape[0] * 0.5)

    # Compare dimensions of the original and warped images
        
        if abs(original_img.shape[0] - warped.shape[0]) > max_allowed_difference or \
            abs(original_img.shape[1] - warped.shape[1]) > max_allowed_difference:
            cv2.imwrite('./output/'+image, original_img)
            print("[Success (warp skipped)] ", image)
        else:
            cv2.imwrite('./output/'+image, warped)
            print("[Success] ", image)
    except:
        cv2.imwrite('./output/'+image,original_img)
        print("[Success (preprocessing skipped)] ", image)

    # cv2.imshow("Final Scanned image", imutils.resize(warped, height=650))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


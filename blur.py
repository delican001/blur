from imutils import paths
import argparse
import cv2
import math


def variance_of_laplacian(image):
    # Вычисляет Лаплассиан изображения и возвращает значение
    return cv2.Laplacian(image, cv2.CV_64F).var()


def normalize(value, ethalon):
    return value / ethalon

def activate(value):
    return 1 / (1 + math.exp(-value))

# построение аргументов командной строки и их парсинг
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
                help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=0.65,
                help="focus measures that fall below this value will be considered 'blurry'")
ap.add_argument("-e", "--ethalon", help="path to input ethalon image")

args = vars(ap.parse_args())

ethalon_im = cv2.imread(args["ethalon"])
gray = cv2.cvtColor(ethalon_im, cv2.COLOR_BGR2GRAY)
ethalon = variance_of_laplacian(gray)

for imagePath in paths.list_images(args["images"]):

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    text = "Not Blurry"

    normalized = normalize(fm, ethalon)
    activated = activate(normalized)
    if activated < args["threshold"]:
        text = "Blurry"

    cv2.putText(image, "{}: {:.2f}".format(text, activated), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)
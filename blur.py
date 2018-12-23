from imutils import paths
import argparse
import cv2


def variance_of_laplacian(image):
    # Вычисляет Лаплассиан изображения и возвращает значение
    return cv2.Laplacian(image, cv2.CV_64F).var()


def normalize(value):
    return value / args["normalize"] * 100


# построение аргументов командной строки и их парсинг
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
                help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
                help="focus measures that fall below this value will be considered 'blurry'")
ap.add_argument("-n", "--normalize", type=float, default=100,
                help="value which will be used to normalize")

args = vars(ap.parse_args())

for imagePath in paths.list_images(args["images"]):

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    text = "Not Blurry"

    if fm < args["threshold"]:
        text = "Blurry"

    fm = normalize(fm)

    cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)
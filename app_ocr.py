from PIL import Image
import pytesseract
import db_actions
import numpy as np
import cv2


def img_to_text(img_path):
    """
    reads image from database and returns the text
    :param img_path: path to image
    :return: text from image
    """

    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

    img_data = db_actions.get_image(img_path)
    print("type:", type(img_data[0]))
    # convert the image data to a NumPy array
    np_array = np.frombuffer(img_data[0], np.uint8)
    print("type:", type(np_array))
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    print("type:", type(img))

    if img_data is None:
        return False, ""

    print("checkpoint:")
    print(img.shape)
    print(img.dtype)

    # scale up if smaller
    if img.shape[1] < 900.0:
        scale_factor = 900.0 / img.shape[1]
        img = cv2.resize(img, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LANCZOS4)

    # binarization
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # noise removal
    denoised = cv2.fastNlMeansDenoising(img_bin, h=10, templateWindowSize=7, searchWindowSize=21)

    # get text and cut to only the items part
    text = pytesseract.image_to_string(denoised, config="--psm 1").replace('\n\n', '\n')

    return text
from PIL import Image
import uuid
import os

from subprocess import Popen, PIPE, call

import cv2

def gocr(mat, encoding="utf-8"):
    p = Popen(["gocr049.exe", "-"], stdin=PIPE, stdout=PIPE)
    retval, buf = cv2.imencode(".pgm", mat)
    p.stdin.write(buf)
    p.stdin.close()
    p.wait()
    text = p.stdout.read()
    p.stdout.close()
    return text.decode(encoding).strip("\n")


def ocrad(mat, encoding="utf-8"):
    p = Popen(["ocrad", "-"], stdin=PIPE, stdout=PIPE)
    retval, buf = cv2.imencode(".pgm", mat)

    p.stdin.write(buf)
    p.stdin.close()
    p.wait()
    text = p.stdout.read()
    p.stdout.close()

    return text.decode(encoding).strip("\n")

def cuneiform(mat):
    file_prefix = str(uuid.uuid4())
    image_path = "/tmp/" + file_prefix + ".png"
    data_path = "/tmp/" + file_prefix + ".txt"

    cv2.imwrite(image_path, mat)

    FNULL = open(os.devnull, 'w')
    call(["cuneiform", image_path, "-o", data_path], stdout=FNULL)

    with open(data_path) as file_handler:
        value = file_handler.read()

    os.remove(image_path)
    os.remove(data_path)

    return value.strip("\n")


if __name__ == '__main__':
    from time import time

    image = cv2.imread("joy_of_data.png", 0)
    print("Original text: \"joy of data\"")

    number_of_runs = 10

    for function in [tesseract, gocr, ocrad, cuneiform]:
        pre = time()
        for i in range(number_of_runs):
            result = function(image)
        print("{}: {}, took {}s for {} runs".format(function.__name__, result, time() - pre, number_of_runs))

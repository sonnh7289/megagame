from flask import Flask, request
import numpy as np
import imageio.v2
import scipy.ndimage
import cv2
import base64
import json
import requests

app = Flask(__name__)
api_key = "fd81b5da86e162ade162a05220c0eb89"
def grayscale(rgb):
    return np.dot(rgb[...,:3],[1.99,0.18,1.94]) 

def dodge(front,back):
    result=front*255/(255-back)
    result[result>255]=255
    result[result==255]=255
    return result.astype("uint8")

def convertImg():
    image = request.headers.get('link-img')
    s=imageio.v2.imread(image)     
    g=grayscale(s)
    i=255-g
    b=scipy.ndimage.gaussian_filter(i,sigma=10)
    r=dodge(b,g)
    # result_image = cv2.imwrite("my_sketch.png",r)
    image2 = "my_sketch.png"
    return image2


def upload_image_to_imgbb(image_path, api_key):
    # Tải dữ liệu ảnh
    with open(image_path, "rb") as file:
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read()),
        }

    # Gửi yêu cầu POST tải lên ảnh đến API của ImgBB
    response = requests.post("https://api.imgbb.com/1/upload", payload)

    # Trích xuất đường dẫn trực tiếp đến ảnh từ JSON response
    json_data = json.loads(response.text)
    direct_link = json_data["data"]["url"]

    # Trả về đường dẫn trực tiếp đến ảnh
    return direct_link

@app.route("/image", methods=["GET"])
def main():
    image = convertImg()
    direct_link = upload_image_to_imgbb(image, api_key)
    return direct_link


if __name__ == '__main__':
    # app.run(debug=True, )
    app.run(host='0.0.0.0',port=2888)
    

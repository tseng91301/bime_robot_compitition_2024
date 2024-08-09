import requests
from PIL import Image
from io import BytesIO

def download_image(url, save_path):
    # 下載圖片
    response = requests.get(url)
    if response.status_code == 200:
        # 讀取圖片內容
        image = Image.open(BytesIO(response.content))
        # 將圖片保存為JPG格式
        image.save(save_path, 'JPEG')
        print(f"Image saved as {save_path}")
    else:
        print("Failed to retrieve image")
        raise Exception


# 示例用法
images_link = open("rooster_img_url").read().split('\n')
current_num = 0
for v in images_link:
    try:
        download_image(v, f"images/rooster_{current_num}.jpg")
        current_num += 1
    except:
        pass


# 示例用法
images_link = open("starling_img_url").read().split('\n')
current_num = 0
for v in images_link:
    try:
        download_image(v, f"images/starling_{current_num}.jpg")
        current_num += 1
    except:
        pass

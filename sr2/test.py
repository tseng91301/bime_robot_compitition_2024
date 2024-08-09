import os

def list_files(directory):
    try:
        # 列出資料夾底下的所有文件
        files = os.listdir(directory)
        return files
    except FileNotFoundError:
        return "找不到指定的資料夾"
    except PermissionError:
        return "沒有權限訪問指定的資料夾"

# 使用範例
directory = 'coco128/coco128/labels/train2017'
files = list_files(directory)
print(files)

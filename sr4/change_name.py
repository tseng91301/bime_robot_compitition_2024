import os

title = "chicken_starling_goose"
dir = "images"

files = os.listdir(dir)
now_num = 0
for filename in files:
    old_file_path = os.path.join(dir, filename)
    if os.path.isfile(old_file_path):
        new_filename = f"{title}_{now_num}.jpg"
        new_file_path = os.path.join(dir, new_filename)
        os.rename(old_file_path, new_file_path)
        print(f"Renamed: {filename} -> {new_filename}")
        now_num += 1

import os

# label txt file path
path = 'datasets/coco128/labels/train2017'

def list_files(directory):
    try:
        # 列出資料夾底下的所有文件
        files = os.listdir(directory)
        return files
    except FileNotFoundError:
        print("找不到指定的資料夾")
        exit()
    except PermissionError:
        print("沒有權限訪問指定的資料夾")
        exit()

def read_label_file(file_in):
    with open(file_in, 'r') as f:
        file_str = f.read()
        file_arr1 = file_str.split("\n")
        out_arr = []
        for v in file_arr1:
            if v is None or (v==""):
                continue
            t1 = v.split(" ")
            out_arr.append(t1)
        f.close()
        return out_arr


# search file named <name>_{number}.txt
names = ['chickHealth_goose_frame']

change_from_to = [[0, 82], [1, 83], [2, 84]]

file_names = list_files(path)

for v1 in file_names:
    for v2 in names:
        if v2 in v1:
            data_arr1 = read_label_file(os.path.join(path, v1))
            for i3, v3 in enumerate(data_arr1):
                new_v = v3
                for v4 in change_from_to:
                    if v3[0] == str(v4[0]):
                        print(f"Changed from {v3[0]} to {v4[1]}")
                        new_v[0] = str(v4[1])
                data_arr1[i3] = new_v
            with open(os.path.join(path, v1), 'w') as f_o:
                output_str = ""
                t2 = 0
                for v3 in data_arr1:
                    if(t2):
                        output_str += "\n"
                    t3 = 0
                    for v4 in v3:
                        if(t3):
                            output_str += " "
                        output_str += v4
                        t3 += 1
                    t2 += 1
                f_o.write(output_str)
                f_o.close()

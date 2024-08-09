import cv2
import os

def video_to_frames(video_path, video_ext, output_folder, interval):
    # 創建輸出文件夾（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 讀取影片
    cap = cv2.VideoCapture(f"video/{video_path}.{video_ext}")
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if(frame_count % interval != 0):
            continue

        print(f"frame_count: {frame_count}")

        # 將幀保存為 PNG 圖像
        frame_filename = os.path.join(output_folder, f"{video_path}_frame_{frame_count:04d}.png")
        print(frame_filename)
        cv2.imwrite(frame_filename, frame)

    cap.release()
    print(f"Video has been converted to {frame_count} PNG images in the folder {output_folder}.")

# 使用範例
# video_names = ['blue']
video_names = ['blue', 'green', 'purple', 'yellow']
video_ext = "mp4"
# video_path = 'video/blue.mp4'
output_folder = 'output_frames'
for v in video_names:
    video_to_frames(f"{v}", video_ext, output_folder, 20)


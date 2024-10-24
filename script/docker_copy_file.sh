# 要將一個檔案從你的本地系統複製到 Docker 容器中，你可以使用 docker cp 命令。這個命令允許你將檔案或目錄從本地系統複製到執行中的容器中，或從容器中複製到本地系統。

# 複製檔案到 Docker 容器
# 假設你有一個檔案 myfile.txt，需要複製到容器內的 /path/in/container 目錄中。這裡是具體的步驟：

# 確認容器的名稱或ID
# 使用 docker ps 命令查看執行中的容器名稱或ID。
docker ps

# 使用 docker cp 命令
# 假設容器名稱為 mycontainer，你可以使用以下命令將檔案 myfile.txt 複製到容器中的指定目錄 /path/in/container：
docker cp myfile.txt dakuo:/root/jetson_python


# 例子：
# 如果你想將本地的 config.conf 檔案複製到容器的 /etc/myapp/ 目錄中，且容器名稱為 myapp_container，你可以這樣做：
docker cp config.conf myapp_container:/etc/myapp/


# 複製整個目錄
# 如果你想要複製整個目錄到 Docker 容器中，可以指定目錄路徑：
docker cp /local/path/to/directory mycontainer:/path/in/container


# 如果你需要將檔案從 Docker 容器複製回本地，也可以使用相同的命令，但將容器路徑作為源：
docker cp mycontainer:/path/in/container/myfile.txt /local/path/to/destination
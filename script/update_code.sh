sudo docker start dakuo
sudo docker exec -it dakuo /bin/bash -c "rm -rf /ultralytics/main_code/*"
sudo docker cp ~/main/jetson_python/. dakuo:/ultralytics/main_code/


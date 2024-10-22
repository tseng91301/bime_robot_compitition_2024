sudo docker start dakuo
sudo docker exec -it dakuo /bin/bash -c "rm -rf /ultralytics/main_code/*"
sudo docker cp ~/main/jetson_python/*:/ultralytics/main_code/


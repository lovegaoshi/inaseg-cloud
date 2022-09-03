# required softwares

biliup-rs
yt-dlp
aria2
ffmpeg
docker

# docker command

sudo docker pull gaoshi/inaseg:gpu

git clone https://github.com/lovegaoshi/inaseg-cloud.git

chmod 777 biliup

chmod 777 yt-dlp

sudo docker run --rm -it --mount type=bind,source="/home/USERNAME/inaseg-cloud",target=/tf/out -u=1001:1002 gaoshi/inaseg:gpu /bin/bash -c "cd /tf/out; python /tf/out/BiliWatcher.py"; sudo poweroff
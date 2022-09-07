## inaseg

inaseg uses inaspeechsegmenter and shazamAPI to segment music from streams, then identify them.
this is an example setup of inaseg running on cloud and my router (ASUS-merlin TUF5400; any openwrt or rpi would work); which uses:
a trimmed version of ddrecorder to record streams;
yt-dlp to download pre-recorded streams, in conjunction with aria2 to saturate bandwith;
ffmpeg to segment media files;
shazamAPI to call shazam on segmented media files;
biliup-rs to upload segmented media to bilibili for storage

# inaseg
to try/use inaseg's segmentation and shazam functionality, go through inaseg.ipynb.

# biliup configuration
you must configure config/biliWatcher.yaml for monitoring what streams to segment, and config/biliWrapper.json for upload settings.

configuring biliWatcher.yaml:
you must use a format as:
- extractor: biliseries
  filter: null
  last_url: https://www.bilibili.com/video/BV1hV4y1p7aE
  url: https://space.bilibili.com/731556/channel/seriesdetail?sid=120117&ctype=0

write your own extractor in inaConstant.py; currently only supports https://space.bilibili.com/{userid}/channel/seriesdetail?sid={listid} with biliseries.
write your own filter in inaConstant.py; currently only supports no filtering by setting filter to null, or only include titles with the words 歌 and 唱 by setting to karaoke
for initializing segmentation on ALL files in the biliseries playlist, set last_url to null; for initializing segmentation on FUTURE files, set to true

configuring biliWrapper.json:
you must use a format as:
"{streamer id}": [
        "{streamer live url}",
        "{video description}",
        [
            "{video tag 1}",
            "{video tag 2}"
        ]
    ],
streamer id is tied to how ytdlp template is configured.

upload templates are hardcoded in biliupWrapper.py's bilibili_upload, change accordingly.

# cloud deployment

I used $300 google trial to segment ~10,000 hrs of stream at 4 core 32GB RAM N2 instances, most was paid towards data egress to bilibili. I recommend allocating at least 24GB RAM and 60GB disk.
cloud setup:
apt install docker ffmpeg aria2 
wget biliup-rs yt-dlp
chmod biliup-rs yt-dlp

sudo docker pull gaoshi/inaseg:gpu

git clone https://github.com/lovegaoshi/inaseg-cloud.git

chmod 777 biliup

chmod 777 yt-dlp

sudo docker run --rm -it --mount type=bind,source="/home/USERNAME/inaseg-cloud",target=/tf/out -u=1001:1002 gaoshi/inaseg:gpu /bin/bash -c "cd /tf/out; python /tf/out/BiliWatcher.py"; sudo poweroff


# asuswrt deployment

logically since most of us are bottlenecked by download and upload bandwidth, it sounds like a great idea to only do the inaseg part on a CUDA enabled computer and let the rest handled by the router. however there are quite a bunch of problems with routers than rpi, or a recycled laptop:

1. openwrt systems have very limited precompiled package support. for example numpy can't be installed unless I somehow install pypy-dev.
2. router external flash drive is not meant for high write scenarios; in my case a m2 enclosure had stability problems.
3. recorder even though is meant to be low computational cost, but still takes 0.2 load per record process of TUF5400's CPU; bundled with external drive instability will drop recording from time to time, creating stutters.
4. router to computer in my case can only deliver 200mbps.

I finally decided to:
1. record on router;
2. run inaseg on computer, but with soundonly to limit bandwidth problems;
3. send timestamps and shazam results to router by writing to a file on mounted router storage;
4. router thread does ffmpeg (which is only segmentation and thus trivial on both cpu and disk, hopefully), upload, then cleanup

# biliup-rs with asuswrt:
asuswrt-merlin can only run arm-unknown-linux-gnueabi version of rust. 
cross build --target arm-unknown-linux-gnueabi

this cross docker does not have openSSL installed, and this docker might have used an older version of ubuntu that the apt cached of libssl-dev (1.0) contributed to RSA fail errors; just recompile openSSL for both x86_64 (to compile openssl-dev) and arm-unknown-linux-gnueabi (for arm-unknown-linux-gnueeabi-gcc). instructions:
with the dockerfile running, run:

apt install wget
wget https://www.openssl.org/source/openssl-1.1.1q.tar.gz
tar -xvzf openssl-1.1.1q.tar.gz && cd openssl-1.1.1q
export CROSS_SSL_TARGET=arm-linux-gnueabi # e.g. mipsel-sf-linux-musl
export OPENSSL_ARCH="linux-generic64" # This value is chosen from the output of ./Configure, it is specific to OpenSSL, you can try linux-generic
export CROSS_SSL_TOOLCHAINS="/usr/arm-linux-gnueabi" #  This must match the root of where you put your built toolchains
export CROSS_SSL_ARCH="arm-linux-gnueabi" #  This must match the toolchain name in config.mak in musl-cross-make
export CROSS_SSL_INC="/usr/arm-linux-gnueabi/include"
export CROSS_SSL_LIB="/usr/arm-linux-gnueabi/lib"
./Configure --cross-compile-prefix=/usr/bin/arm-linux-gnueabi- -I"${CROSS_SSL_INC}" -L"${CROSS_SSL_LIB}" --prefix=/usr/arm-linux-gnueabi "${OPENSSL_ARCH}"
make -j
make install

then tar this openssl 1.1.1q into a different folder, now run:
./Configure --prefix=/openssl  "linux-x86_64"

then at Cross.toml, put this:

[build.env]
passthrough = ["PKG_CONFIG_PATH=/openssl-1.1.1q/:/openssl/openssl-1.1.1q/"]



# install rust???:

asusmerlin uses arm-unknown-linux-gnueabi!!!!!

wget https://static.rust-lang.org/rustup/dist/arm-unknown-linux-gnueabi/rustup-init
chmod 777 rustup-init
mkdir /opt/installs/
mkdir /opt/installs/cargo
mkdir /opt/installs/rustup
export CARGO_HOME=/opt/installs/cargo
export RUSTUP_HOME=/opt/installs/rustup
./rustup-init

# install go???:
https://blog.hypriot.com/post/how-to-compile-go-on-arm/

$ curl -sSL https://storage.googleapis.com/golang/go1.4.3.src.tar.gz | sudo tar -xz
cd go/src
time ./make.bash

install gcc?
https://github.com/Entware/Entware-ng/wiki/Using-gcc-(native-compilation)

set LD_LIBRARY_PATH = /lib
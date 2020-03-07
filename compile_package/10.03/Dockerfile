FROM ubuntu:12.04

#COPY sources.list /etc/apt/sources.list

ENV HOSTNAME owrt-10.03-build-env

USER root
RUN apt-get update
RUN apt-get install -y libssl-dev zlib1g-dev autotools-dev zip automake \
gcc g++ sudo vim wget build-essential subversion git-core libncurses5-dev \
zlib1g-dev gawk flex quilt libssl-dev xsltproc libxml-parser-perl mercurial \
bzr ecj cvs unzip mercurial
# add a user "openwrt" as it is suggested to build as non-root
RUN mkdir -p /home/openwrt &&\
    useradd -m -d /home/openwrt openwrt &&\
    echo 'openwrt:openwrt' | chpasswd &&\
    usermod -aG sudo openwrt
RUN mkdir -p /root/firmware &&\
    mkdir -p /root/firmware/cache &&\
    chown -R openwrt:openwrt /root &&\
    chown -R openwrt:openwrt /home/openwrt

USER openwrt

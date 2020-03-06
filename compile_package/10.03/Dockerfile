FROM ubuntu:12.04

#COPY sources.list /etc/apt/sources.list

ENV HOSTNAME owrt-10.03-build-env

RUN apt-get update
RUN apt-get install -y libssl-dev zlib1g-dev autotools-dev zip automake \
gcc g++ sudo vim wget build-essential subversion git-core libncurses5-dev \
zlib1g-dev gawk flex quilt libssl-dev xsltproc libxml-parser-perl mercurial \
bzr ecj cvs unzip mercurial

# add a user "openwrt" as it is suggested to build as non-root
RUN useradd -md /home/openwrt openwrt && echo 'openwrt:openwrt' | chpasswd && usermod -aG sudo openwrt
RUN mkdir -p /root/firmware && chown -R openwrt:openwrt /root
USER openwrt

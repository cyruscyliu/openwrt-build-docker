FROM ubuntu:18.04


#COPY sources.list /etc/apt/sources.list

ENV HOSTNAME owrt-18.06-build-env

USER root
RUN apt-get update && \
apt-get install -y sudo time git-core subversion build-essential gcc-multilib \
curl libncurses5-dev zlib1g-dev gawk flex gettext wget unzip python vim && \
apt-get clean
# add a user "openwrt" as it is suggested to build as non-root
RUN mkdir -p /home/openwrt &&\
    useradd -m -d /home/openwrt openwrt &&\
    echo 'openwrt:openwrt' | chpasswd &&\
    usermod -aG sudo openwrt
RUN mkdir -p /root/firmware && chown -R openwrt:openwrt /root

USER openwrt
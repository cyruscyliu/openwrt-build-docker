# OpenWrt Build Docker

We support automatically building the OpenWrt project given a target/subtarget
of a specific OpenWrt revision. We now support OpenWrt from 10.03 to 19.07.1.
Please check [progress-summary](./progress-summary.md) for more information.

## Install

```bash
apt-get install -y docker.io && pip install docker-compose==1.19.0 && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

Then, download all [the OpenWrt download
packages](https://drive.google.com/drive/folders/1KCdgytkYtWFmiXKlpb6nkqnoRGn9z9Ck),
or one of them you need, and put them into the `./pre_download` directory for
sake of saving time.

## Usage

This project works on a batch of descriptions in a batch file. Having loaded the
batch file, a target/subtarget of a specific OpenWrt revision will be built
automatically. Each descrition of a batch file should have three elements,
`REVESION TARGET SUBTARGET`. Each element can be constant string or regular
expression. Here is an example.

``` bash
$ cat defconfig/example.batch
^archive-15.05$ ^oxnas$ ^generic$
```

After writing down your batch file, one line command is enough to build all of
descriptions.

```bash
./openwrt.py defconfig/example.batch -o example.log
```

If you want to handle building errors and rebuild manually, you need to go to
the corresponding build directory, for example,
`build/15.05-archive-15.05-oxnas-generic-OLDEST`, to maybe modify
`docker-compose.yml` and `build.sh`, and finally to run `./re_compile.sh`.
Please note that `./re_compile.sh` will clean the previous builds. Chang
`command` in `docker-compose.yml` if you want to debug the errors.

## Authors

[Qiang Liu](https://github.com/cyruscyliu), and [Cen Zhang](https://github.com/occia)

## Contact

If you have any problems, please fire issues!

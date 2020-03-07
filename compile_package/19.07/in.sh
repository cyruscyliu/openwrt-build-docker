docker exec -it `docker ps | grep 1907_firmware | awk '{print $1}'` bash

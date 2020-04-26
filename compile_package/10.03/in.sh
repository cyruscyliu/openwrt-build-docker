docker exec -it `docker ps | grep 1003_firmware | awk '{print $1}'` bash

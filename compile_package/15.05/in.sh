docker exec -it `docker ps | grep 1505_firmware | awk '{print $1}'` bash

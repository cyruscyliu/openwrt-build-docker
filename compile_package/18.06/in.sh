docker exec -it `docker ps | grep 1806_firmware | awk '{print $1}'` bash

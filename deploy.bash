docker-compose down
docker-compose build analytics
docker-compose up -d
clear
docker logs analytics -f
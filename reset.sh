
docker ps -a | grep theindex | awk '{print $1}' | xargs docker rm -f
echo "y\n" | docker volume prune
docker-compose -f local.yml run django python manage.py makemigrations
docker-compose -f local.yml run django python manage.py migrate
docker-compose -f local.yml run django python manage.py import_pages yaml/core.yaml

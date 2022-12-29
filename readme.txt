demarrer le conteneur de mysql
docker run --name mysql -e MYSQL_ROOT_PASSWORD=MYsql -p 3310:3306 -d docker.io/library/mysql


# problème d'acces à la camera ds docker
docker-compose up -d
docker run  test_web
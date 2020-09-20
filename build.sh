
# Build the base Python Container for microservices
docker build -t python-flask-restful:latest --rm -f ./util/python-flask-restfull.dockerfile .

docker-compose up -d --build
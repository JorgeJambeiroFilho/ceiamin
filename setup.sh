openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./selfsigned.key -out ./selfsigned.crt

cd backend
docker build -t rfb_ceiamin_backend .
cd ..
cd ia
docker build -t rfb_ceiamin_ia .
cd ..
cd frontend
docker build -t rfb_ceiamin_frontend .
export ENV_FOR_DYNACONF=testing
docker-compose up

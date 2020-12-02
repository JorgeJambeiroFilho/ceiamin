cd backend
docker build -t rfb_ceiamin_backend .
cd ..
cd frontend
docker build -t rfb_ceiamin_frontend .
export ENV_FOR_DYNACONF=testing
docker-compose up

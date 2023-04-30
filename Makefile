reup:
	sudo docker-compose down -v
	#sudo docker-compose stop sprint06_auth_api
	sudo docker-compose build
	sudo docker-compose up -d
	#sudo docker-compose up sprint06_auth_api
reup_api:
	sudo docker-compose stop sprint06_auth_api
	sudo docker-compose build sprint06_auth_api
	sudo docker-compose up -d sprint06_auth_api
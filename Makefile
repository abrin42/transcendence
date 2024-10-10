NAME = ft_transcendence

all : ${NAME}

${NAME} :
	docker compose up --build -d

clean :
	docker compose down
	docker rmi $$(docker images -q)

fclean :
	docker compose down
	docker rmi $$(docker images -q)
	docker volume rm $$(docker volume ls -q)
	docker network rm $$(docker network ls -q)

cleanVolume:
	docker volume rm $$(docker volume ls -q)

cleanNetwork:
	docker network rm $$(docker network ls -q)

re : fclean all

.PHONY: all clean fclean re

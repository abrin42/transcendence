NAME = ft_transcendence
OTHER_IP = $(shell hostname -I | awk '{print $$1}')
CERT_DIR = ./certificates

all : ${NAME}

${NAME} :
	docker compose up --build

create-certificates:
	mkdir -p $(CERT_DIR)
	@echo "Generating certificates using IP address: $(OTHER_IP)"
	@bash generate_certificates.sh $(OTHER_IP) $(CERT_DIR)

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

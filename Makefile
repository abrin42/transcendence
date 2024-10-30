NAME = ft_transcendence
OTHER_IP = $(shell ifconfig eno2 | grep 'inet ' | awk '{print $$2}')
CERT_DIR = ./certificates
CERT_FILE="root-ca.crt"

all : ${NAME}

${NAME} :
	@echo "export OTHER_IP=$(OTHER_IP)" >> .env
	@echo "OTHER_IP added to .env."
	@echo "The server is running on IP address: \033[1;33m$(OTHER_IP)\033[0m"
	@echo "You can join the website on: \033[1;33mhttps://$(OTHER_IP):8443/\033[0m"
	@if [ -f $(CERT_DIR)/$(CERT_FILE) ]; then \
		docker compose up --build; \
	else \
		echo "There is no certificate. Please run \"make create-cert\" and add it to Chrome or Firefox certificate manager."; \
	fi


create-cert:
	mkdir -p $(CERT_DIR)
	@echo "Generating certificates using IP address: $(OTHER_IP)"
	@bash generate_certificates.sh $(OTHER_IP) $(CERT_DIR)
	@if [ -f $(CERT_DIR)/$(CERT_FILE) ]; then \
        mkdir -p ~/.local/share/ca-certificates/ && \
        cp $(CERT_DIR)/$(CERT_FILE) ~/.local/share/ca-certificates/ && \
        update-ca-certificates --fresh --verbose --certificates ~/.local/share/ca-certificates/$(CERT_FILE); \
        echo "Certificat installé dans le magasin de certificats utilisateur."; \
    else \
        echo "Fichier $(CERT_FILE) introuvable."; \
    fi

clean-cert:
	@rm -f ~/.local/share/ca-certificates/$(CERT_FILE)
	@echo "Certificat supprimé du magasin de certificats utilisateur."

clean :
	docker compose down
	docker rmi $$(docker images -q)

cleanVolume:
	docker volume rm $$(docker volume ls -q)

cleanNetwork:
	docker network rm $$(docker network ls -q)

fclean :
	docker compose down
	@ if test -n "$(docker images -q)"; then \
		docker rmi $$(docker images -q); \
	fi
	@ if test -n "$(docker volume ls -q)"; then \
		docker volume rm $$(docker volume ls -q); \
	fi
	@ if test -n "$(docker network ls -q)"; then \
		docker network rm $$(docker network ls -q); \
	fi
	@sed -i '/^export OTHER_IP=/d' .env
	@echo "OTHER_IP removed from .env."

re : fclean all

.PHONY: all clean fclean re create-certificates install-shop
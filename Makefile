NAME = ft_transcendence
OTHER_IP = $(shell ifconfig eno2 | grep 'inet ' | awk '{print $$2}')
CERT_DIR = ./certificates
CERT_FILE = "root-ca.crt"

all : ${NAME}

${NAME} :
	@sed -i '/^export OTHER_IP=/d' .env
	@echo "export OTHER_IP=$(OTHER_IP)" >> .env
	@echo "The server is running on this IP address: \033[1;33m$(OTHER_IP)\033[0m"
	@echo "You can join the website on: \033[1;33mhttps://$(OTHER_IP):8443/\033[0m"

	@if [ -f $(CERT_DIR)/$(CERT_FILE) ]; then \
		docker compose up --build; \
	else \
		echo "There is no certificate. Please run \"make create-cert\" and add it to your Chrome or Firefox certificates manager."; \
	fi

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

re : fclean all

##############################################################
####################   CERTIFICATES   ########################
##############################################################

create-cert:
	mkdir -p $(CERT_DIR)	
	@bash generate_certificates.sh $(OTHER_IP) $(CERT_DIR)
	@if [ -f $(CERT_DIR)/$(CERT_FILE) ]; then \
        echo "Certificate already installed."; \
    else \
        echo "Certificate $(CERT_FILE) not found."; \
    fi
	@sed -i '/^IP.2 =/d' openssl.cnf
	@echo "IP.2 = $(OTHER_IP)" >> openssl.cnf
	@sed -i "s/server_names;/server_name localhost $(OTHER_IP);/" nginx/nginx.conf
	@echo "Certificates generated using IP address: $(OTHER_IP)"

clean-cert:
	@sed -i '/^export OTHER_IP=/d' .env
	@sed -i '/^IP.2 =/d' openssl.cnf
	@sed -i 's/server_name localhost .*/server_names;/' nginx/nginx.conf
	@rm -rf $(CERT_DIR)
	@echo "Certificates removed."

.PHONY: all clean cleanVolume cleanNetwork fclean create-cert clean-cert re

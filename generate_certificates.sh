#!/bin/bash

IP_ADDRESS=$1
OUTPUT_DIR=$2

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Root CA
openssl req -x509 -nodes -newkey rsa:2048 -keyout "$OUTPUT_DIR/root-ca.key" -days 365 -out "$OUTPUT_DIR/root-ca.crt" -subj "/C=US/ST=Denial/L=Earth/O=Atest/CN=root_CA"

# Server CSR and Key
openssl req -nodes -newkey rsa:2048 -keyout "$OUTPUT_DIR/server.key" -out "$OUTPUT_DIR/server.csr" -subj "/C=US/ST=Denial/L=Earth/O=Dis/CN=$IP_ADDRESS"

# Server Certificate with subjectAltName for localhost and IP address
openssl x509 -req -CA "$OUTPUT_DIR/root-ca.crt" -CAkey "$OUTPUT_DIR/root-ca.key" -in "$OUTPUT_DIR/server.csr" -out "$OUTPUT_DIR/server.crt" -days 365 -CAcreateserial -extfile <(cat <<EOF
subjectAltName=DNS:localhost,IP:$IP_ADDRESS
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage=digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
EOF
)

echo "Certificates created in $OUTPUT_DIR with IP $IP_ADDRESS and localhost"

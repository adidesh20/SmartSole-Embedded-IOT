#/bin/bash


sudo openssl genrsa -des3 -out ca.key 2048
sudo openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
sudo openssl genrsa -out server.key 2048
sudo openssl req -new -out server.csr -key server.key
sudo openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360

sudo openssl rsa -in server.key -out server-nopass.key
sudo mv server-nopass.key server.key

sudo openssl genrsa -out client.key 2048
sudo openssl req -new -out client.csr -key client.key
sudo openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 360

sudo cp ca.crt ../../src/communications/certs/
sudo cp client.key ../../src/communications/certs/
sudo cp client.crt ../../src/communications/certs/

sudo cp server.key ../certs
sudo cp server.crt ../certs
sudo cp ca.crt ../ca_certificates

#sudo mv server-nopass.key server.key
#
#sudo mv server.key ../certs
#sudo mv server.crt ../certs
#sudo mv ca.crt ../ca_certificates

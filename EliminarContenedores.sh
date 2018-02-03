#/bin/bash

echo Vamos a limpiar docker

# Parar todos los contenedores
sudo docker stop $(sudo docker ps -a -q)

# Eliminar todos los contenedores
sudo docker rm $(sudo docker ps -a -q)

# Eliminar todas las imágenes
sudo docker rmi $(sudo docker images -q)

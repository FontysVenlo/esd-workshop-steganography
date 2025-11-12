docker pull alessandraiorga2003/stego-tool:latest

for windows:

docker run -it --rm alessandraiorga2003/stego-tool:latest
docker run -it --rm -v %cd%:/app/output alessandraiorga2003/stego-tool:latest

for linux and mac:

docker run -it --rm -v "$(pwd):/app/output" alessandraiorga2003/stego-tool:latest
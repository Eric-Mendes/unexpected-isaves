UID=$(shell id -u)
GID=$(shell id -g)


image_save:
	docker build -t image_saver:latest --build-arg GID=$(GID) --build-arg UID=$(UID) .
	docker run --rm -it -v "$(PWD)/app/saves:/app/saves" image_saver:latest
	docker rmi image_saver:latest

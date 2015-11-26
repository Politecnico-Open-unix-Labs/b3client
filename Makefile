.PHONY: install

install:
	pip install websocket-client daemonize
	cp b3d.py /etc/init.d/b3d
	mkdir -p /etc/b3d
	cp -r plugins /etc/b3d/

.DEFAULT_GOAL = install


install:
	cp b3d.service /etc/systemd/system/
	cp b3d.py /usr/local/bin/b3d
	cp b3d.json /etc/
	systemctl daemon-reload
	service b3d restart

uninstall:
	service b3d stop
	systemctl daemon-reload
	rm /etc/systemd/system/b3d.service
	rm /usr/local/bin/b3d

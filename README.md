files:
```
/etc/systemd/system/b3d.service
/usr/local/bin/b3d
/etc/b3d.json
```

deploy:
```
make install
```

read the logs:
```
journalctl -u b3d
```

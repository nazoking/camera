install:
	sudo install -g root -o root -m 0744 -p system/spy-recorder.service /etc/systemd/system/
	sudo install -g root -o root -m 0744 -p system/spy-web.service /etc/systemd/system/
	sudo systemctl daemon-reload
	if [ ! -e /var/lib/samba/public/log/ ]; then mkdir /var/lib/samba/public/log/; fi

enable:
	sudo systemctl enable spy-recorder
	sudo systemctl enable spy-web

deploy:
	rsync -avvzu ./ pi@raspizero.local:/opt/dev/app/ --exclude .git --exclude venv --exclude __pycac
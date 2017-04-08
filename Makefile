install:
	python setup.py install
	cp etc/wazo-admin-ui/conf.d/extension.yml /etc/wazo-admin-ui/conf.d
	systemctl restart wazo-admin-ui

uninstall:
	pip uninstall wazo-admin-ui-extension
	rm /etc/wazo-admin-ui/conf.d/extension.yml
	systemctl restart wazo-admin-ui

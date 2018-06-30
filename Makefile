ANSIBLE_GROUP = ansible
init:
	mkdir -p ./build/usr/share/ansible/modules
	cp -r ./xenserver/module_utils ./build/usr/share/ansible/
	cp -r ./xenserver ./build/usr/share/ansible/modules/
install:
	cp -r ./build/usr /
	chgrp -R $(ANSIBLE_GROUP) \
		/usr/share/ansible
uninstall:
	rm -rf /usr/share/ansible/modules/xenserver
clean:
	find . -iname *.pyc -exec rm -f {} +
	rm -rf ./build

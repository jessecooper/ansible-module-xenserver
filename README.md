#Ansible Xenserver
A custom ansible module for working with Xenserver. It is a wrapper around the xe command.
## Install
```
make
make install
# It installs under /usr/share/ansible/xenserver
```
## Uninstall
```
make uninstall
```
## Example play using the module
```
---
- hosts: xenserver01
  remote_user: root
  tasks:
    - name: "List xen guests"
      xen_vm_list:
	params: all
    - name: "install vm"
      xen_vm_install:
        template: <template uuid>
        name_label: test-from-ansible
```
## Develop
Coming soon

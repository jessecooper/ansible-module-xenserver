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
      xen_vm:
        vm_list: all
```
## Develop
Coming soon

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
    - name: "start vm"
      xen_vm_start:
        uuid: <template uuid>
    - name: "vm install"
      xen_vm_start:
        uuid: <vm uuid>

```
## Develop
Coming soon

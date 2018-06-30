#Ansible Xenserver
A custom ansible module for working with Xenserver. It is a wrapper around the xe command.
## Install
Requires ansible 2.4+
```
make
make install
# It installs under /usr/share/ansible/xenserver
```
Edit /etc/ansible/ansible.cfg and add the following lines:
```
library = /usr/share/ansible/module
module_utils = /usr/share/ansible/module_utils
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
      register: vm_uuid
    - name: "start vm"
      xen_vm_start:
        uuid: "{{ vm_uuid.uuid }}"
    - name: "get ipv4 address"
      xen_vm_param:
        uuid: "{{ vm_uuid.uuid }}"
	param: networks
      register: vm_ip
...
```
## Develop
Coming soon

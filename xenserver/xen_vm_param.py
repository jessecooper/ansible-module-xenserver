#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: xen_vm_param
author:
    - Jesse Cooper (@jessecooper)
version_added: "2.1"
short_description: Manage xenserver
requirements: [ xe ]
description:
    - Manage xenserver guests using xe commands
options:
    uuid:
        description:
            - uuid of vm
        required: true
    action:
        description:
            - [get|set|remove|add|clear] all or common seperated list of vm params to return
        required: true
    param-name:
        description:
            - the vm paramater
        required: true
'''

EXAMPLES = '''
- xen_vm_param:
    uuid: <vm uuid>
    action: get
    params-name: networks
'''

import os
import re
import socket
import traceback

from ansible.module_utils.basic import (
    AnsibleModule,
    get_distribution,
    get_distribution_version,
    get_platform,
    load_platform_subclass,
)
from ansible.module_utils._text import to_native
from ansible.module_utils.xenserver_common import XeBase

class XeVmParam(XeBase):
    """
    This is a xe vm_list command wrapper class
    """

    def get(self, uuid, param_name):
        """get(str, str) -> dict
        Args:
            params (str): parameters to return from each vm.
        Returns:
            dict
        """
        self.cmd.append('vm-param-get')
        self.cmd.append('uuid=%s' % uuid)
        self.cmd.append('param-name=%s' % param_name)
        rc, out, err = self.module.run_command(self.cmd)
        if rc != 0:
            self.module.fail_json(msg="Command failed rc=%d, out=%s, err=%s" % (rc, out, err))
        if param_name == "networks":
            return self._format_networks(to_native(out).strip())
        else:
            return to_native(out).strip()

    def _format_networks(self, networks):
        """_format_networks(str) -> dict"""
        ipv4 = []
        ipv6 = []
        networks_dict = {
            "ipv4": ipv4,
            "ipv6": ipv6
        }
        ip_reg = re.compile(
            # Match ipv4 and ipv6.IPv6 needs to be refined
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[0-9A-Fa-f]{4}:+.*"
        )
        ips = ip_reg.findall(networks)
        # This works fine for a single nic I am sure it
        # needs to be fixed for multiple nics
        if len(ips) > 0:
            networks_dict['ipv4'] = ips[0]
            networks_dict['ipv6'] = ips[1]

        return networks_dict

def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(required=True),
            uuid=dict(required=True),
            param=dict(required=True)
        ),
        supports_check_mode=True,
    )

    vm_param_cmd = XeVmParam(module)
    vm_param = module.params['param']
    vm_uuid = module.params['uuid']
    vm_action = module.params['action']

    if vm_action == 'get':
        out = vm_param_cmd.get(vm_uuid, vm_param)
    # elif ... set up other actions
    kw = {
            "changed": True, 
            vm_param: out,
            "ansible_facts": { 
                "ansible_fqdn": socket.getfqdn(),
                "ansible_domain": '.'.join(socket.getfqdn().split('.')[1:])
                }
        }

    # dict with after and before key 
    #if changed:
    #    kw['diff'] = {'after': '\n',
    #                  'before': '\n'}

    module.exit_json(**kw)

if __name__ == '__main__':
    main()

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
module: xen_vm_list
author:
    - Jesse Cooper (@jessecooper)
version_added: "2.1"
short_description: Manage xenserver
requirements: [ xe ]
description:
    - Manage xenserver guests using xe commands
options:
    params:
        description:
            - all or common seperated list of vm params to return
        required: true
'''

EXAMPLES = '''
- xen_vm_list:
    params: all
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

class XeVmList(XeBase):
    """
    This is a xe vm_list command wrapper class
    """

    def vm_list(self, params=None):
        """vm_list(str) -> dict
        Args:
            params (str): parameters to return from each vm.
        Returns:
            dict
        """
        self.cmd.append('vm-list')
        if params != None:
            self.cmd.append('params=%s' % params)
        rc, out, err = self.module.run_command(self.cmd)
        if rc != 0:
            self.module.fail_json(msg="Command failed rc=%d, out=%s, err=%s" % (rc, out, err))
        return to_native(out).strip()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            params=dict(required=True)
        ),
        supports_check_mode=True,
    )

    vm_list_cmd = XeVmList(module)
    vm_list_params = module.params['params']

    if vm_list_params != 'all':
        out = vm_list_cmd.vm_list(params=vm_list_params)
    else:
        out = vm_list_cmd.vm_list()
    
    # split output by \n and : and remove the last 3 indexe I am sure this can be done better
    out_formated = re.split(r"\n|:\s", out.replace(' ', '').strip())[:-3:]
    kw = dict(changed=True, vm_list=out_formated,
              ansible_facts=dict(
                    ansible_fqdn=socket.getfqdn(),
                    ansible_domain='.'.join(socket.getfqdn().split('.')[1:])
                    )
              )

    #if changed:
    #    kw['diff'] = {'after': '\n',
    #                  'before': '\n'}

    module.exit_json(**kw)

if __name__ == '__main__':
    main()

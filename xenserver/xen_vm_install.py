#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
'''xen_vm_install: wrapper around xe vm-install command
   TODO:
    * check if vm present before install
'''

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: xen_vm_install
author:
    - Jesse Cooper (@jessecooper)
version_added: "2.1"
short_description: Manage xenserver
requirements: [ xe ]
description:
    - Manage xenserver guests using xe commands
options:
    template:
        description:
            - xen os template name
        required: true

'''

EXAMPLES = '''
- xen_vm_install:
    temlate: <temlate name>
    name-label: <vm name>
'''

import os
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

class XeVmInstall(XeBase):
    """
    This is a xe vm_list command wrapper class
    """

    def vm_install(self, template=None, name_label=None):
        """vm_list(str) -> dict
        Args:
            template (str): parameters to return from each vm.
            name_label (str): parameters to return from each vm.
        Returns:
            dict
        """
        self.cmd.append('vm-install')
        self.cmd.append('template=%s' % template)
        self.cmd.append('new-name-label=%s' % name_label)
        rc, out, err = self.module.run_command(self.cmd)
        if rc != 0:
            self.module.fail_json(msg="Command failed rc=%d, out=%s, err=%s" % (rc, out, err))
        return to_native(out).strip()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            template=dict(required=True),
            name_label=dict(required=True)
        ),
        supports_check_mode=True,
    )

    vm_install_cmd = XeVmInstall(module)
    vm_template = module.params['template']
    vm_name = module.params['name_label']

    out = vm_install_cmd.vm_install(
        template=vm_template,
        name_label=vm_name
        )
    
    out_formated = out.strip().split()[1::2]
    kw = dict(
        changed=True,
        uuid=out,
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

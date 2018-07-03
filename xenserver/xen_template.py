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
module: xen_template
author:
    - Jesse Cooper (@jessecooper)
version_added: "2.1"
short_description: Manage xenserver
requirements: [ xe ]
description:
    - Manage xenserver guests using xe commands
options:
    template_list:
        description:
            - return a list of virtual machines
        required: false
'''

EXAMPLES = '''
- xen_template:
    template_list: all
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

class XeTemplateList(XeBase):
    """
    This is a xe template_list command wrapper class
    """

    def template_list(self, params=None):
        """template_list(str) -> dict
        Args:
            params (str): parameters to return from each vm.
        Returns:
            dict
        """
        self.cmd.append('template-list')
        if params != None:
            self.cmd.append('params=%s' % params)
        rc, out, err = self.module.run_command(self.cmd)
        if rc != 0:
            self.module.fail_json(msg="Command failed rc=%d, out=%s, err=%s" % (rc, out, err))
        return to_native(out).strip()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            template_list=dict(required=False),
            params=dict(required=False)
        ),
        supports_check_mode=True,
    )

    template_list_cmd = XeTemplateList(module)
    template_list_type = module.params['template_list']
    template_list_params = module.params['params']

    if template_list_type == 'all':
        if template_list_params:
            out = template_list_cmd.template_list(params=template_list_params)
        else:
            out = template_list_cmd.template_list()
    kw = dict(changed=True, template_list=out,
              ansible_facts=dict(
                    ansible_fqdn=socket.getfqdn(),
                    ansible_domain='.'.join(socket.getfqdn().split('.')[1:])
                    )
              )

    #if changed:
    #    kw['diff'] = {'after': 'hostname = ' + name + '\n',
    #                  'before': 'hostname = ' + name_before + '\n'}

    module.exit_json(**kw)

if __name__ == '__main__':
    main()

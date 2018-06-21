'''xenserver_common
'''
class XeBase(object):
    """
    This is a xe command generic class
    """
    def __init__(self, module):
        self.module = module
        self.cmd = ['xe']

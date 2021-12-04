# TODO: create proper implementation


class Regex:
    '''class resposible for creating names of files based on their path and regex format'''

    def __init__(self):
        return

    def create_name(self, filepath):
        '''Creates file name based on filepath and set regex'''
        return ''.join([s+"_" for s in filepath.split("/")])[:-1]

    def check_if_ignore(self, filepath):
        '''Returns true or false whether a file should be ignred based on regex and its name'''
        return False

from exceptions import Exception

class Error(Exception):
    ''' Base class to create exceptions'''
    pass

class fileFormatError(Error):
    '''The user should only load compressed files.

    Attributes:
        message -- Error Info
    '''
    def __init__(self,message):
        self.message = message
        

class validationError(Error):
    '''New user errors.

    Attributes:
        message -- Error Info
    '''
    def __init__(self,message):
        self.message = message
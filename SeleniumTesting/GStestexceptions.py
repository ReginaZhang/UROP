'''
Module created on 26/11/2014

@author: Regina Zhang

'''

class LoginException(Exception):
    def __init__(self, message = None, username = None, pw = None):
        self.username = username
        self.pw = pw
        self.message = message

    def __str__(self):
        if self.username == None and self.pw == None:
            if self.message == None:
                return "Not sepcified exception"
            else:
                return self.message
        report = "Failed to login with username '{0}' and password '{1}' \n"\
                 .format(self.username, self.pw)
        if self.message:
            report += "\tMessage: " + self.message
        return report

class MountingException(Exception):
    def __init__(self, message = None):
        self.message = message

    def __str__(self):
        report = "Failed to mount a container."
        if self.message:
            return report + "\n" + self.message
        return report

class DisconnectContainerException(Exception):
    def __init__(self, message = None):
        self.message = message

    def __str__(self):
        report = "Failed to disconnect a container."
        if self.message:
            return report + "\n" + self.message
        return report

class RenameException(Exception):
    def __init__(self, message = None):
        self.message = message

    def __str__(self):
        report = "Failed to rename the file."
        if self.message:
            return report + "\n" + self.message
        return report
    
class CopyException(Exception):
    def __init__(self, message = None):
        self.message = message
        
    def __str__(self):
        report = "Failed to copy the file"
        if self.message:
            return report + "\n" + self.message
        return report

class DeleteException(Exception):
    def __init__(self, message = None):
        self.message = message
        
    def __str__(self):
        report = "Failed to delete the file"
        if self.message:
            return report + "\n" + self.message
        return report
    
class MoveException(Exception):
    def __init__(self, message = None):
        self.message = message
        
    def __str__(self):
        report = "Failed to move the file"
        if self.message:
            return report + "\n" + self.message
        return report
    
class PublicURLException(Exception):
    def __init__(self, message = None):
        self.message = message
        
    def __str__(self):
        report = "Error occurred when manipulating public URLs."
        if self.message:
            return self.message
        return report
    
class PrivateURLException(Exception):
    def __init__(self, message = None):
        self.message = message
        
    def __str__(self):
        report = "Failed to get the private URL."
        if self.message:
            return report + "\n" + self.message
        return report
    
class ImportURLException(Exception):
    def __init__(self,message = None):
        self.message = message
        
    def __str__(self):
        report = "Failed to import URL."
        if self.message:
            return report + "\n" + self.message
        return report
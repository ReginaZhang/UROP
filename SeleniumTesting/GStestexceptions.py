
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

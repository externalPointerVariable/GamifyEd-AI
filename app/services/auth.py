import requests

class auth:
    def __init__(self):
        self.userName = ""
        self.userId = ""
        self.userRole = ""
    
    def getUserStatus(self):
        try:
            pass
        except Exception as e:
            return f"Not able to authenticate the user {str(e)}"
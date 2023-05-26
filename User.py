class user :
    def __init__(self , id, pwd, admin = False):
        self.id = id
        self.pwd = pwd
        self.isAdmin = admin
        self.isVoted = False

    def setVote(self) :
        self.isVoted = True

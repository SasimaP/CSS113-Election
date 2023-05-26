class party() : 
    def __init__ (self , name , depart , intro) :
        self.name = name
        self.depart = depart
        self.intro = intro
        self.score = 0

    def increaseScore (self) :
        self.score += 1

    def toString(self) :
        return (self.name + " - " + self.depart + " - " + self.intro + " - " + str(self.score))
    
    def introduce(self) :
        return (self.name + " " + self.depart + " " + self.intro)

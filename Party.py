class party() : 
    def __init__ (self , name , depart , intro , img_path) :
        self.name = name
        self.depart = depart
        self.intro = intro
        self.score = 0
        self.img = img_path

    def increaseScore (self) :
        self.score += 1

    def toString(self) :
        return (self.name + " - " + self.depart + " - " + self.intro + " - " + str(self.score))
    
    def introduce(self) :
        return (self.name + " " + self.depart + " " + self.intro)

import tkinter as tk 
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import User
import Party
import csv
userlist = []
partyList = []

with open("DB.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        userlist.append(User.user(row[0], row[1]))

userlist.append(User.user("admin","1234", True))
partyList.append(Party.party("Grizzly","IT","I am Brown"))
partyList.append(Party.party("Panda","FIBO","I am Panda"))
partyList.append(Party.party("Ice Bear","ACS","I am Ice"))

class tkinterApp(tk.Tk):
    def __init__ (self, *args , **kwargs) :
        tk.Tk.__init__(self, *args , **kwargs)

        mainframe = ttk.Frame(self)
        mainframe.pack(side="top", fill="both", expand=True)

        mainframe.grid_rowconfigure(0 , weight=1)
        mainframe.grid_columnconfigure(0 , weight=1)

        self.currentUser = User.user('','')
        self.frames = {}
        for F in (AuthenticatePage , MenuPage , PartyPage, ElectionPage, AdminPage ):
            frame = F(mainframe , self )
            self.frames[F] = frame
            frame.grid(row = 0, column = 0 , sticky='nwes')
        self.show_page(MenuPage)

    def show_page(self, cont) :
        frame = self.frames[cont]
        frame.tkraise()

    def setCurrentUser (self , user) :
        self.currentUser = user

    def clearUser(self) :
        self.currentUser = User.user('','')

class AuthenticatePage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        # style = ttk.Style()
        # style.configure("test.TFrame", background = "red")
        # style.configure("w.TFrame", background = "green")
        ttk.Frame.__init__(self, parent, style="test.TFrame")

        title = ttk.Label(self , text="Authentication" ,font=("Times New Roman", 20),anchor="center" ).pack(fill="x" , pady=(90 ,0))
        # title.grid(row = 0 , column = 0, columnspan=2, sticky=EW)
        userInputGroup = ttk.Frame(self)
        userInputGroup.pack(pady=(10 , 5))
        ttk.Label(userInputGroup , text="STD_ID" , font=("Times New Roman", 12), anchor=CENTER , width=10 ).pack(side=LEFT)
        # .grid(row = 1 , column = 0, sticky = "WE")
        
        self.userEntry = ttk.Entry(userInputGroup)
        self.userEntry.pack(side=LEFT)
        # self.userEntry.grid(row =  1 , column = 1 , sticky = "E")

        passInputGroup = ttk.Frame(self)
        passInputGroup.pack(pady=(5, 10))
        ttk.Label(passInputGroup , text="PASS" , font=("Times New Roman", 12),anchor=CENTER , width=10).pack(side=LEFT)
        # .grid(row = 2, column = 0)
        self.passEntry = ttk.Entry(passInputGroup , show="*" )
        self.passEntry.pack(side=LEFT)
        # self.passEntry.grid(row = 2 , column = 1)

        ttk.Button(self ,text = "Submit", command= lambda : self.login(controller)).pack()
        # ttk.Button(self ,text = "Submit", command= lambda : print()).grid(row = 4, columnspan=2)
        

    def login(self, controller) :
        if self.userEntry.get() in [user.id for user in userlist] :
            userInfo = [user for user in userlist if user.id == self.userEntry.get()][0]
            if self.passEntry.get() == userInfo.pwd :
                if userInfo.isAdmin == True :
                    controller.show_page(AdminPage)
                elif userInfo.isVoted == False :
                    controller.setCurrentUser(userInfo)
                    controller.show_page(MenuPage)
                else :
                    messagebox.showerror("Error" , "This Id is already voted")
            else:
                messagebox.showerror("Error" , "Password incorrectly")
        else:
            messagebox.showerror("Error" , "Id " + self.userEntry.get() + " is not exist!")

    def tkraise(self, aboveThis = None):
        # self.userEntry.delete(0 , tk.END)
        # self.passEntry.delete(0, tk.END)
        super().tkraise(aboveThis)

   
class MenuPage(tk.Frame):
     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # ttk.Label(self , text="Menu" , font=("Times New Roman", 20)).grid(row = 0)

        ButtonGroup = ttk.Frame(self, height = 20)
        ButtonGroup.pack(pady=(130 , 5))
        ttk.Button(ButtonGroup ,text = "Party Detail" , command= lambda : controller.show_page(PartyPage)).pack(side = LEFT)
        ttk.Button(ButtonGroup ,text = "Election" , command= lambda : controller.show_page(ElectionPage)).pack(side = LEFT, expand=1, fill="both")

class PartyPage(tk.Frame):
     def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        for i in range(len(partyList)):
            ttk.Label(self, text= partyList[i].introduce()).grid(row = i)
        ttk.Button(self ,text = "Vote" , command= lambda : controller.show_page(ElectionPage)).grid(row = 4 , sticky="NWES")

class ElectionPage(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.score = [tk.IntVar(),tk.IntVar(),tk.IntVar()]
        self.checkbox = [0, 0, 0]
        for i in range(len(partyList)):
            self.checkbox[i] = ttk.Checkbutton(self, text= partyList[i].name , variable=self.score[i] , command = self.updateCheckButton)
            self.checkbox[i].grid(row = i , column = 0)
        ttk.Button(self, text="Back" , command = lambda : self.confirm_vote(controller)).grid(row = 4)
        ttk.Button(self, text="Confirm" , command = lambda : self.confirm_vote(controller)).grid(row = 5)
        
        
    def confirm_vote(self, controller) :
        if messagebox.askyesno("Confirm your vote" , "Do you want to submit this vote. You can't change the result after you confirm") :
            for i in range(len(self.score)) :
                if self.score[i].get() == 1:
                    partyList[i].increaseScore()
                    
            userlist[userlist.index(controller.currentUser)].isVoted = True
            controller.clearUser()
            controller.show_page(AuthenticatePage)

        
    def updateCheckButton(self) : 
        checked = 0
        for i in range(len(self.score)) :
            self.checkbox[i].config(state =tk.NORMAL)
            if self.score[i].get() == 1 :
                checked += 1
        
        if (checked == 2 ) :
            for i in range(len(self.score)) :
                if self.score[i].get() == 0 :
                    self.checkbox[i].config(state =tk.DISABLED)
    
    def tkraise(self):
        for i in range(len(self.checkbox)) :
            self.score[i].set(0)
        self.updateCheckButton()
        super().tkraise(None)

class AdminPage(tk.Frame) :
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        for i in range(len(partyList)) :
            ttk.Label(self ,text = partyList[i].toString()).grid(row = i)
        ttk.Button(self, text = "Go back", command = lambda : controller.show_page(AuthenticatePage)).grid(row = len(partyList) + 1)
        
    def reloadScore(self) :
        for i in range(3) :
            print(partyList[i].toString())

    def tkraise(self):
        for i in range(len(partyList)) :
            ttk.Label(self ,text = partyList[i].toString()).grid(row = i)
        super().tkraise(None)

app = tkinterApp()
app.geometry("600x400")
app.mainloop()


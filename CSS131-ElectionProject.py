import tkinter as tk 
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
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
userlist.append(User.user("123","1234"))
userlist.append(User.user("321","1234"))

partyList.append(Party.party("Grizzly","IT","ผมมีนโยบาย อัจฉริยะ เช่น!!! ยกเลิกแบงค์พัน!!!", "./img/grizzly.png"))
partyList.append(Party.party("Panda","FIBO","ผมมีนโยบาย อัจฉริยะ เช่น!!! หวยใบเสร็จ!!!", "./img/Panda.png"))
partyList.append(Party.party("Ice Bear","ACS","ผมมีนโยบาย อัจฉริยะ เช่น!!! Digital Wallet!!!", "./img/Ice_bear.png"))

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
        self.show_page(AuthenticatePage)

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

        ttk.Frame.__init__(self, parent, style="test.TFrame")
        style = ttk.Style()

        ttk.Label(self , text="Authentication" ,font=("Times New Roman", 20),anchor="center" ).pack(fill="x" , pady=(90 ,0))
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
        self.passEntry.bind("<Return>" , lambda event : self.login(controller))
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
        self.userEntry.delete(0 , tk.END)
        self.passEntry.delete(0, tk.END)
        super().tkraise(aboveThis)

   
class MenuPage(tk.Frame):
     def __init__(self, parent, controller):
        style = ttk.Style()
        style.configure("buttonStyle.TButton", font = ("Times New Roman", 18))

        ttk.Frame.__init__(self, parent)
        # ttk.Label(self , text="Menu" , font=("Times New Roman", 20)).grid(row = 0)

        ButtonGroup = ttk.Frame(self)
        ButtonGroup.pack(pady=(130 , 5), ipady=40 , fill=Y)
        ttk.Button(ButtonGroup ,text = "Party Detail" , command= lambda : controller.show_page(PartyPage), style="buttonStyle.TButton").pack(side = LEFT , fill=Y, padx=15 , ipadx=35)
        ttk.Button(ButtonGroup ,text = "Election" , command= lambda : controller.show_page(ElectionPage), style="buttonStyle.TButton").pack(side = LEFT, fill=Y, padx=15 , ipadx=35)

class PartyPage(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        partyFrame = ttk.Frame(self)
        partyFrame.pack(pady=(20 , 20))
        imgLabel = [0,0,0]
        for i in range(len(partyList)):
            frame = ttk.Frame(partyFrame)
            frame.pack(side=LEFT , padx=20)

            imgLoad = Image.open(partyList[i].img) 
            imgLoad = imgLoad.resize((120,180),Image.LANCZOS)
            img = ImageTk.PhotoImage(imgLoad)

            imgLabel[i] = ttk.Label(frame , image= img)
            imgLabel[i].bind("<Enter>" , lambda event , party = partyList[i] : self.show_detail(party))
            imgLabel[i].bind("<Leave>" , self.clearInfoFrame)


            imgLabel[i].image = img
            imgLabel[i].pack()
            
        btn = ttk.Button(self ,text = "Vote" , command= lambda : controller.show_page(ElectionPage))
        btn.place(rely=0.95, relx=0.95, x=0, y=0, anchor=SE)
        
        self.infoFrame = ttk.Frame(self)
        self.infoFrame.pack(pady=25)
        ttk.Label(self.infoFrame , text = "Hover image for infomation" , font=("Times New Roman" , 16)).pack()

    def show_detail(self , info) :
        self.infoFrame.winfo_children()[0].destroy()
        ttk.Label(self.infoFrame , text = "Name : " + info.name ,font=("Times New Roman", 12) ).pack(side=TOP )
        ttk.Label(self.infoFrame , text = "Department : " +info.depart,font=("Times New Roman", 12) ).pack(side=TOP)
        ttk.Label(self.infoFrame , text = "Short introduction : " +info.intro,font=("Times New Roman", 12) ).pack(side=TOP)

    def clearInfoFrame(self, event) :
        for w in self.infoFrame.winfo_children() :
            w.destroy()
        ttk.Label(self.infoFrame , text = "Hover image for infomation" , font=("Times New Roman" , 16)).pack()




class ElectionPage(tk.Frame):
    def __init__(self, parent, controller):
        style = ttk.Style()
        style.configure("buttonStyle.TCheckbutton", font = ("Times New Roman", 16))
        style.configure("buttonStyle.TButton", font = ("Times New Roman", 12))

        ttk.Frame.__init__(self, parent)

        self.score = [tk.IntVar(),tk.IntVar(),tk.IntVar()]
        self.checkbox = [0, 0, 0]

        ttk.Label(self, text = "You can choose maximum 2 of party form party list or none of them.", font= ("Times New Roman" , 12)).pack(pady= (50 , 10))

        checkboxFrame = ttk.Frame(self )
        checkboxFrame.pack(fill='x' , padx = 50 , pady = 15)

        for i in range(len(partyList)):
            self.checkbox[i] = ttk.Checkbutton(checkboxFrame, text= partyList[i].name , variable=self.score[i] , command = self.updateCheckButton , style="buttonStyle.TCheckbutton")
            self.checkbox[i].pack(fill = 'x' , pady = 5)

        buttonFrame = ttk.Frame(self)
        buttonFrame.pack()

        ttk.Button(buttonFrame, text="Party Detail" , command = lambda : controller.show_page(PartyPage) , style= "buttonStyle.TButton").pack(side=LEFT , padx = 10 , ipady= 10)
        ttk.Button(buttonFrame, text="Confirm" , command = lambda : self.confirm_vote(controller), style= "buttonStyle.TButton").pack(side=LEFT , padx = 10, ipady= 10)
        
        
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
        partyFrame = ttk.Frame(self)
        partyFrame.pack(pady=(20 , 20))
        imgLabel = [0,0,0]
        self.textLabel = [0,0,0]
        for i in range(len(partyList)):
            frame = ttk.Frame(partyFrame)
            frame.pack(side=LEFT , padx=20)

            imgLoad = Image.open(partyList[i].img) 
            imgLoad = imgLoad.resize((120,180),Image.LANCZOS)
            img = ImageTk.PhotoImage(imgLoad)

            imgLabel[i] = ttk.Label(frame , image= img)
            imgLabel[i].image = img
            imgLabel[i].pack()
            self.textLabel[i] = ttk.Label(frame , text = partyList[i].name + " : " + str(partyList[i].score) , font= ("Times New Roman" , 12))
            self.textLabel[i].pack()
        ttk.Button(self, text = "Go back", command = lambda : controller.show_page(AuthenticatePage)).pack()
        

    def tkraise(self):
        for i in range(len(partyList)) :
            self.textLabel[i].config(text= partyList[i].name + " : " + str(partyList[i].score))
        super().tkraise(None)

app = tkinterApp()
app.geometry("600x400")
app.mainloop()


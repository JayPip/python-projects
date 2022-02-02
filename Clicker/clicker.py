
from faulthandler import disable
from tkinter import *
from tkinter import messagebox
import time
from threading import *
from tkinter import ttk

form = Tk()

form.title("Clicker!")
form.geometry("350x250")

#var
treeView = None
ctr = 0
userName = ""

#functions
def counter():
    global ctr
    ctr+=1
    ctrString.set("Your Clicks: " + str(ctr))
    form.update_idletasks()

def infoPopup():
    global ctr
    pace = ctr/5
    if pace < 2:
        messagebox.showinfo("Your Pace", "Too slow ;/")
        reset()
    elif pace>=3 and pace<5:
        messagebox.showinfo("Your Pace", "Not bad")    
        reset()
    elif pace>=5 and pace<7:
        messagebox.showinfo("Your Pace", "Wow!")
        reset()   
    elif pace>=7:
        messagebox.showinfo("Your Pace", "Global Elite")
        reset()

def startCount():   
    timerLabel.set('3!')
    form.update_idletasks()
    time.sleep(1)
    timerLabel.set('2!')
    form.update_idletasks()
    time.sleep(1)
    timerLabel.set('1!')
    form.update_idletasks()
    time.sleep(1)
    timerLabel.set('Go!')
    Clickerbtn['state'] = "normal"
    Clickerbtn['bg'] = "green"
    form.after(5000, infoPopup)

def timerThread():
    thread = Thread(target = startCount)
    thread.start()


def getData():
#    updateData()
    f = open("scores.txt", "r")
    fileData = f.readlines()
    f.close()
    treeView.delete(*treeView.get_children())
    for set in fileData:
        subset = set.split(" ")
        treeView.insert("", 'end',  
             values =(subset[0], subset[1]))
    form.after(300, getData)
    
    
def updateData():
    f = open("scores.txt", "r")
    fileData = f.readlines()
    for set in fileData:
        subset = set.split(" ")
        if subset[0]== userName:
            subset[1]=ctr/5

def listThread():
    thread = Thread(target = getData)
    thread.start()

def reset():
    global ctr
    ctr = 0
    ctrString.set("Your Clicks: " + str(ctr))
    timerLabel.set("")
    Clickerbtn['state'] = "disabled"
    Clickerbtn['bg'] = "red"
    form.update_idletasks()


def welcomeForm():
    textForm = Toplevel(form)
    textForm.title("Enter your Username:")
    textForm.geometry("300x100")
    
def LogForm():
    form.withdraw()
    LogForm = Toplevel(form)
    LogForm.title("Your Username")
    LogForm.geometry("300x100")
    UserTxt = Text(LogForm, height = 1, width= 15)
    UserTxt.grid(row = 0, column= 0)
    Savebtn = Button(LogForm, text = "Save", command = saveName(UserTxt))
    CloseBtn = Button(LogForm, text="Close", command = closeLog(LogForm))
    Savebtn.grid(row = 1, column= 0)
    CloseBtn.grid(row = 1, column = 1)

def saveName(UserTxt):
    global userName
    userName = UserTxt.get("1.0",END)

def closeLog(LogForm):
    form.deiconify()
    LogForm.destroy

ctrString = StringVar()
timerLabel = StringVar()
ctrString.set("Your Clicks: ")

Startbtn = Button(form, text = "Start your test", command = timerThread)
Clickerbtn = Button(form, text = "Click!",bg = "red",
    highlightcolor = "red", width = 20, height= 5, command = counter,
    state= "disabled")
Timerlbl = Label(form, textvariable= timerLabel) 
Pacelbl = Label(form, textvariable = ctrString )
LogBtn = Button(form, text = "Log In", command = LogForm)



treeView = ttk.Treeview(form, selectmode= "browse")

treeView['columns'] = ("1","2")
treeView['show'] = 'headings'

treeView.column("1", width = 100, anchor ='c') 
treeView.column("2", width = 50, anchor ='c') 

treeView.heading("1", text ="Username") 
treeView.heading("2", text ="Score") 

LogBtn.grid(row = 0, column= 0, padx=15 )
Startbtn.grid(row = 1, column= 0, padx=15 )
Timerlbl.grid(row = 2, column= 0 , padx=15)
Clickerbtn.grid(row = 3, column= 0 , padx=15)
Pacelbl.grid(row = 4, column= 0 , padx=15 )
treeView.grid(row = 0, column = 1, sticky= W, rowspan=5, padx=5, pady= 5)
if userName == "":
     Startbtn["state"] = "disabled"
else:
    LogBtn["state"] = "disabled"
    Startbtn["state"] ="enabled"

listThread()
form.mainloop()
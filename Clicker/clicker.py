
from faulthandler import disable
from os import stat
from tkinter import *
from tkinter import messagebox
import time
from threading import *
from tkinter import ttk
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

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
    updateData(pace)
    getData()

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
    f = open("scores.txt", "r")
    fileData = f.readlines()
    f.close()
    treeView.delete(*treeView.get_children())
    for set in fileData:
        subset = set.split(" ")
        treeView.insert("", 'end',  
             values =(subset[0], subset[1]))
    
    
def updateData(pace): 
    f = open("scores.txt", "r")
    fileData = f.readlines()
    x = True
    for set in fileData:
        subset = set.split(" ")
        if subset[0]== userName:
            pattern = set
            x = False
            global ctr
            print(pace)
            subst = subset[0] + " " + str(pace) +"\n"
    f.close()
    if x == True:
        f = open("scores.txt", "a")
        f.write(userName + " " + str(pace)+ "\n")
        f.close()
    else:
        #Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open("scores.txt") as old_file:
                for line in old_file:
                    new_file.write(line.replace(pattern, subst))
        #Copy the file permissions from the old file to the new file
        copymode("scores.txt", abs_path)
        #Remove original file
        remove("scores.txt")
        #Move new file
        move(abs_path, "scores.txt")
    

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

def save():
    global userName
    userName = UserTxt.get("1.0", "end-1c")
    Startbtn["state"] ="normal"


UserTxt = Text(form, height = 1, width= 15)
UserTxt.grid(row = 0, column= 0, columnspan=2, sticky=W, pady=15, padx=50)
Savebtn = Button(form, text = "Save", command =save)
Savebtn.grid(row = 0, column= 0, columnspan=2, sticky=W, padx=15)



ctrString = StringVar()
timerLabel = StringVar()
ctrString.set("Your Clicks: ")

Startbtn = Button(form, text = "Start your test", command = timerThread, state="disabled")
Clickerbtn = Button(form, text = "Click!",bg = "red",
    highlightcolor = "red", width = 20, height= 5, command = counter,
    state= "disabled")
Timerlbl = Label(form, textvariable= timerLabel) 
Pacelbl = Label(form, textvariable = ctrString )




treeView = ttk.Treeview(form, selectmode= "browse")

treeView['columns'] = ("1","2")
treeView['show'] = 'headings'

treeView.column("1", width = 100, anchor ='c') 
treeView.column("2", width = 50, anchor ='c') 

treeView.heading("1", text ="Username") 
treeView.heading("2", text ="Score") 


Startbtn.grid(row = 1, column= 0, padx=15 )
Timerlbl.grid(row = 2, column= 0 , padx=15)
Clickerbtn.grid(row = 3, column= 0 , padx=15)
Pacelbl.grid(row = 4, column= 0 , padx=15 )
treeView.grid(row = 0, column = 1, sticky= W, rowspan=5, padx=5, pady= 5)

if userName == "":
     Startbtn["state"] = "disabled"

listThread()
form.mainloop()
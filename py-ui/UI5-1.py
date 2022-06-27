from datetime import date
import requests
from requests.structures import CaseInsensitiveDict
import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText



root = Tk()
root.config(bg="#394766")
root.title("Vertretungsplan UI 5.1")
root.geometry("1000x600")

content = ttk.Frame(root, padding=(0,0,0,0))
content.grid(column=0, row=0, sticky=(N, S, E, W))

frame2 = Frame(root, bg="#1c2333")

def show_frame(frame):
    frame.tkraise()

def toInput():
    show_frame(content)
    runbutton = Button(root, width=100, height=5, bg="#394766", fg="white", text="Ausführen", command=lambda:run(False))
    runbutton.grid(column=0, row=1, sticky=(N, S, E, W))

def toOutput():
    runbutton2 = Button(root, width=100, height=5, bg="#394766", fg="white", text="Schließen", command=lambda:toInput())
    runbutton2.grid(row=1, column=0, sticky=(S, E, W))

for frame in (content, frame2):
    frame.grid(row=0, column=0, sticky=(N, S, E, W))

show_frame(content)

url = "https://nessa.webuntis.com/WebUntis/monitor/substitution/data?school=Gym%20Carolinum"

date = date.today()
date = date.strftime("%Y%m%d")


def run(f1):

    if f1 == True:
        show_frame(content)
    elif f1 == False:
        show_frame(frame2)

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"


    tage = dayentry.get()

    nurAusfaelle = nurausfälleentry.get().replace("j", "true").replace("n", "false")

    data = '"formatName":"VP SuS IServ morgen","schoolName":"Gym Carolinum","date":{},"dateOffset":{},"strikethrough":false,"mergeBlocks":true,"showOnlyFutureSub":false,"showBreakSupervisions":true,"showTeacher":true,"showClass":false,"showHour":true,"showInfo":true,"showRoom":true,"showSubject":true,"groupBy":1,"hideAbsent":false,"departmentIds":[],"departmentElementType":-1,"hideCancelWithSubstitution":true,"hideCancelCausedByEvent":false,"showTime":false,"showSubstText":true,"showAbsentElements":[],"showAffectedElements":[1],"showUnitTime":true,"showMessages":true,"showStudentgroup":false,"enableSubstitutionFrom":false,"showSubstitutionFrom":0,"showTeacherOnEvent":false,"showAbsentTeacher":true,"strikethroughAbsentTeacher":false,"activityTypeIds":[],"showEvent":true,"showCancel":true,"showOnlyCancel":{},"showSubstTypeColor":false,"showExamSupervision":false,"showUnheraldedExams":false'.format(
        date, tage, nurAusfaelle)
    data = "{" + data + "}"

    resp = requests.post(url, headers=headers, data=data)
    raw = resp.content.decode("utf-8")
    data = json.loads(raw)

    klasse = klasseentry.get()
    
    toOutput()
    output = ScrolledText(root, width=100, height=12)
    output.grid(row=0, column=0, sticky=(N, S, E, W))
    
    global out
    out = data["payload"]["weekDay"]
    for x in data['payload']['rows']:
        a = x['group']
        if klasse.upper() in a:
            pass
        else:
            continue
        b = x['data']
        c = [a, b]
        
        out = str(out) + "\n" + str(c).replace("[", "").replace("]", "").replace("'", "").replace('<span class="substMonitorSubstElem">',"").replace("</span>", "")
    output.insert(tk.INSERT, str(out))
    out = ""

    output.configure(state ='disabled')

titlebar = Label(content, bg="#1c2333", fg="#4db2ff", text="Vertretungsplan-Tool \n von Heinrich und Silas")
titlebar.grid(column=0, row=0, sticky=(N, S, E, W))
titlebar.config(font=("Courier", 15))

daylabel = Label(content, bg="#1c2333", fg="white", text="Welchen Tag nachschauen \n (0= Heute, 1= Morgen ...)")
daylabel.grid(column=0, row=1, sticky=(N, E, W))
daylabel.config(font=("Courier", 15))

dayentry = Entry(content, width=50, bg="#1c2333", fg="white")
dayentry.grid(column=0, row=2, sticky=(N, E, W))

ausfällelabel = Label(content, bg="#1c2333", fg="white", text="Nur Ausfälle anzeigen? (n/j)")
ausfällelabel.grid(column=0, row=3, sticky=(N, E, W))
ausfällelabel.config(font=("Courier", 16))

nurausfälleentry = Entry(content, width=50, bg="#1c2333", fg="white")
nurausfälleentry.grid(column=0, row=4, sticky=(N, E, W))

klasselabel1 = Label(content, bg="#1c2333", fg="white", text="Nur Klasse/Jahrgang anzeigen?")
klasselabel1.grid(column=0, row=5, sticky=(N, E, W))
klasselabel1.config(font=("Courier", 16))

klasseentry = Entry(content, width=50, bg="#1c2333", fg="white")
klasseentry.grid(column=0, row=6, sticky=(N, S, E, W))

toInput()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)

def close_win(e):
   root.destroy()
root.bind('<Escape>', lambda e: close_win(e))
print("press <Escape> to quiet")

root.mainloop()

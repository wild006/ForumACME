#!/usr/bin/env python3

from tkinter import *
from multilistbox import *

forum = Tk()

def visioner(event, n):
    print(a.sujet.get(a.sujet.curselection()[0]))

def supprimer(event):
    pass
        
class Suj:
    def __init__(self, sujet, date, nb, last, i):
        self.liste = Listbox(forum)
        self.liste.bind('<<ListboxSelect>>', lambda e: visioner(e, i))
        self.liste.insert(END, sujet + " " + date + " " + str(nb) + " " + last)
        self.liste.pack()

class Sujet:
    def __init__(self, _id, sujet, date, nb, dernier, parent):
        self.id = _id
        self.sujet = sujet
        self.date = date
        self.nb = nb
        self.dernier = dernier
        self.parent = parent
        
class SujetView:
    def __init__(self, sujets):
        self.sujet = Listbox(forum)
        self.sujet.grid(row=0,column=0)
        self.nbmess = Listbox(forum)
        self.nbmess.grid(row=0,column=1)
        self.dernier = Listbox(forum)
        self.dernier.grid(row=0,column=2)
        self.visioner = Listbox(forum)
        self.visioner.grid(row=0,column=3)
        self.supprimer = Listbox(forum)
        self.supprimer.grid(row=0,column=4)

        s = []
        n = []
        d = []
        _id = []
        
        for i in sujets:
            _id.append(i.id)
            s.append(i.sujet)
            n.append(i.nb)
            d.append(i.date)
            
        self.populeSujet(s)
        self.populeNb(n)
        self.populeDernier(d)
        self.populeAct(len(sujets))
                         

    def populeSujet(self, sujets):
        for s in sujets:
            self.sujet.insert(END,s)

    def populeNb(self, nbs):
        for i in nbs:
            self.nbmess.insert(END, i)

    def populeDernier(self, lst):
        for l in lst:
            self.dernier.insert(END, l)

    def populeAct(self, n):
        self.sujet.bind('<<ListboxSelect>>', lambda e: visioner(e, 0))
        for i in range(n):
            self.visioner.insert(END, (i, "visioner"))
        for i in range(n):
            self.supprimer.insert(END, Button(forum, text="supprimer", command=supprimer))


mlb = MultiListbox(forum, (('Subject', 40), ('Sender', 20), ('Date', 10)))
for i in range(1000):
    mlb.insert(END, ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
mlb.pack(expand=YES,fill=BOTH)
forum.mainloop()
#s = (Sujet(0, "Premier", "hier", "23", "demain", None),
#     Sujet(1, "Second", "demain", "11", "hier", 0))

#a = SujetView(s)
#but = Button(forum, text="visioner", command=lambda e: visioner(e, 0))

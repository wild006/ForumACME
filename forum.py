#!/usr/bin/env python3

from tkinter import *
from multilistbox import *

forum = Tk()

def visioner(event):
    print (event)

def supprimer(event):
    pass
        
class Sujet:
    def __init__(self, _id, sujet, date, nb, dernier, parent):
        self.id = _id
        self.sujet = sujet
        self.date = date
        self.nb = nb
        self.dernier = dernier
        self.parent = parent

mlb = MultiListbox(forum, (('Message', 40), ('Date', 20), ('Stuff', 10)))
for i in range(1000):
    mlb.insert(END, ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
mlb.pack(expand=YES,fill=BOTH)

btn = Button(forum, text="stuff", command=lambda: visioner(mlb.curselection()))
btn.pack()
forum.mainloop()

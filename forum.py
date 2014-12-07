#!/usr/bin/env python3

from tkinter import *
from multilistbox import *


        
class Sujet:
    def __init__(self, _id, nom, date, nb, dernier, parent):
        self.id = _id
        self.nom = nom
        self.date = date
        self.nb = nb
        self.dernier = dernier
        self.parent = parent

class Vue():
    def __init__(self, commandes):
        self.forum = Tk()
        self.commandes = commandes
        
        self.mlb = MultiListbox(self.forum, (('Message', 40), ('Date', 20), ('Stuff', 10)))
        self.remplirListe()
        #for i in range(1000):
        #    mlb.insert(END, ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
        self.mlb.pack(expand=YES,fill=BOTH)

        btn = Button(self.forum, text="stuff", command=lambda: self.visioner(self.mlb.curselection()))
        btn.pack()

    def remplirListe(self):
        sujets = self.commandes.searchSujet()
        print("sujets", sujets)
        for sujet in sujets:
            self.mlb.insert(END, ('Important Message: ' + sujet.nom, sujet.date, sujet.dernier))

    def visioner(self,event):
       print (event)

    def supprimer(self,event):
        pass

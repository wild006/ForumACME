#!/usr/bin/env python3

from tkinter import *
from multilistbox import *

class User():
    def __init__(self, _id, nom, prenom, username, passwd, mail):
        self.id = _id
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.passwd = passwd
        self.mail = mail

class Message():
    def __init__(self, _id, text, date, auteur, sujetid):
        self.id = _id
        self.texte = text
        self.date = date
        self.auteur = auteur
        self.sujetid = sujetid
        
class Sujet():
    def __init__(self, _id, nom, date, nbMessages, dernier, parent):
        self.id = _id
        self.nom = nom
        self.date = date
        self.nbMessages = nbMessages
        self.dernier = dernier
        self.parent = parent

class Vue():
    def __init__(self, commandes):
        self.forum = Tk()
        self.commandes = commandes
        
        self.mlb = MultiListbox(self.forum, (('Message', 40), ('Date', 20), ('Nombre de messages', 10)))
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
            self.mlb.insert(END, ('Important Message: ' + sujet.nom, sujet.date, sujet.nbMessages))

    def visioner(self,event):
       print (event)

    def supprimer(self,event):
        pass

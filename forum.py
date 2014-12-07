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

class SujetVue():
    def __init__(self, commandes):
        self.forum = Tk()
        self.commandes = commandes
        
        self.boxSujet = MultiListbox(self.forum, (('Message', 40), ('Date', 20), ('Nombre de messages', 10)))
        self.remplirListe()
        self.boxSujet.pack(expand=YES,fill=BOTH)

        btn = Button(self.forum, text="stuff", command=lambda: self.visioner(self.boxSujet.curselection()))
        btn.pack()

    def remplirListe(self):
        sujets = self.commandes.searchSujet() #[Sujet(0, "Un", "hier", "2", "demain", None), Sujet(1, "Deux", "demain", "3", "hier", None)]
        for sujet in sujets:
            self.boxSujet.insert(END, ('Important Message: ' + sujet.nom, sujet.date, sujet.nbMessages))

    def visioner(self, event):
        MessageVue(event[0], self.commandes)

    def supprimer(self, event):
        pass

class MessageVue():
    def __init__(self, n, commandes):
        """Affiche les messages du sujet a l'id `n'"""
        self.commandes = commandes
        self.id = n
        self.mess = Tk()
        self.message = MultiListbox(self.mess, (('Texte', 40), ('Auteur', 20), ('Date', 10)))
        self.message.pack(expand=YES, fill=BOTH)
        self.remplirListe()

    def remplirListe(self):
        messages = self.commandes.trouveSujet(self.id) #[Message(0, "Premier", "Jamais", "Moi", self.id), Message(1, "Second", "Toujours", "L'autre", self.id)]
        for m in messages:
            self.message.insert(END,(m.texte, m.auteur, m.date))

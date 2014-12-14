#!/usr/bin/env python3

from tkinter import *
from PIL import Image, ImageTk

class MesssageCanvas():
    def __init__(self,parent,messageVue, message):
        self.parent = parent #root
        self.message = message
        self.messageVue = messageVue
        self.canevas = Canvas(self.parent, bg="white", width=800, height=175)
        self.draw()
        self.canevas.pack()

    def draw(self):
        self.texteMessage = self.canevas.create_text(200,50,font=("Arial",12),anchor=NW, justify=LEFT, text=self.message.texte, width=600)
        self.texteUser = self.canevas.create_text(70,130,text=self.message.auteur)
        self.texteUser = self.canevas.create_text(600,20,anchor=NW,text=self.message.date)

        image = Image.open("moyen_profil.jpg")
        self.imageProfilTk = ImageTk.PhotoImage(image)
        self.imageProfil = self.canevas.create_image(20,20,anchor=NW,image=self.imageProfilTk, tags="profil")
        #self.rectangleTexte = self.canevas.create_rectangle(self.canevas.bbox(self.texteMessage),fill="grey")
        #self.canevas.tag_lower(self.rectangleTexte,self.texteMessage)
        image = Image.open("repondre_bouton.jpg")
        self.imageBoutonRepondreTk = ImageTk.PhotoImage(image)
        self.imageBoutonRepondre = self.canevas.create_image(525,130,anchor=NW,image=self.imageBoutonRepondreTk, tags="boutonRepondre")
        image = Image.open("supprimer_bouton.jpg")
        self.imageBoutonSupprimerTk = ImageTk.PhotoImage(image)
        self.imageBoutonSupprimer = self.canevas.create_image(650,130,anchor=NW,image=self.imageBoutonSupprimerTk, tags="boutonSupprimer")

        self.canevas.tag_bind("boutonRepondre", '<ButtonPress-1>', self.repondre)
        self.canevas.tag_bind("boutonSupprimer", '<ButtonPress-1>', self.supprimer)

    def repondre(self,event):
        print("repondre")
        self.messageVue.repondre(self.message)

    def supprimer(self,event):
        print("supprimer")
        self.messageVue.supprimer(self.message)

def main():
    root = Tk()
    #root.wm_title("Multi-Column List")
    #root.wm_iconname("mclist")

    #import plastik_theme
    #plastik_theme.install('~/tile-themes/plastik/plastik')

    message1 = MesssageCanvas(root, None, None)
    root.mainloop()

if __name__ == "__main__":
    main()

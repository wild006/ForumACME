import mysql.connector
import re
from forum import *

nomDB = "FORUM"

class Commandes():
    def __init__(self):
        self.startUp()
        self.v = Vue(self)
        self.v.forum.mainloop()

        
    def startUp(self):
        try:
            nomDB = "FORUM"
            self.db = mysql.connector.connect(user='root', password='AAAaaa111',
                                          host='127.0.0.1',
                                         database= nomDB)
            #Tester toutes les tables ? (Corrumption)
        except:
            print("pas créé !")
            self.db = mysql.connector.connect(host="localhost",
                                         user="root",passwd="AAAaaa111")
            self.executeScript("forumDB.sql", self.db)
            self.db = mysql.connector.connect(user='root', password='AAAaaa111',
                                          host='127.0.0.1',
                                         database= nomDB)
            self.executeScript("forumTables.sql", self.db)

        self.executeCommand("INSERT INTO SUJET(nom, date) VALUES('LOL', '1776-7-4 04:13:54')")
        self.executeCommand("INSERT INTO SUJET(nom, date) VALUES('Pourquoi pas ? ', '1776-7-4 04:13:54')")

    def executeCommand(self,command):
        #POUR DES TESTS !
        cursor = self.db.cursor()
        cursor.execute(command)
    
    def executeScript(self,path,db):
        file = open(path, 'r')
        fileCommands = file.read()
        file.close()

        sqlCommands = fileCommands.split(';')

        for command in sqlCommands:
            print(command)
            regex = re.search(r'\S', command, re.I)
            if regex:
                cursor = db.cursor()
                cursor.execute(command)
            else:
                print("pas valide")
                print(command)


    def creerUser(self,nom,prenom,username,passwd,mail):
        if searchUser(username):
            pass

    def searchUser(self,username):
        try:
            cursor = self.db.cursor()
            command = "SELECT * FROM USER WHERE username = " + username
            print(command)
            cursor.execute(command)
            print("cursor", cursor)
        except:
            print("pas trouvé")

    def searchSujet(self):
        cursor = -1 #Pas trouvé
        try:
            cursor = self.db.cursor()
            command = "SELECT * FROM SUJET"
            print(command)
            cursor.execute(command)
            print("cursor", cursor)
        except:
            print("pas trouvé")

        sujets = []
        for (_id, nom, date, dernier,parent) in cursor:
            sujet = Sujet(_id,nom,date,0,dernier,parent)
            print("i", _id,nom,date,dernier,parent)
            sujets.append(sujet)
        return sujets

    def connectionUser(self):
        pass

    def nouveauMessage(self):
        pass


class User():
    def __init__(self, _id,nom,prenom,username,passwd, mail):
        self.id = _id
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.passwd = passwd
        self.mail = mail

def main():
    c = Commandes()
    #searchUser("Luc",db)
    #searchUser("Luc",db)
    if c.db:
        c.db.close() 

if __name__ == "__main__":
    main()

import mysql.connector
import re
from forum import *

nomDB = "FORUM"

class Commandes():
    def __init__(self):
        self.startUp()
        self.v = SujetVue(self)
        self.v.forum.mainloop()

    def startUp(self):
        try:
            self.nomDB = "FORUM"
            db = mysql.connector.connect(user='root', password='AAAaaa111',
                                          host='127.0.0.1',
                                         database= nomDB)
            #Tester toutes les tables ? (Corrumption)
        except:
            print("pas créé !")
            db = mysql.connector.connect(host="localhost",
                                         user="root",passwd="AAAaaa111")
            self.executeScript("forumDB.sql", db)
            db = self.connectionDB('root','AAAaaa111','127.0.0.1',self.nomDB)
            self.executeScript("forumTables.sql", db)

        #POUR DES TESTS
        #INSERTION DE SUJETS
        self.executeCommand("INSERT INTO SUJET(nom, date) VALUES('LOL', '1776-7-4 04:13:54')", True)
        self.executeCommand("INSERT INTO SUJET(nom, date) VALUES('Pourquoi pas ? ', '1776-7-4 04:13:54')", True)
        #INSERTION DE MESSAGES
        idSujet = self.trouveIdSujet("'LOL'")
        print("id",idSujet)
        if idSujet:
            self.executeCommand("INSERT INTO MESSAGE(texte, sujet) VALUES('Un message très important !!', " + str(idSujet) + ")", True)

    def connectionDB(self,user, password, host, nomBD):
        return mysql.connector.connect(user=user, password=password,
                                          host=host,
                                         database= nomDB)

    def executeCommand(self,command, commit = False):
        #POUR DES TESTS !
        db = self.connectionDB('root','AAAaaa111','127.0.0.1',self.nomDB)
        cursor = db.cursor()
        cursor.execute(command)
        if commit:
            db.commit()
        db.close()

    def trouveIdSujet(self,nomSujet):
        try:
            db = self.connectionDB('root','AAAaaa111','127.0.0.1',self.nomDB)
            cursor = db.cursor()
            command = "SELECT id FROM SUJET WHERE nom = " + nomSujet
            print(command)
            cursor.execute(command, (nomSujet))
            print("cursor", cursor)
            result = cursor.fetchone()#Il devrait avoir qu'un sujet avec ce nom...
            db.close()
            return result[0]
        except:
            print("pas trouvé")
            db.close()

        return None
    
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
            db = self.connectionDB('root','AAAaaa111','127.0.0.1',self.nomDB)
            cursor = db.cursor()
            command = "SELECT * FROM SUJET"
            print(command)
            cursor.execute(command)
            print("cursor", cursor)
        except:
            print("pas trouvé")

        sujets = []
        for (_id, nom, date, dernier,parent) in cursor:
            nbMessages = self.searchNbMessages("'" + nom + "'")
            sujet = Sujet(_id,nom,date,nbMessages,dernier,parent)
            print("i", _id,nom,date,dernier,parent)
            sujets.append(sujet)
        db.close()
        return sujets

    def searchNbMessages(self,sujet):
        if True:
            db = self.connectionDB('root','AAAaaa111','127.0.0.1',self.nomDB)
            cursor = db.cursor()
            print(sujet)
            idSujet = self.trouveIdSujet(sujet)
            if idSujet == None:
                return 0
            command = "SELECT COUNT(*) FROM MESSAGE WHERE sujet = " + str(idSujet)
            print(command)
            cursor.execute(command)
            print("cursor", cursor)

            result = cursor.fetchone()
            db.close()
            print(result[0])
            return result[0]
        else:
            print("pas trouvé")
            db.close()
            
        return 0

        

    def connectionUser(self):
        pass

    def nouveauMessage(self):
        pass


def main():
    c = Commandes()
    #searchUser("Luc",db)
    #searchUser("Luc",db)

if __name__ == "__main__":
    main()

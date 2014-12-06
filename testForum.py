import mysql.connector
import re

nomDB = "FORUM"

def executeScript(path,db):
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


def creerUser(nom,prenom,username,passwd,mail):
    if searchUser(username):
        pass

def searchUser(username, db):
    try:
        cursor = db.cursor()
        command = "SELECT * FROM USER WHERE username = " + username
        print(command)
        cursor.execute(command)
        print("cursor", cursor)
    except:
        print("pas trouvé")

def connectionUser():
    pass

def nouveauMessage():
    pass

def main():
    try:
        nomDB = "FORUM"
        db = mysql.connector.connect(user='root', password='AAAaaa111',
                                      host='127.0.0.1',
                                     database= nomDB)
        #Tester toutes les tables ? (Corrumption)
    except:
        print("pas créé !")
        db = mysql.connector.connect(host="localhost",
                                     user="root",passwd="AAAaaa111")
        executeScript("forumDB.sql", db)
        db = mysql.connector.connect(user='root', password='AAAaaa111',
                                      host='127.0.0.1',
                                     database= nomDB)
        executeScript("forumTables.sql", db)

    searchUser("Luc",db)
    searchUser("Luc",db)
    db.close() 

class User():
    def __init__(self, _id,nom,prenom,username,passwd, mail):
        self.id = _id
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.passwd = passwd
        self.mail = mail
        




if __name__ == "__main__":
    main()

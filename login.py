from tkinter import *
import hashlib
import time
from tkinter.messagebox import showerror, showinfo
import sqlite3

conn = sqlite3.connect('login.sqlite')
c = conn.cursor()

t = 'CREATE TABLE IF NOT EXISTS LoginCredentials (username VARCHAR (32), password VARCHAR (32), userID INTEGER PRIMARY KEY AUTOINCREMENT)'
c.execute(t)
conn.commit()

def forget(widget):
    widget.place_forget()

def addNewUserPage():
    global resultStr

    newUserFrame = Frame(root)
    newUserFrame.place(x=0,y=0,width=500,height=520)

    txt1=Label(root, text="ESTOQUE INTELIGENTE",bg="#008", fg= "#999")
    txt1.place(x=0,y=0,width=500,height=50)

    usernameLabel = Label(newUserFrame, text="Criar um usuário:")
    usernameEntry = Entry(newUserFrame, width=30)
    usernameLabel.place(x=150,y=80,width=200,height=20)
    usernameEntry.place(x=150,y=100,width=200,height=20)

    passwordLabel = Label(newUserFrame, text="Criar uma senha:")
    passwordEntry = Entry(newUserFrame, show="*", width=30)
    passwordLabel.place(x=150,y=140,width=200,height=20)
    passwordEntry.place(x=150,y=160,width=200,height=20)

    resultStr = StringVar()
    result = Label(newUserFrame,textvariable=resultStr)
    result.place(relx=.45,rely=.7)

    enter = Button(newUserFrame,text="Entrar", fg="green", command=lambda: insertToDB(usernameEntry.get(), passwordEntry.get()))
    enter.place(x=190,y=210,width=120,height=20)

    back = Button(newUserFrame,text="Voltar",command=lambda: forget(newUserFrame))
    back.place(x=190,y=240,width=120,height=20)

def insertToDB(username, password):
    hashedUsername = hashlib.md5(username.encode('UTF-8')).hexdigest()
    hashedPassword = hashlib.md5(password.encode('UTF-8')).hexdigest()

    c.execute("INSERT INTO LoginCredentials(username,password) VALUES (?,?)",(hashedUsername,hashedPassword))
    conn.commit()

    showinfo('Usuário criado', 'Usuário criado com sucesso')

def authenticate(username,password):

    result_of_login = StringVar()
    resultLabel = Label(mainMenu, textvariable=result_of_login)
    resultLabel.place(relx=.45,rely=.7)


    c.execute("SELECT COUNT (*) FROM LoginCredentials")
    dbcount = c.fetchall()
    if dbcount[0][0] == 0:
        showerror('ERRO', 'Nenhum usuário cadastrado no banco de dados')
        return

    else:
        matchedUsername = False
        matchedPassword = False

        hashedUsername = hashlib.md5(username.encode('UTF-8')).hexdigest()
        hashedPassword = hashlib.md5(password.encode('UTF-8')).hexdigest()

        c.execute("SELECT username FROM LoginCredentials")
        query = c.fetchall()

        length = len(query)

        for i in range(length):
            dbUsername = query[i][0]

            if dbUsername == hashedUsername:
                matchedUsername = True
                c.execute("SELECT userID FROM LoginCredentials WHERE username = ?",(hashedUsername,))
                idnum = c.fetchall()

        if matchedUsername == True:
            length = len(idnum)

            for i in range(length):
                c.execute("SELECT password FROM LoginCredentials WHERE userID = ?",(idnum[i][0],))
                query = c.fetchall()

                if query[i][0] == hashedPassword:
                    matchedPassword = True

        if matchedUsername == True and matchedPassword == True:
            root.destroy()
            time.sleep(0.1)
            import Registration_System
            return
        else:
            showerror('ERRO', 'Login e/ou senha errado, tente novamente')
            return



root = Tk()
root.title("ESTOQUE INTELIGENTE - LOGIN")
root.geometry("500x300")
root.configure(background="#999")

mainMenu = Frame(root)
mainMenu.place(x=0,y=0,width=500,height=520)

txt1=Label(root, text="ESTOQUE INTELIGENTE",bg="#008", fg= "#999")
txt1.place(x=0,y=0,width=500,height=50)

usernameLabel = Label(mainMenu, text="Usuário:")
usernameEntry = Entry(mainMenu, width=30)
usernameLabel.place(x=150,y=80,width=200,height=20)
usernameEntry.place(x=150,y=100,width=200, height=20)

passwordLabel = Label(mainMenu, text="Senha:")
passwordEntry = Entry(mainMenu, width=30,show="*")
passwordLabel.place(x=150,y=140,width=200,height=20)
passwordEntry.place(x=150,y=160,width=200, height=20)

enter = Button(mainMenu,text="Entrar",fg="green",command=lambda: authenticate(usernameEntry.get(),passwordEntry.get()))
enter.place(x=190,y=210,width=120,height=20)

newUserButton = Button(mainMenu, text="Criar uma conta", command=addNewUserPage)
newUserButton.place(x=190,y=240,width=120,height=20)

root.mainloop()
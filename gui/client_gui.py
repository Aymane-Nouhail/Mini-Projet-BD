from tkinter import *
import sqlite3
from tkinter.ttk import *
import customtkinter

root_client = Tk()
root_client.title('Client')
root_client.iconbitmap('./marisa_icon.ico')
root_client.geometry("470x400")


#Create a database or connect to one
conn = sqlite3.connect('clients.db')

#creating cursor
c = conn.cursor()

#enabling the use of foreign keys 
conn.execute("PRAGMA foreign_keys = 1")

#Creating the table (if first use
c.execute("""
CREATE TABLE IF NOT EXISTS clients(
   ID_client INT,
   nom_client text,
   adresse_client text,
   PRIMARY KEY(ID_client)
);
""")

def clear_input_lines_clients():
    id_client.delete(0,END)
    nom_client.delete(0,END)
    adresse_client.delete(0,END)
    return

def new_window_message(window_title,window_message):
    top = Toplevel()
    top.title(window_title)
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("300x100")
    print_label = Label(top, text=window_message,font=("Calibri",11))
    print_label.grid(row=0,column=0,padx=60,pady=20)
    ok_btn = Button(top, text = "OK", command=top.destroy)
    ok_btn.grid(row=1, column=0, padx=20)
    
def submit():
    conn = sqlite3.connect('clients.db')
    if id_client.get() == '':
        new_window_message("query error","Echec de l'ajout. ID manquant")
        return
    c = conn.cursor()
    c.execute("INSERT INTO clients VALUES(:ID_client, :nom_client, :adresse_client)",
    {
        'ID_client' : id_client.get(),
        'nom_client' : nom_client.get(),
        'adresse_client' : adresse_client.get()
    }
    )
    conn.commit()
    conn.close()
    #clear text boxes
    new_window_message("query confirmation","ajouté avec succès")
    clear_input_lines_clients()

def query():
    top = Toplevel()
    top.title("Table of Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("780x400")
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute("SELECT * from clients;")
    records = c.fetchall()
    records = [("id client : ", "nom client : ", "adresse client : ")]+records
    print(records)
    style = Style()
    style.configure("BW.TLabel", foreground="blue",background="white")
    for i in range(len(records)):
        for j in range(len(records[0])):
            if i==0:
                query_label = Entry(top,width=35,font=('Calibri',11,'bold italic'),style="BW.TLabel")
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                
            else:
                query_label = Entry(top,width=35,font=('Calibri',11,'bold'))
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
    conn.commit()
    conn.close()
    clear_input_lines_clients()

def clear():
    def clear_all():
        conn = sqlite3.connect('clients.db')
        c = conn.cursor()
        c.execute("DELETE FROM clients;")
        conn.commit()
        conn.close()
        top.destroy()
        new_window_message("query confirmation","database cleared successfully")
    top = Toplevel()
    top.title("Confirmation Prompt")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("400x100")
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    print_label= Label(top, text="Are you sure you want to clear the database?",font=("Calibri",11))
    print_label.grid(row=0,column=0,padx=80)
    yes_btn = Button(top, text = "yes", command=clear_all)
    yes_btn.grid(row=1, column=0, padx=20,pady=(10,0))
    no_btn = Button(top, text = "no", command=top.destroy)
    no_btn.grid(row=2, column=0, padx=20,pady=(10,0))
    conn.commit()
    conn.close()

def search():
    top = Toplevel()
    top.title("Table of Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("780x400")
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM clients WHERE
        id_client = :ID_client OR nom_client = :nom_client OR adresse_client = :adresse_client""",
    {
        'ID_client' : id_client.get(),
        'nom_client' : nom_client.get(),
        'adresse_client' : adresse_client.get()
    })
    records = c.fetchall()
    records = [("id client : ", "nom client : ", "adresse client : ")]+records
    print(records)
    style = Style()
    style.configure("BW.TLabel", foreground="blue",background="white")
    for i in range(len(records)):
        for j in range(len(records[0])):
            if i==0:
                query_label = Entry(top,width=35,font=('Calibri',11,'bold italic'),style="BW.TLabel")
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                
            else:
                query_label = Entry(top,width=35,font=('Calibri',11,'bold'))
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
    conn.commit()
    conn.close()

def remove():
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute("""DELETE FROM clients WHERE
        id_client = :ID_client OR nom_client = :nom_client OR adresse_client = :adresse_client""",
    {
        'ID_client' : id_client.get(),
        'nom_client' : nom_client.get(),
        'adresse_client' : adresse_client.get(),
    })
    conn.commit()
    conn.close()
    new_window_message("query confirmation","client deleted successfully")
    clear_input_lines_clients()
    

##### ENTRIES #####
id_client = Entry(root_client,width=30)
id_client.grid(row=0, column=1, padx=20,pady=(10,0))

nom_client = Entry(root_client,width=30)
nom_client.grid(row=1, column=1, padx=20)

adresse_client = Entry(root_client,width=30)
adresse_client.grid(row=2, column=1, padx=20)

##### TEXTBOX LABELS #####
id_client_label = Label(root_client, text="Identifiant du client")
id_client_label.grid(row=0, column=0,pady=(10,0))

nom_client_label = Label(root_client, text="Nom du client")
nom_client_label.grid(row=1, column=0)

adresse_client_label = Label(root_client, text="Adresse du client")
adresse_client_label.grid(row=2, column=0)

##### BUTTONS #####

submit_btn = customtkinter.CTkButton(root_client, text = "Add record to database", command=submit)
submit_btn.grid(row = 3, column=0, columnspan=2, padx=65, pady=(40,10),ipadx=80)

query_btn = customtkinter.CTkButton(root_client, text="Show all records in database", command=query)
query_btn.grid(row = 4, column=0, columnspan=2, padx=65, pady=10,ipadx=65)

clear_btn = customtkinter.CTkButton(root_client, text="Clear/Erase all records in database", command=clear)
clear_btn.grid(row=5, column=0, columnspan=2, padx=65, pady=10,ipadx=47)

search_btn = customtkinter.CTkButton(root_client, text="Search for a record in database", command=search)
search_btn.grid(row=6, column=0, columnspan=2, padx=65, pady=10,ipadx=59)

remove_btn = customtkinter.CTkButton(root_client, text="Remove an element from the database",command=remove)
remove_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=10,ipadx=40)

#commit changes and close
conn.commit()
root_client.mainloop()
conn.close()

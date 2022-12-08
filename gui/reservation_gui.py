# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 21:27:03 2022

@author: Mehdi
"""

from tkinter import *
import sqlite3
from tkinter.ttk import *



root_reservation = Tk()
root_reservation.title('Onglet reservation')
root_reservation.iconbitmap('./marisa_icon.ico')
myLabel = Label(root_reservation, text="Hello World!")
root_reservation.geometry("470x400")

#Create a database or conntect to one
conn = sqlite3.connect('reservation.db')

#creating cursor
c = conn.cursor()

#enabling the use of foreign keys 
conn.execute("PRAGMA foreign_keys = 1")
#c.execute("DROP TABLE maison;")
'''
#create a table

c.execute("""
    
    CREATE TABLE maison(
       ID_maison INT,
       nom_maison text,
       Loyer DECIMAL(15,2),
       nb_chambres text,
       nb_personnnes_max INT,
       nom_ile text,
       PRIMARY KEY(ID_maison),
       CONSTRAINT loyer_min CHECK(loyer>=100)
    );
          
   CREATE TABLE clients(
   ID_client INT,
   nom_client text,
   adresse_client text,
   PRIMARY KEY(ID_client),
);
          
CREATE TABLE reservation(
   ID_maison INT,
   ID_client INT,
   NUM_semaine INT,
   PRIMARY KEY(ID_maison, ID_client),
   
   FOREIGN KEY (id_maison)
   REFERENCES maison(id_maison),
   
   FOREIGN KEY (id_table2)
   REFERENCES client(id_client)),

    Constraint ck_numsemaine CHECK(NUM_semaine>10 and NUM_semaine<40) ;
    );
""")
'''


#create submit function

def submit():
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    #Inserting into table
    c.execute("INSERT INTO reservation VALUES(:ID_maison, :ID_client, :NUM_semaine)",
    {
        'ID_maison' : id_maison.get(),
        'ID_client' : id_client.get(),
        'NUM_semaine' : num_semaine.get()
    }
    )
    conn.commit()
    conn.close()
    #clear text boxes
    #useless
    id_maison.delete(0,END)
    id_client.delete(0,END)
    num_semaine.delete(0,END)

#create Query function
def query():
    top = Toplevel()
    top.title("Table of Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("1150x400")
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    #top.configure(bg='green')
    #Selecting from table
    c.execute("SELECT * from clients;")
    records = c.fetchall()
    records = [("id client : ", "nom client : ", "adresse client : ")] + records
    print(records)
    style = Style()
    style.configure("BW.TLabel", foreground="blue",background="white")
    for i in range(len(records)):
        for j in range(len(records[0])):
            if i==0:
                query_label = Entry(top,width=25,font=('Calibri',11,'bold italic'),style="BW.TLabel")
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                #query_label.config(state=DISABLED)
                #query_label.configure(style="BW.TLabel")
            else:
                query_label = Entry(top,width=25,font=('Calibri',11,'bold'))
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                #query_label.config(state=DISABLED)
    conn.commit()
    conn.close()
    #clearing all windows
    clear_input_lines_client()
    return

#create clear function
def clear():
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    #deleting everything from table
    c.execute("DELETE from maison;")
    conn.commit()
    conn.close()
    
def search():
    top = Toplevel()
    top.title("Search Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("1150x400")
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM maison WHERE
        id_maison = :ID_maison OR ID_client = :ID_client OR NUM_semaine= :NUM_semaine""",
    {
        'ID_maison' : id_maison.get(),
        'ID_client' : id_client.get(),
        'NUM_semaine' : num_semaine.get()
    })
    records = c.fetchall()
    records = [("identifiant","nom","loyer","nombre de chambres", "nombre des personnes max.","l'ile de la maison")] + records
    print(records)
    style = Style()
    style.configure("BW.TLabel", foreground="blue",background="white")
    for i in range(len(records)):
        for j in range(len(records[0])):
            if i==0:
                query_label = Entry(top,width=25,font=('Calibri',11,'bold italic'),style="BW.TLabel")
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                #query_label.config(state=DISABLED)
                #query_label.configure(style="BW.TLabel")
            else:
                query_label = Entry(top,width=25,font=('Calibri',11,'bold'))
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                #query_label.config(state=DISABLED)
    conn.commit()
    conn.close()
    #clearing all windows
    clear_input_lines_maison()
    return records[1:]
def search_new_window():
    top = Toplevel()
    top.title("Search Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("100x100")
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM maison WHERE
        id_maison = :ID_maison OR ID_client = :ID_client OR NUM_semaine= :NUM_semaine""",
    {
        'ID_maison' : id_maison.get(),
        'ID_client' : id_client.get(),
        'NUM_semaine' : num_semaine.get()
    })
    records = c.fetchall()
    records[-1] = [("identifiant maison","identifiant client","num semaine")]
    for i in range(len(records)):
        query_label = Entry(top, width=20,font=('Arial',16,'bold'))
        query_label.grid(row=i,column=0)
        query_label.insert(END, records[i][0])
        for j in range(len(records[0])):
            query_label = Entry(top, width=20,font=('Arial',16,'bold'))
            query_label.grid(row=i,column=j)
            query_label.insert(END, records[i][j])
    conn.commit()
    conn.close()
    #clearing all windows
    id_maison.delete(0,END)
    id_client.delete(0,END)
    num_semaine.delete(0,END)
   
def modify():
    top = Toplevel()
    top.title("Modifier")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("400x400")
    
    newvalues= Label(top, text="Enter new values :")
    newvalues.grid(row=0,column=0)
    id_maisonmod = Entry(top,width=30)
    id_maisonmod.grid(row=1, column=1, padx=20,pady=(10,0))

    id_clientmod = Entry(top,width=30)
    id_clientmod.grid(row=2, column=1, padx=20)

    num_semainemod = Entry(top,width=30)
    num_semainemod.grid(row=3, column=1, padx=20)
    #creating text box labels :
    id_maison_labelmod = Label(top, text="Identifiant de la maison")
    id_maison_labelmod.grid(row=1, column=0,pady=(10,0))

    id_client_labelmod = Label(top, text="Identifiant du client")
    id_client_labelmod.grid(row=2, column=0)

    num_semaine_labelmod = Label(top, text="Numero de la semaine")
    num_semaine_labelmod.grid(row=3, column=0)
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    c.execute("""UPDATE reservation SET ID_maison = :ID_maisonmod, ID_client= :ID_clientmod, NUM_semaine =:NUM_semainemod FROM reservation WHERE ID_maison= :ID_maison OR ID_client= :ID_client OR NUM_semaine= :NUM_semaine""",
    {
        'ID_maison' : id_maison.get(),
        'ID_client' : id_client.get(),
        'NUM_semaine' : num_semaine.get(),
        'ID_maisonmod' : id_maison.get(),
        'ID_clientmod' : id_clientmod.get(),
        'NUM_semainemod' : num_semainemod.get()
    })
    id_maison.delete(0,END)
    id_client.delete(0,END)
    num_semaine.delete(0,END)
   
    
    
#create text box labels
id_maison = Entry(root_reservation,width=30)
id_maison.grid(row=0, column=1, padx=20,pady=(10,0))

id_client = Entry(root_reservation,width=30)
id_client.grid(row=1, column=1, padx=20)

num_semaine = Entry(root_reservation,width=30)
num_semaine.grid(row=2, column=1, padx=20)
#creating text box labels :
id_maison_label = Label(root_reservation, text="Identifiant de la maison")
id_maison_label.grid(row=0, column=0,pady=(10,0))

id_client_label = Label(root_reservation, text="Identifiant du client")
id_client_label.grid(row=1, column=0)

num_semaine_label = Label(root_reservation, text="Numero de la semaine")
num_semaine_label.grid(row=2, column=0)



#Create Submit Button
submit_btn = Button(root_reservation, text = "Add record to database", command=submit)
submit_btn.grid(row = 6, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a Query Button
modify_btn = Button(root_reservation, text="Modify record in database", command=modify)
modify_btn.grid(row = 7, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a Clear Button
clear_btn = Button(root_reservation, text="Clear/Erase all records in database", command=clear)
clear_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a search button
search_btn = Button(root_reservation, text="Search for a record in database", command=search_new_window)
search_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10,ipadx=100)
#commit changes
conn.commit()
root_reservation.mainloop()
#close connection
conn.close()


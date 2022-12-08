# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 22:27:45 2022

@author: Mehdi
"""

from tkinter import *
import sqlite3
from tkinter.ttk import *

root = Tk()
root.title("Interface Graphique")
root.geometry("720x480")
root.iconbitmap('./marisa_icon.ico')
root.config(background='#ABC8C2')

def pageMaison() :
    maison_reservation=Tk()
    maison_reservation.mainloop()

def pageClient() :
    client_reservation=Tk()
    client_reservation.mainloop()
    
def pageReservation():
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
        id_maison.delete(0,END)
        id_client.delete(0,END)
        num_semaine.delete(0,END)

    #create Query function
    def query():
        conn = sqlite3.connect('DB_project.db')
        c = conn.cursor()
        #Selecting from table
        c.execute("SELECT * from maison;")
        records = c.fetchall()
        query_titles = ["id maison : ", "nom maison : ", "loyer maison : ", "nombre chambres : ", "nombre personnes max : ", "nom ile : "]
        print_records = ''
        for i in range(len(records)):
            print_records += query_titles[i%6] + str(records[i]) + '\n'
        query_label = Label(root_reservation, text = print_records)
        query_label.grid(row = 9, column = 0, columnspan=2)
        print(records)
        conn.commit()
        conn.close()

    #create clear function
    def clear():
        conn = sqlite3.connect('DB_project.db')
        c = conn.cursor()
        #deleting everything from table
        c.execute("DELETE from maison;")
        conn.commit()
        conn.close()

    def search():
        conn = sqlite3.connect('DB_project.db')
        c = conn.cursor()
        c.execute("SELECT * FROM reservation WHERE id_maison = :input_id",{'input_id' : id_maison.get()})
        records = c.fetchall()
        print(records)
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
    query_btn = Button(root_reservation, text="Show all records in database", command=query)
    query_btn.grid(row = 7, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

    #Create a Clear Button
    clear_btn = Button(root_reservation, text="Clear/Erase all records in database", command=clear)
    clear_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

    #Create a search button
    search_btn = Button(root_reservation, text="Search for a record in database", command=search)
    search_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10,ipadx=100)
    #commit changes
    conn.commit()
    root_reservation.mainloop()
    #close connection
    conn.close()


    root_reservation.mainloop()
    
Maisonbutton= Button(root, text="Maison", command=pageMaison)
Maisonbutton.grid(row=0, column=1,columnspan=2, padx=20,pady=(100,0))

Clientbutton= Button(root, text="Client", command=pageClient)
Clientbutton.grid(row=1, column=1,columnspan=2, padx=20)
Reservationbutton=Button(root, text="Reservation", command=pageReservation)
Reservationbutton.grid(row=2, column=1,columnspan=2, padx=20)

root.mainloop()
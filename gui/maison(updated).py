from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('Codemy.com - TreeBase')
root.iconbitmap('./marisa_icon.ico')
root.geometry("1000x550")

# Read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = parser.get('colors', 'primary_color')
saved_secondary_color = parser.get('colors', 'secondary_color')
saved_highlight_color = parser.get('colors', 'highlight_color')

def query_database():
	# Clear the Treeview
	for record in my_tree.get_children():
		my_tree.delete(record)
		
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("SELECT rowid, * FROM maison")
	records = c.fetchall()
	
	# Add our data to the screen
	global count
	count = 0
	
	#for record in records:
	#	print(record)
	print(records)

	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[3], record[4],record[5]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[3], record[4], record[5]), tags=('oddfrow',))
		# increment counter
		count += 1


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()


def search_records():
	lookup_record_nom_maison = search_entry_nom_maison.get()
	lookup_record_loyer = search_entry_loyer.get()
	lookup_record_nb_personnes_max = search_entry_nb_personnes_max.get()
	lookup_record_nb_chambres = search_entry_nb_chambres.get()
	lookup_record_nom_ile = search_entry_nom_ile.get()
	# close the search box
	search.destroy()
	
	# Clear the Treeview
	for record in my_tree.get_children():
		my_tree.delete(record)
	
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()
	records = []
	#c.execute("SELECT rowid, * FROM maison WHERE nom_maison like ? OR loyer like=?", (lookup_record_nom_maison,),(lookup_record_loyer,))
	if lookup_record_nom_maison != '':
		c.execute("SELECT rowid, * FROM maison WHERE nom_maison like :nom_maison",
			{
				'nom_maison':lookup_record_nom_maison,
			})
		records = c.fetchall()
	if lookup_record_loyer != '':
		c.execute("SELECT rowid, * FROM maison WHERE loyer=:loyer",
			{
				'loyer':lookup_record_loyer,
			})
		records += c.fetchall()
	if lookup_record_nb_chambres != '':
		c.execute("SELECT rowid, * FROM maison WHERE nb_chambres=:nb_chambres",
			{
				'nb_chambres':lookup_record_nb_chambres,
			})
		records += c.fetchall()
	
	'''c.execute("SELECT rowid, * FROM maison WHERE nb_personnes_max=:nb_personnes_max",
		{
			'nb_personnes_max':lookup_record_nb_personnes_max,
		})
	records += c.fetchall()'''
	if lookup_record_nom_ile != '':
		c.execute("SELECT rowid, * FROM maison WHERE nom_ile like :nom_ile",
			{
				'nom_ile':lookup_record_nom_ile,
			})
		records += c.fetchall()
	# Add our data to the screen
	global count
	count = 0
	#for record in records:
	#	print(record)


	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[3], record[4],record[5]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[3], record[4], record[5]), tags=('oddfrow',))
		# increment counter
		count += 1


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

'''
def search_records():
	lookup_record_nom_maison = search_entry_nom_maison.get()
	lookup_record_loyer = search_entry_loyer.get()
	lookup_record_id = search_entry_id.get()
	# close the search box
	search.destroy()
	
	# Clear the Treeview
	for record in my_tree.get_children():
		my_tree.delete(record)
	
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	#c.execute("SELECT rowid, * FROM maison WHERE nom_maison like ? OR loyer like=?", (lookup_record_nom_maison,),(lookup_record_loyer,))
	c.execute("SELECT rowid, * FROM maison WHERE nom_maison like :nom_maison",
		{
			'nom_maison':lookup_record_nom_maison,
		})
	records = c.fetchall()
	c.execute("SELECT rowid, * FROM maison WHERE loyer=:loyer",
		{
			'loyer':lookup_record_loyer,
		})
	records += c.fetchall()
	c.execute("SELECT rowid, * FROM maison WHERE oid=:id",
		{
			'id':lookup_record_id,
		})
	records += c.fetchall()
	print(records)
	# Add our data to the screen
	global count
	count = 0
	
	#for record in records:
	#	print(record)


	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4]), tags=('oddrow',))
		# increment counter
		count += 1


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()
'''
def lookup_records():
	global search_entry_nom_maison, search_entry_loyer, search_entry_nb_chambres, search_entry_nb_personnes_max, search_entry_nom_ile, search

	search = Toplevel(root)
	search.title("Lookup Records")
	search.geometry("400x1200")

	# Create label frame
	search_frame_nom_maison = LabelFrame(search, text="Nom Maison")
	search_frame_nom_maison.pack(padx=10, pady=10)

	search_frame_loyer = LabelFrame(search, text="Loyer")
	search_frame_loyer.pack(padx=10, pady=10)

	search_frame_id = LabelFrame(search, text="id")
	search_frame_id.pack(padx=10, pady=10)

	search_frame_nb_chambres = LabelFrame(search, text="Nombre chambres")
	search_frame_nb_chambres.pack(padx=10, pady=10)

	search_frame_nb_personnes_max = LabelFrame(search, text="Nombre personnes max")
	search_frame_nb_personnes_max.pack(padx=10, pady=10)

	search_frame_nom_ile = LabelFrame(search, text="nom ile")
	search_frame_nom_ile.pack(padx=10, pady=10)
	
	# Add entry box
	search_entry_nom_maison = Entry(search_frame_nom_maison, font=("Helvetica", 18))
	search_entry_nom_maison.pack(pady=20, padx=20)

	search_entry_loyer = Entry(search_frame_loyer, font=("Helvetica", 18))
	search_entry_loyer.pack(pady=20, padx=20)

	search_entry_nb_chambres = Entry(search_frame_nb_chambres, font=("Helvetica", 18))
	search_entry_nb_chambres.pack(pady=20, padx=20)

	search_entry_nb_personnes_max = Entry(search_frame_nb_personnes_max, font=("Helvetica", 18))
	search_entry_nb_personnes_max.pack(pady=20, padx=20)

	search_entry_nom_ile = Entry(search_frame_nom_ile, font=("Helvetica", 18))
	search_entry_nom_ile.pack(pady=20, padx=20)

	# Add button
	search_button = Button(search, text="Search Records", command=search_records)
	search_button.pack(padx=20, pady=20)



def primary_color():
	# Pick Color
	primary_color = colorchooser.askcolor()[1]

	# Update Treeview Color
	if primary_color:
		# Create Striped Row Tags
		my_tree.tag_configure('evenrow', background=primary_color)

		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'primary_color', primary_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)


def secondary_color():
	# Pick Color
	secondary_color = colorchooser.askcolor()[1]
	
	# Update Treeview Color
	if secondary_color:
		# Create Striped Row Tags
		my_tree.tag_configure('oddrow', background=secondary_color)
		
		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'secondary_color', secondary_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)

def highlight_color():
	# Pick Color
	highlight_color = colorchooser.askcolor()[1]

	#Update Treeview Color
	# Change Selected Color
	if highlight_color:
		style.map('Treeview',
			background=[('selected', highlight_color)])

		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'highlight_color', highlight_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)

def reset_colors():
	# Save original colors to config file
	parser = ConfigParser()
	parser.read('treebase.ini')
	parser.set('colors', 'primary_color', 'lightblue')
	parser.set('colors', 'secondary_color', 'white')
	parser.set('colors', 'highlight_color', '#347083')
	with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)
	# Reset the colors
	my_tree.tag_configure('oddrow', background='white')
	my_tree.tag_configure('evenrow', background='lightblue')
	style.map('Treeview',
			background=[('selected', '#347083')])

# Add Menu
my_menu = Menu(root)
root.config(menu=my_menu)



# Configure our menu
option_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)
# Drop down menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Reset Colors", command=reset_colors)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

#Search Menu
search_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)
# Drop down menu
search_menu.add_command(label="Search", command=lookup_records)
search_menu.add_separator()
search_menu.add_command(label="Reset", command=query_database)

# Add Fake Data



# Do some database stuff
# Create a database or connect to one that exists
conn = sqlite3.connect('tree_crm.db')

# Create a cursor instance
c = conn.cursor()

# Create Table
c.execute("""
CREATE TABLE IF NOT EXISTS maison(
   nom_maison text,
   Loyer DECIMAL(15,2),
   nb_chambres integer,
   nb_personnnes_max integer,
   nom_ile text,
   CONSTRAINT loyer_min CHECK(loyer>=100)
);
""")
# Add dummy data to table





# Commit changes
conn.commit()

# Close our connection
conn.close()



# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")

# Change Selected Color #347083
style.map('Treeview',
	background=[('selected', saved_highlight_color)])

# Create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("Nom Maison", "Loyer", "ID", "Nombre chambres", "Nombre personnes max", "Nom ile")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Nom Maison", anchor=W, width=140)
my_tree.column("Loyer", anchor=W, width=140)
my_tree.column("ID", anchor=CENTER, width=100)
my_tree.column("Nombre chambres", anchor=CENTER, width=140)
my_tree.column("Nombre personnes max", anchor=CENTER, width=140)
my_tree.column("Nom ile", anchor=CENTER, width=140)


# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Nom Maison", text="Nom Maison", anchor=W)
my_tree.heading("Loyer", text="Loyer", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Nombre chambres", text="Nombres chambres", anchor=CENTER)
my_tree.heading("Nombre personnes max", text="Nombre personnes max", anchor=W)
my_tree.heading("Nom ile", text="Nom ile", anchor=CENTER)



# Create Striped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)



# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

nom_maison_label = Label(data_frame, text="Nom maison")
nom_maison_label.grid(row=0, column=0, padx=10, pady=10)
nom_maison_entry = Entry(data_frame)
nom_maison_entry.grid(row=0, column=1, padx=10, pady=10)

loyer_maison_label = Label(data_frame, text="Loyer")
loyer_maison_label.grid(row=0, column=2, padx=10, pady=10)
loyer_maison_entry = Entry(data_frame)
loyer_maison_entry.grid(row=0, column=3, padx=10, pady=10)

id_entry = Entry(data_frame)

nb_personnes_max_label = Label(data_frame, text="nombre personnes max")
nb_personnes_max_label.grid(row=1, column=2, padx=10, pady=10)
nb_personnes_max_entry = Entry(data_frame)
nb_personnes_max_entry.grid(row=1, column=3, padx=10, pady=10)

nom_ile_label = Label(data_frame, text="Nom ile")
nom_ile_label.grid(row=1, column=4, padx=10, pady=10)
nom_ile_entry = Entry(data_frame)
nom_ile_entry.grid(row=1, column=5, padx=10, pady=10)


nb_chambres_label = Label(data_frame, text="nombre chambres")
nb_chambres_label.grid(row=1, column=0, padx=10, pady=10)
nb_chambres_entry = Entry(data_frame)
nb_chambres_entry.grid(row=1, column=1, padx=10, pady=10)

# Move Row Up
def up():
	rows = my_tree.selection()
	for row in rows:
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move Rown Down
def down():
	rows = my_tree.selection()
	for row in reversed(rows):
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

# Remove one record
def remove_one():
	x = my_tree.selection()[0]
	my_tree.delete(x)

	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	# Delete From Database
	c.execute("DELETE from maison WHERE oid=" + id_entry.get())
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear The Entry Boxes
	clear_entries()

	# Add a little message box for fun
	messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")



# Remove Many records
def remove_many():
	# Add a little message box for fun
	response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	#Add logic for message box
	if response == 1:
		# Designate selections
		x = my_tree.selection()

		# Create List of ID's
		ids_to_delete = []
		
		# Add selections to ids_to_delete list
		for record in x:
			ids_to_delete.append(my_tree.item(record, 'values')[2])

		# Delete From Treeview
		for record in x:
			my_tree.delete(record)

		# Create a database or connect to one that exists
		conn = sqlite3.connect('tree_crm.db')

		# Create a cursor instance
		c = conn.cursor()
		

		# Delete Everything From The Table
		c.executemany("DELETE FROM maison WHERE id = ?", [(a,) for a in ids_to_delete])

		# Reset List
		ids_to_delete = []


		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()

		# Clear entry boxes if filled
		clear_entries()


# Remove all records
def remove_all():
	# Add a little message box for fun
	response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")

	#Add logic for message box
	if response == 1:
		# Clear the Treeview
		for record in my_tree.get_children():
			my_tree.delete(record)

		# Create a database or connect to one that exists
		conn = sqlite3.connect('tree_crm.db')

		# Create a cursor instance
		c = conn.cursor()

		# Delete Everything From The Table
		c.execute("delete from maison where 1>0")
			


		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()

		# Clear entry boxes if filled
		clear_entries()

		# Recreate The Table
		create_table_again()

# Clear entry boxes
def clear_entries():
	# Clear entry boxes
	nom_maison_entry.delete(0, END)
	loyer_maison_entry.delete(0, END)
	id_entry.delete(0, END)
	nb_personnes_max_entry.delete(0, END)
	nom_ile_entry.delete(0, END)


# Select Record
def select_record(e):
	# Clear entry boxes
	nom_maison_entry.delete(0, END)
	loyer_maison_entry.delete(0, END)
	id_entry.delete(0, END)
	nb_chambres_entry.delete(0, END)
	nb_personnes_max_entry.delete(0, END)
	nom_ile_entry.delete(0, END)

	# Grab record Number
	selected = my_tree.focus()
	# Grab record values
	values = my_tree.item(selected, 'values')

	# outpus to entry boxes
	nom_maison_entry.insert(0, values[0])
	loyer_maison_entry.insert(0, values[1])
	nb_chambres_entry.insert(0, values[3])
	nb_personnes_max_entry.insert(0, values[4])
	nom_ile_entry.insert(0, values[5])

# Update record
def update_record():
	# Grab the record number
	selected = my_tree.focus()
	# Update record
	my_tree.item(selected, text="", values=(nom_maison_entry.get(), loyer_maison_entry.get(), id_entry.get(), nb_personnes_max_entry.get(), nom_ile_entry.get(),))

	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("""UPDATE maison SET
		nom_maison = :nom_maison,
		Loyer = :loyer,
		nb_chambres = :nb_chambres,
		nb_personnes_max = :nb_personnes_max,
		nom_ile = :nom_ile,

		WHERE oid = :oid""",
		{
			'nom_maison': nom_maison_entry.get(),
			'loyer': loyer_maison_entry.get(),
            'nb_chambres': nb_chambres_entry.get(),
			'nb_personnes_max': nb_personnes_max_entry.get(),
			'nom_ile': nom_ile_entry.get(),
			'oid': id_entry.get(),
		})
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()


	# Clear entry boxes
	nom_maison_entry.delete(0, END)
	loyer_maison_entry.delete(0, END)
	id_entry.delete(0, END)
	nb_personnes_max_entry.delete(0, END)
	nom_ile_entry.delete(0, END)

# add new record to database
def add_record():
	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	# Add New Record
	c.execute("INSERT INTO maison VALUES (:nom_maison, :loyer, :nb_chambres, :nb_personnes_max, :nom_ile)",
		{
			'nom_maison': nom_maison_entry.get(),
			'loyer': loyer_maison_entry.get(),
			'nb_chambres' : nb_chambres_entry.get(),
			'nb_personnes_max': nb_personnes_max_entry.get(),
			'nom_ile': nom_ile_entry.get(),
		})
	

	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear entry boxes
	nom_maison_entry.delete(0, END)
	loyer_maison_entry.delete(0, END)
	id_entry.delete(0, END)
	nb_personnes_max_entry.delete(0, END)
	nom_ile_entry.delete(0, END)
	nb_chambres_entry.delete(0,END)

	# Clear The Treeview Table
	my_tree.delete(*my_tree.get_children())

	# Run to pull data from database on start
	query_database()

def create_table_again():
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	# Create Table
	
	c.execute("""CREATE TABLE if not exists maison (
		nom_maison text,
		loyer DECIMAL(15,2),
		nb_chambres integer
		nb_personnes_max integer,
		nom_ile text,
		CONSTRAINT loyer_min CHECK(loyer>=100)
		""")
	
	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

# Add Buttons
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text="Update Record", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

remove_many_button = Button(button_frame, text="Remove Many Selected", command=remove_many)
remove_many_button.grid(row=0, column=4, padx=10, pady=10)

move_up_button = Button(button_frame, text="Move Up", command=up)
move_up_button.grid(row=0, column=5, padx=10, pady=10)

move_down_button = Button(button_frame, text="Move Down", command=down)
move_down_button.grid(row=0, column=6, padx=10, pady=10)

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run to pull data from database on start
query_database()

root.mainloop()
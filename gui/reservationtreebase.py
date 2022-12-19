from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('Codemy.com - TreeBase')
#root.iconbitmap('c:/gui/codemy.ico')
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

	c.execute("SELECT rowid, * FROM reservations")
	records = c.fetchall()
	
	# Add our data to the screen
	global count
	count = 0
	
	#for record in records:
	#	print(record)


	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4],), tags=('oddrow',))
		# increment counter
		count += 1


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()



def search_records():
	lookup_record = search_entry_client.get()
	# close the search box
	search.destroy()
	
	# Clear the Treeview
	for record in my_tree.get_children():
		my_tree.delete(record)
	
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("SELECT rowid, * FROM reservations WHERE id_client = :id_client",
           {
               'id_client' : search_entry_client.get
    })
	records=c.fetchall()
    

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



def lookup_records():
	global search_entry_client, search

	search = Toplevel(root)
	search.title("Lookup Records")
	search.geometry("400x200")
	#search.iconbitmap('c:/gui/codemy.ico')

	# Create label frame
	search_frame_client = LabelFrame(search, text="id_client")
	search_frame_client.pack(padx=10, pady=10)

	# Add entry box
	search_entry_client = Entry(search_frame_client, font=("Helvetica", 18))
	search_entry_client.pack(pady=20, padx=20)

	# Add button
	search_button_client = Button(search, text="Search Records", command=search_records)
	search_button_client.pack(padx=20, pady=20)
    
  

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

#enabling the use of foreign keys 
conn.execute("PRAGMA foreign_keys = 1")
# Create Table

c.execute("""CREATE TABLE IF NOT EXISTS reservations(
	id_maison integer,
	id_client integer,
	id integer,
	num_sem integer,
    Constraint ck_numsemaine CHECK(num_sem>9 and num_sem<41),
    PRIMARY KEY(ID_maison, ID_client),
	FOREIGN KEY(id_maison) REFERENCES MAISON(oid),
    FOREIGN KEY(id_client) REFERENCES CLIENTS(oid))
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
my_tree['columns'] = ("id_maison", "id_client", "ID", "num_sem")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("id_maison", anchor=W, width=200)
my_tree.column("id_client", anchor=W, width=200)
my_tree.column("ID", anchor=CENTER, width=100)
my_tree.column("num_sem", anchor=CENTER, width=430)


# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("id_maison", text="id_maison", anchor=W)
my_tree.heading("id_client", text="id_client", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("num_sem", text="num_sem", anchor=CENTER)


# Create Striped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)



# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

id_maison_label = Label(data_frame, text="id_maison")
id_maison_label.grid(row=0, column=0, padx=10, pady=10)
id_maison_entry = Entry(data_frame)
id_maison_entry.grid(row=0, column=1, padx=10, pady=10)

id_client_label = Label(data_frame, text="id_client")
id_client_label.grid(row=0, column=2, padx=10, pady=10)
id_client_entry = Entry(data_frame)
id_client_entry.grid(row=0, column=3, padx=10, pady=10)

id_entry = Entry(data_frame)

num_sem_label = Label(data_frame, text="num_sem")
num_sem_label.grid(row=1, column=0, padx=10, pady=10)
num_sem_entry = Entry(data_frame)
num_sem_entry.grid(row=1, column=1, padx=10, pady=10)


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
	c.execute("DELETE from reservations WHERE oid=" + id_entry.get())
	


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
		c.executemany("DELETE FROM reservations WHERE id = ?", [(a,) for a in ids_to_delete])

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
		c.execute("DROP TABLE reservations")
			


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
	id_maison_entry.delete(0, END)
	id_client_entry.delete(0, END)
	id_entry.delete(0, END)
	num_sem_entry.delete(0, END)


# Select Record
def select_record(e):
	# Clear entry boxes
	id_maison_entry.delete(0, END)
	id_client_entry.delete(0, END)
	id_entry.delete(0, END)
	num_sem_entry.delete(0, END)

	# Grab record Number
	selected = my_tree.focus()
	# Grab record values
	values = my_tree.item(selected, 'values')

	# outpus to entry boxes
	id_maison_entry.insert(0, values[0])
	id_client_entry.insert(0, values[1])
	id_entry.insert(0, values[2])
	num_sem_entry.insert(0, values[3])

# Update record
def update_record():
	# Grab the record number
	selected = my_tree.focus()
	# Update record
	my_tree.item(selected, text="", values=(id_maison_entry.get(), id_client_entry.get(), id_entry.get(), num_sem_entry.get(),))

	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("""UPDATE reservations SET
		id_maison = :id_maison,
		id_client = :id_client,
		num_sem = :num_sem
		
		WHERE oid= :oid""",
		{
			'id_maison': id_maison_entry.get(),
			'id_client': id_client_entry.get(),
			'num_sem': num_sem_entry.get(),
            'oid' : id_entry.get(),
		})
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()


	# Clear entry boxes
	id_maison_entry.delete(0, END)
	id_client_entry.delete(0, END)
	id_entry.delete(0, END)
	num_sem_entry.delete(0, END)

# add new record to database
def add_record():
	# Update the database
	# Create a database or connect to one that exists
    if int(num_sem_entry.get())>40 or int(num_sem_entry.get())<10 :
        response = messagebox.askyesno("Impossible to add this record","Please choose a <<numero semaine>> between 10 and 40")
        return
    conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
    c = conn.cursor()

	# Add New Record
    c.execute("INSERT INTO reservations VALUES (:id_maison, :id_client, :id, :num_sem)",
		{
			'id_maison': id_maison_entry.get(),
			'id_client': id_client_entry.get(),
			'id': id_entry.get(),
			'num_sem': num_sem_entry.get(),
		})
	

	# Commit changes
    conn.commit()

	# Close our connection
    conn.close()

	# Clear entry boxes
    id_maison_entry.delete(0, END) 
    id_client_entry.delete(0, END) 
    id_entry.delete(0, END) 
    num_sem_entry.delete(0, END)

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
	c.execute("""CREATE TABLE if not exists reservations (
		id_maison integer,
		id_client integer,
		id integer,
		num_sem integer,
        Constraint ck_numsemaine CHECK(num_sem>9 and num_sem<41))
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
import tkinter as tk
from tkinter import ttk
import media_tables
import sqlite3

class GUI(tk.Tk):
    def __init__(self, title="Media Library", w=700, h=500, database_path="media.db"):
        super().__init__()
        self.title(title)
        self.geometry(f"{w}x{h}")
        self.w = w
        self.h = h
        self.__database_path = database_path
        self.__connect_to_database(self.__database_path)
        self.__initialise_widgets()

    def __initialise_widgets(self):
        style = ttk.Style()
        style.theme_use("default")
        # Table colour
        style.configure("Treeview", 
            background="#D3D3D3", 
            foreground="black", 
            rowheight=25, 
            fieldbackground="lightgrey"
            )
        # Selected row colour
        style.map("Treeview", 
            background=[("selected", "blue")])
        
        window = ttk.Notebook(self)
        window.pack(fill="both", expand=1)

        movies_frame = tk.Frame(window, width=self.w, height=self.h)
        games_frame = tk.Frame(window, width=self.w, height=self.h)
        music_frame = tk.Frame(window, width=self.w, height=self.h)

        movies_frame.pack(fill="both", expand=1)
        games_frame.pack(fill="both", expand=1)
        music_frame.pack(fill="both", expand=1)

        window.add(movies_frame, text="Movies")
        window.add(games_frame, text="Games")
        window.add(music_frame, text="Music")

        self.movies_tab = MoviesTab(movies_frame, self.__db_connection, self.__db_cursor)
        self.games_tab = GamesTab(games_frame, self.__db_connection, self.__db_cursor)
        self.music_tab = MusicTab(music_frame, self.__db_connection, self.__db_cursor)
    
    def __connect_to_database(self, database_path):
        # persistent storage DB
        self.__db_connection = sqlite3.connect(database_path)
        # create cursor
        self.__db_cursor = self.__db_connection.cursor()
        print(f"Connected to {database_path}")
    
    def __close_database_connection(self):
        self.__db_connection.close()


class MediaTab:
    def __init__(self, master):
        self.master = master

        # Dropdown for selecting category
        self.dropdown_frame = tk.Frame(self.master)
        self.dropdown_frame.pack(fill="both", expand=1)
        self.dropdown_label = tk.Label(self.dropdown_frame, text="Category")
        self.dropdown_label.grid(row=0, column=0, sticky="NESW")
        self.dropdown_menu = ttk.Combobox(self.dropdown_frame, state="readonly", values=["All"])
        self.dropdown_menu.grid(row=0, column=1)
        self.dropdown_menu.set("All")
        
        # Frame for table
        self.table_frame = tk.Frame(self.master)
        # self.table_frame.pack(pady=20)
        self.table_frame.pack(fill="both", expand=1)

        # Define scrollbar for table
        self.table_scroll = tk.Scrollbar(self.table_frame)
        self.table_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Table is a Treeview object
        self.table = ttk.Treeview(self.table_frame, yscrollcommand=self.table_scroll.set, selectmode="extended")
        self.table.pack(pady=50)

        # Attach scrollbar
        self.table_scroll.config(command=self.table.yview)

        self.buttons_frame = tk.LabelFrame(self.master, text="Options")
        self.buttons_frame.pack(fill="x", expand="yes", padx=20)


class MoviesTab(MediaTab):
    def __init__(self, master, db_connection, db_cursor):
        super().__init__(master)
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor

        self.media_tables = media_tables.MoviesTable(self.__db_connection, self.__db_cursor)

        # Columns
        self.table["columns"] = ("ID", "Title", "Director", "Year")
        self.table.column("#0", width=0, stretch=tk.NO) # Disable column 0
        self.table.column("ID", anchor=tk.W, width=140)
        self.table.column("Title", anchor=tk.W, width=140)
        self.table.column("Director", anchor=tk.W, width=140)
        self.table.column("Year", anchor=tk.W, width=140)

        self.table.heading("#0", text="")
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
        self.table.heading("Title", text="Title", anchor=tk.CENTER)
        self.table.heading("Director", text="Director", anchor=tk.CENTER)
        self.table.heading("Year", text="Year", anchor=tk.CENTER)

class GamesTab(MediaTab):
    def __init__(self, master, db_connection, db_cursor):
        super().__init__(master)
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor

        self.media_tables = media_tables.GamesTable(self.__db_connection, self.__db_cursor)

        # Columns
        self.table["columns"] = ("ID", "Name", "Platform", "Developer")
        self.table.column("#0", width=0, stretch=tk.NO) # Disable column 0
        self.table.column("ID", anchor=tk.W, width=140)
        self.table.column("Name", anchor=tk.W, width=140)
        self.table.column("Platform", anchor=tk.W, width=140)
        self.table.column("Developer", anchor=tk.W, width=140)

        self.table.heading("#0", text="")
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
        self.table.heading("Name", text="Name", anchor=tk.CENTER)
        self.table.heading("Platform", text="Platform", anchor=tk.CENTER)
        self.table.heading("Developer", text="Developer", anchor=tk.CENTER)


class MusicTab(MediaTab):
    def __init__(self, master, db_connection, db_cursor):
        super().__init__(master)
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor

        self.media_tables = media_tables.MusicTable(self.__db_connection, self.__db_cursor)

        # Columns
        self.table["columns"] = ("ID", "Song", "Album", "Artist")
        self.table.column("#0", width=0, stretch=tk.NO) # Disable column 0
        self.table.column("ID", anchor=tk.W, width=140)
        self.table.column("Song", anchor=tk.W, width=140)
        self.table.column("Album", anchor=tk.W, width=140)
        self.table.column("Artist", anchor=tk.W, width=140)

        self.table.heading("#0", text="")
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
        self.table.heading("Song", text="Song", anchor=tk.CENTER)
        self.table.heading("Album", text="Album", anchor=tk.CENTER)
        self.table.heading("Artist", text="Artist", anchor=tk.CENTER)

        self.add_button = tk.Button(self.buttons_frame, text="Add Item", command=self.add_item_popup)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.edit_button = tk.Button(self.buttons_frame, text="Edit Item", command=self.edit_item_popup)
        self.edit_button.grid(row=0, column=1, padx=10, pady=10)
        self.edit_button["state"] = "disabled"

        self.delete_button = tk.Button(self.buttons_frame, text="Delete Item", command=self.delete_item)
        self.delete_button.grid(row=0, column=2, padx=10, pady=10)
        self.delete_button["state"] = "disabled"

        self.new_cat_button = tk.Button(self.buttons_frame, text="Create New Category", command=self.create_new_category_popup)
        self.new_cat_button.grid(row=0, column=3, padx=10, pady=10)

        self.move_cat_button = tk.Button(self.buttons_frame, text="Move Item to Category")
        self.move_cat_button.grid(row=0, column=5, padx=10, pady=10)

        self.table.bind("<ButtonRelease-1>", lambda x : self.enable_buttons(""))
        self.dropdown_menu.bind("<<ComboboxSelected>>", lambda x : self.change_category(""))
        self.display_category = 0 # Initial dropdown key to display

        self.update_table()
        self.media_tables.add_to_category(1, "Favourites")
        self.media_tables.add_to_category(2, "Favourites")
        self.media_tables.add_to_category(4, "Favourites")
        categories = self.get_categories()
        print(categories)
    
    def enable_buttons(self, event):
        self.edit_button["state"] = "normal"
        self.delete_button["state"] = "normal"
    
    def disable_buttons(self):
        self.edit_button["state"] = "disabled"
        self.delete_button["state"] = "disabled"
    
    def add_item_popup(self):
        self.add_window = tk.Tk()
        self.add_window.title("Add item")
        self.add_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Song")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.__entry1 = tk.Entry(text_field_frame, width=30)
        self.__entry1.grid(row=0, column=1)

        label2 = tk.Label(text_field_frame, text="Album")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.__entry2 = tk.Entry(text_field_frame, width=30)
        self.__entry2.grid(row=1, column=1)

        label3 = tk.Label(text_field_frame, text="Artist")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.__entry3 = tk.Entry(text_field_frame, width=30)
        self.__entry3.grid(row=2, column=1)

        # Buttons
        button_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button_popup = tk.Button(button_frame, text="Add", command=self.add_item)
        add_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.add_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)

    def add_item(self):
        record = [self.__entry1.get(), self.__entry2.get(), self.__entry3.get()]
        self.media_tables.add_record(record)
        self.add_window.destroy()
        self.update_table()
        self.disable_buttons()
    
    def delete_item(self):
        selected_item = self.table.focus()
        if selected_item == '':
            return # TODO disable button for this scenario
        else:
            print("Deleting")
        values = self.table.item(selected_item, 'values')
        record_id = int(values[0])
        self.media_tables.delete_record(record_id)
        self.update_table()
        self.disable_buttons()

    def edit_item_popup(self):
        selected_item = self.table.focus()
        if selected_item == '':
            return # TODO disable button for this scenario
        else:
            print("Editing")
        values = self.table.item(selected_item, 'values')
        
        self.edit_window = tk.Tk()
        self.edit_window.title("Add item")
        self.edit_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Song")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.__entry1 = tk.Entry(text_field_frame, width=30)
        self.__entry1.grid(row=0, column=1)
        self.__entry1.insert(0, values[1])

        label2 = tk.Label(text_field_frame, text="Album")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.__entry2 = tk.Entry(text_field_frame, width=30)
        self.__entry2.grid(row=1, column=1)
        self.__entry2.insert(0, values[2])

        label3 = tk.Label(text_field_frame, text="Artist")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.__entry3 = tk.Entry(text_field_frame, width=30)
        self.__entry3.grid(row=2, column=1)
        self.__entry3.insert(0, values[3])

        # Buttons
        button_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        edit_button_popup = tk.Button(button_frame, text="Done", command=lambda : self.edit_item(values[0]))
        edit_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.edit_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
        
    def edit_item(self, record_id):
        record = [self.__entry1.get(), self.__entry2.get(), self.__entry3.get()]
        self.media_tables.edit_record(record_id, song=record[0], album=record[1], artist=record[2])
        self.edit_window.destroy()
        self.update_table()
        self.disable_buttons()

    def update_table(self):
        tables = self.media_tables.get_all_records()

        for item in self.table.get_children():
            self.table.delete(item)

        self.table.tag_configure("oddrow", background="white")
        self.table.tag_configure("evenrow", background="lightblue")
        category = list(tables.keys())[self.display_category]
        table_data = tables[category]
        count = 0
        for record in table_data:
            if count % 2 == 0:
                self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("evenrow",))
            else:
                self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("oddrow",))
            count += 1

    def get_categories(self):
        tables = self.media_tables.get_all_records()
        category_names = list(tables.keys())[1:]
        return category_names
    
    def change_category(self, event):
        print(self.dropdown_menu.current())
        self.display_category = self.dropdown_menu.current()
        self.update_table()
        self.disable_buttons()
    
    def update_dropdown_categories(self):
        categories = self.get_categories()
        categories = ["All"] + [x[len("music_table")+1:] for x in categories[1:]]
        self.dropdown_menu["values"] = tuple(categories)
    
    def create_new_category_popup(self):
        self.create_cat_window = tk.Tk()
        self.create_cat_window.title("Create New Category")
        self.create_cat_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.create_cat_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Category Name")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.__entry1 = tk.Entry(text_field_frame, width=30)
        self.__entry1.grid(row=0, column=1)
        self.__entry1.grid(row=0, column=1)

        # Buttons
        button_frame = tk.LabelFrame(self.create_cat_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        confirm_button_popup = tk.Button(button_frame, text="Confirm", command=lambda : self.create_new_category())
        confirm_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.create_cat_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
    
    def create_new_category(self):
        category_name = self.__entry1.get()
        self.media_tables.add_new_category(category_name)
        self.create_cat_window.destroy()
        self.update_dropdown_categories()
    
    # def fill_tables_test(self):
    #     tables = self.media_tables.get_all_records()
    #     for table in tables:
    #         print(table)
    #         for record in tables[table]:
    #             print("\t", record)
    #     print()

    #     self.table.tag_configure("oddrow", background="white")
    #     self.table.tag_configure("evenrow", background="lightblue")
        
    #     table_data = tables["music_table"]
    #     count = 0
    #     for record in table_data:
    #         if count % 2 == 0:
    #             self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("evenrow",))
    #         else:
    #             self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("oddrow",))
    #         count += 1

        # self.edits_frame = tk.LabelFrame(master, text="Edit")
        # self.edits_frame.pack(fill="x", expand="yes", padx=20)

        # self.title_label = tk.Label(self.edits_frame, text="Title")
        # self.title_label.grid(row=0, column=0, padx=10, pady=10)
        # self.title_entry = tk.Entry(self.edits_frame)
        # self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        # self.album_label = tk.Label(self.edits_frame, text="Album")
        # self.album_label.grid(row=0, column=2, padx=10, pady=10)
        # self.album_entry = tk.Entry(self.edits_frame)
        # self.album_entry.grid(row=0, column=3, padx=10, pady=10)

        # self.artist_label = tk.Label(self.edits_frame, text="Artist")
        # self.artist_label.grid(row=0, column=4, padx=10, pady=10)
        # self.artist_entry = tk.Entry(self.edits_frame)
        # self.artist_entry.grid(row=0, column=5, padx=10, pady=10)


        # self.buttons_frame = tk.LabelFrame(master, text="Options")
        # self.buttons_frame.pack(fill="x", expand="yes", padx=20)

        # self.add_button = tk.Button(self.buttons_frame, text="Add Record")
        # self.add_button.grid(row=0, column=0, padx=10, pady=10)

        # self.edit_button = tk.Button(self.buttons_frame, text="Edit Record", command=lambda x: self.select_record(""))
        # self.edit_button.grid(row=0, column=1, padx=10, pady=10)

        # self.delete_button = tk.Button(self.buttons_frame, text="Delete Record")
        # self.delete_button.grid(row=0, column=2, padx=10, pady=10)

        # self.table.bind("<ButtonRelease-1>", self.select_record)

    # def select_record(self, event):
    #     self.title_entry.delete(0, tk.END)
    #     self.album_entry.delete(0, tk.END)
    #     self.artist_entry.delete(0, tk.END)

    #     # Get data from selected row
    #     selected = self.table.focus()
    #     values = self.table.item(selected, 'values')

    #     self.title_entry.insert(0,values[1])
    #     self.album_entry.insert(0,values[2])
    #     self.artist_entry.insert(0,values[3])

def initialise_database_for_testing(database_path):
    # persistent storage DB
    db_connection = sqlite3.connect(database_path)

    # create cursor
    db_cursor = db_connection.cursor()

    # Create tables
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS movies_table (
                        title text,
                        director text,
                        year integer
                    )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS games_table (
                        name text,
                        platform text,
                        developer text
                    )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS music_table (
                        song text,
                        album text,
                        artist text
                    )""")

    # db_cursor.execute("INSERT INTO movies_table VALUES ('The Shawshank Redemption', 'Frank Darabont', 1994)")
    entries = [
        ('The Shawshank Redemption', 'Frank Darabont', 1994),
        ('The Godfather', 'Francis Ford Coppola', 1972),
        ('The Dark Knight', 'Christopher Nolan', 2008),
        ('The Godfather Part II', 'Francis Ford Coppola', 1974),
        ('12 Angry Men', 'Sidney Lumet', 1957),
        ('Schindler''s List', 'Steven Spielberg', 1993),
    ]
    db_cursor.executemany("INSERT INTO movies_table VALUES (?, ?, ?)", entries)

    entries = [
        ('Red Dead Redemption 2', 'Rockstar Games', 'PlayStation 4'),
        ('The Last of Us', 'Sony Computer Entertainment', 'PlayStation 3'),
        ('Portal 2', 'Valve', 'PC'),
        ('Minecraft', 'Mojang', 'PC'),
        ('Super Mario Galaxy', 'Nintendo', 'Wii'),
    ]
    db_cursor.executemany("INSERT INTO games_table VALUES (?, ?, ?)", entries)

    entries = [
        ('Smells Like Teen Spirit', 'Nevermind', 'Nirvana'),
        ('Wake Up', 'Funeral', 'Arcade Fire'),
        ('Digital Love', 'Discovery', 'Daft Punk'),
        ('Hard to Explain', 'Is This It', 'The Strokes'),
        ('Jacksonville', 'Illinois', 'Sufjan Stevens'),
    ]
    db_cursor.executemany("INSERT INTO music_table VALUES (?, ?, ?)", entries)

    # Commit command
    db_connection.commit()

    # Close connection
    db_connection.close()

if __name__ == "__main__":
    # initialise_database_for_testing("media.db")
    gui = GUI(database_path="media.db")
    gui.mainloop()

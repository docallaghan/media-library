import tkinter as tk
from tkinter import ttk
import media_tables
import sqlite3

class GUI(tk.Tk):
    """Main class for media library GUI"""
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
        
        # Create tabs for each media type
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

        self.movies_tab = MoviesTab(movies_frame, self.__db_connection, self.__db_cursor, main_table_name="movies_table", 
            column_dict={"title": "text", "director": "text", "year": "integer"})
        self.games_tab = GamesTab(games_frame, self.__db_connection, self.__db_cursor, main_table_name="games_table", 
            column_dict={"name": "text", "platform": "text", "developer": "text"})
        self.music_tab = MusicTab(music_frame, self.__db_connection, self.__db_cursor, main_table_name="music_table", 
            column_dict={"song": "text", "album": "text", "artist": "text"})

        # Define action to perform after quitting
        self.protocol("WM_DELETE_WINDOW", self.__on_close)
    
    def __connect_to_database(self, database_path):
        # persistent storage DB
        self.__db_connection = sqlite3.connect(database_path)
        # create cursor
        self.__db_cursor = self.__db_connection.cursor()
    
    def __close_database_connection(self):
        self.__db_connection.close()
    
    def __on_close(self):
        """Called after exiting window"""
        self.__close_database_connection()
        self.destroy()


class MediaTab:
    """Parent class for tabs in GUI for each type of media"""
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


class MusicTab(MediaTab):
    """Class for music media displayed in tab in the GUI"""
    def __init__(self, master, db_connection, db_cursor, main_table_name, column_dict):
        super().__init__(master)
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.main_table_name = main_table_name

        # Link database handling classes
        self.media_tables = media_tables.MediaTable(self.__db_connection, self.__db_cursor, main_table_name, column_dict)

        # Columns
        self.table["columns"] = ("ID", "Song", "Album", "Artist")
        self.table.column("#0", width=0, stretch=tk.NO) # Disable column 0
        self.table.column("ID", anchor=tk.W, width=65)
        self.table.column("Song", anchor=tk.W, width=165)
        self.table.column("Album", anchor=tk.W, width=165)
        self.table.column("Artist", anchor=tk.W, width=165)

        self.table.heading("#0", text="")
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
        self.table.heading("Song", text="Song", anchor=tk.CENTER)
        self.table.heading("Album", text="Album", anchor=tk.CENTER)
        self.table.heading("Artist", text="Artist", anchor=tk.CENTER)

        # Buttons
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

        self.add_to_cat_button = tk.Button(self.buttons_frame, text="Add Item to Category", command=self.add_to_category_popup)
        self.add_to_cat_button.grid(row=0, column=5, padx=10, pady=10)
        self.add_to_cat_button["state"] = "disabled"

        # Bindings for selecting table rows or dropdown items
        self.table.bind("<ButtonRelease-1>", lambda x : self.enable_buttons(""))
        self.dropdown_menu.bind("<<ComboboxSelected>>", lambda x : self.change_category(""))

        self.display_category = 0 # Initial dropdown key to display 0 = "All"
        
        # Populate table and dropdown
        self.update_table()
        self.update_dropdown_categories()
    
    def enable_buttons(self, event):
        """Enable 3 buttons that sometimes require state change"""
        self.edit_button["state"] = "normal"
        self.delete_button["state"] = "normal"
        self.add_to_cat_button["state"] = "normal"
    
    def disable_buttons(self):
        """Disable 3 buttons that sometimes require state change"""
        self.edit_button["state"] = "disabled"
        self.delete_button["state"] = "disabled"
        self.add_to_cat_button["state"] = "disabled"
    
    def add_item_popup(self):
        """Popup window for adding new media items"""
        self.add_window = tk.Tk()
        self.add_window.title("Add item")
        self.add_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Song")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1 = tk.Entry(text_field_frame, width=30)
        self.entry1.grid(row=0, column=1)

        label2 = tk.Label(text_field_frame, text="Album")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.entry2 = tk.Entry(text_field_frame, width=30)
        self.entry2.grid(row=1, column=1)

        label3 = tk.Label(text_field_frame, text="Artist")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.entry3 = tk.Entry(text_field_frame, width=30)
        self.entry3.grid(row=2, column=1)

        # Buttons
        button_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button_popup = tk.Button(button_frame, text="Add", command=self.add_item)
        add_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.add_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)

    def add_item(self):
        """Command exectured after confirming details when adding items"""
        record = [self.entry1.get(), self.entry2.get(), self.entry3.get()]
        self.media_tables.add_record(record)
        self.add_window.destroy()
        self.update_table()
        self.disable_buttons()
    
    def delete_item(self):
        """Retrieve focus from table and delete selected item"""
        selected_item = self.table.focus()
        if selected_item == '':
            return
        
        values = self.table.item(selected_item, 'values')
        record_id = int(values[0])
        self.media_tables.delete_record(record_id)
        self.update_table()
        self.disable_buttons()

    def edit_item_popup(self):
        """Popup window for editing items"""
        selected_item = self.table.focus()
        if selected_item == '':
            return # TODO disable button for this scenario
        
        values = self.table.item(selected_item, 'values')
        
        self.edit_window = tk.Tk()
        self.edit_window.title("Add item")
        self.edit_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Song")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1 = tk.Entry(text_field_frame, width=30)
        self.entry1.grid(row=0, column=1)
        self.entry1.insert(0, values[1])

        label2 = tk.Label(text_field_frame, text="Album")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.entry2 = tk.Entry(text_field_frame, width=30)
        self.entry2.grid(row=1, column=1)
        self.entry2.insert(0, values[2])

        label3 = tk.Label(text_field_frame, text="Artist")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.entry3 = tk.Entry(text_field_frame, width=30)
        self.entry3.grid(row=2, column=1)
        self.entry3.insert(0, values[3])

        # Buttons
        button_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        edit_button_popup = tk.Button(button_frame, text="Done", command=lambda : self.edit_item(values[0]))
        edit_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.edit_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
        
    def edit_item(self, record_id):
        """Command exectured after confirming details when editing items"""
        record = [self.entry1.get(), self.entry2.get(), self.entry3.get()]
        self.media_tables.edit_record(record_id, song=record[0], album=record[1], artist=record[2])
        self.edit_window.destroy()
        self.update_table()
        self.disable_buttons()

    def update_table(self):
        """Called whenever the treeview table needs to be refreshed"""
        tables = self.media_tables.get_all_records()

        for item in self.table.get_children():
            self.table.delete(item)

        self.table.tag_configure("oddrow", background="white")
        self.table.tag_configure("evenrow", background="lightblue")
        category = list(tables.keys())[self.display_category]
        table_data = tables[category]
        
        count = 0
        for record in table_data:
            if category != self.main_table_name:
                record = tuple(list(record[1:]))
            if count % 2 == 0:
                self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("evenrow",))
            else:
                self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("oddrow",))
            count += 1

    def get_categories(self):
        """Helper function to get the names of categories from database"""
        tables = self.media_tables.get_all_records()
        category_names = list(tables.keys())[1:]
        return category_names
    
    def change_category(self, event):
        """Changes table being displayed based on category dropdown menu"""
        self.display_category = self.dropdown_menu.current()
        self.update_table()
        self.disable_buttons()
    
    def update_dropdown_categories(self):
        """Called whenever the categories in the dropdown menu need to be refreshed"""
        categories = self.get_categories()
        categories = ["All"] + [x[len(self.main_table_name)+1:] for x in categories]
        self.dropdown_menu["values"] = tuple(categories)
    
    def create_new_category_popup(self):
        """Popup window for adding a new category"""
        self.create_cat_window = tk.Tk()
        self.create_cat_window.title("Create New Category")
        self.create_cat_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.create_cat_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Category Name")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1 = tk.Entry(text_field_frame, width=30)
        self.entry1.grid(row=0, column=1)

        # Buttons
        button_frame = tk.LabelFrame(self.create_cat_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        confirm_button_popup = tk.Button(button_frame, text="Confirm", command=lambda : self.create_new_category())
        confirm_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.create_cat_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
    
    def create_new_category(self):
        """Command exectured after confirming details when creating a category"""
        category_name = self.entry1.get()
        self.media_tables.add_new_category(category_name)
        self.create_cat_window.destroy()
        self.update_dropdown_categories()

    def add_to_category_popup(self):
        """Popup window for adding item to a category"""
        self.add_to_cat_window = tk.Tk()
        self.add_to_cat_window.title("Add to Category")
        self.add_to_cat_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.add_to_cat_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Category Name")
        label1.grid(row=0, column=0, padx=10, pady=5)

        categories = self.get_categories()
        categories = [x[len(self.main_table_name)+1:] for x in categories]
        self.popup_dropdown_menu = ttk.Combobox(text_field_frame, state="readonly", values=categories)
        self.popup_dropdown_menu.grid(row=0, column=1)

        # Buttons
        button_frame = tk.LabelFrame(self.add_to_cat_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        confirm_button_popup = tk.Button(button_frame, text="Confirm", command=lambda : self.add_to_category())
        confirm_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.add_to_cat_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
    
    def add_to_category(self):
        """Command exectured after confirming details adding item to a category"""
        selected_item = self.table.focus()
        if selected_item == '':
            return
        
        values = self.table.item(selected_item, 'values')
        record_id = int(values[0])

        categories = self.get_categories()
        category_id = self.popup_dropdown_menu.current()
        category = categories[category_id][len(self.main_table_name)+1:]
        self.media_tables.add_to_category(record_id, category)
        self.add_to_cat_window.destroy()
        self.update_table()
        self.disable_buttons()


class MoviesTab(MusicTab):
    """Class for movies media displayed in tab in the GUI. A lot of the behabiour
    is identical to the MusicTab class so this class inherits from it."""
    def __init__(self, master, db_connection, db_cursor, main_table_name, column_dict):
        super().__init__(master, db_connection, db_cursor, main_table_name, column_dict)
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.main_table_name = main_table_name

        # Link database handling classes
        self.media_tables = media_tables.MediaTable(self.__db_connection, self.__db_cursor, main_table_name, column_dict)

        # Columns
        self.table["columns"] = ("ID", "Title", "Director", "Year")
        self.table.column("#0", width=0, stretch=tk.NO) # Disable column 0
        self.table.column("ID", anchor=tk.W, width=65)
        self.table.column("Title", anchor=tk.W, width=165)
        self.table.column("Director", anchor=tk.W, width=165)
        self.table.column("Year", anchor=tk.W, width=165)

        self.table.heading("#0", text="")
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
        self.table.heading("Title", text="Title", anchor=tk.CENTER)
        self.table.heading("Director", text="Director", anchor=tk.CENTER)
        self.table.heading("Year", text="Year", anchor=tk.CENTER)

        # Buttons
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

        self.add_to_cat_button = tk.Button(self.buttons_frame, text="Add Item to Category", command=self.add_to_category_popup)
        self.add_to_cat_button.grid(row=0, column=5, padx=10, pady=10)
        self.add_to_cat_button["state"] = "disabled"

        # Bindings for selecting table rows or dropdown items
        self.table.bind("<ButtonRelease-1>", lambda x : self.enable_buttons(""))
        self.dropdown_menu.bind("<<ComboboxSelected>>", lambda x : self.change_category(""))
        
        self.display_category = 0 # Initial dropdown key to display 0 = "All"
        
        # Populate table and dropdown
        self.update_table()
        self.update_dropdown_categories()
    
    def add_item_popup(self):
        """Popup window for adding new media items"""
        self.add_window = tk.Tk()
        self.add_window.title("Add item")
        self.add_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Title")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1 = tk.Entry(text_field_frame, width=30)
        self.entry1.grid(row=0, column=1)

        label2 = tk.Label(text_field_frame, text="Director")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.entry2 = tk.Entry(text_field_frame, width=30)
        self.entry2.grid(row=1, column=1)

        label3 = tk.Label(text_field_frame, text="Year")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.entry3 = tk.Entry(text_field_frame, width=30)
        self.entry3.grid(row=2, column=1)

        # Buttons
        button_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button_popup = tk.Button(button_frame, text="Add", command=self.add_item)
        add_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.add_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
    
    def edit_item_popup(self):
        """Popup window for editing items"""
        selected_item = self.table.focus()
        if selected_item == '':
            return
        
        values = self.table.item(selected_item, 'values')
        
        self.edit_window = tk.Tk()
        self.edit_window.title("Add item")
        self.edit_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Title")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1 = tk.Entry(text_field_frame, width=30)
        self.entry1.grid(row=0, column=1)
        self.entry1.insert(0, values[1])

        label2 = tk.Label(text_field_frame, text="Director")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.entry2 = tk.Entry(text_field_frame, width=30)
        self.entry2.grid(row=1, column=1)
        self.entry2.insert(0, values[2])

        label3 = tk.Label(text_field_frame, text="Year")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.entry3 = tk.Entry(text_field_frame, width=30)
        self.entry3.grid(row=2, column=1)
        self.entry3.insert(0, values[3])

        # Buttons
        button_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        edit_button_popup = tk.Button(button_frame, text="Done", command=lambda : self.edit_item(values[0]))
        edit_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.edit_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
    
    def edit_item(self, record_id):
        """Command exectured after confirming details when editing items"""
        record = [self.entry1.get(), self.entry2.get(), self.entry3.get()]
        self.media_tables.edit_record(record_id, title=record[0], director=record[1], year=record[2])
        self.edit_window.destroy()
        self.update_table()
        self.disable_buttons()


class GamesTab(MusicTab):
    """Class for games media displayed in tab in the GUI. A lot of the behabiour
    is identical to the MusicTab class so this class inherits from it."""
    def __init__(self, master, db_connection, db_cursor, main_table_name, column_dict):
        super().__init__(master, db_connection, db_cursor, main_table_name, column_dict)
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.main_table_name = main_table_name

        # Link database handling classes
        self.media_tables = media_tables.MediaTable(self.__db_connection, self.__db_cursor, main_table_name, column_dict)

        # Columns
        self.table["columns"] = ("ID", "Name", "Platform", "Developer")
        self.table.column("#0", width=0, stretch=tk.NO) # Disable column 0
        self.table.column("ID", anchor=tk.W, width=65)
        self.table.column("Name", anchor=tk.W, width=165)
        self.table.column("Platform", anchor=tk.W, width=165)
        self.table.column("Developer", anchor=tk.W, width=165)

        self.table.heading("#0", text="")
        self.table.heading("ID", text="ID", anchor=tk.CENTER)
        self.table.heading("Name", text="Name", anchor=tk.CENTER)
        self.table.heading("Platform", text="Platform", anchor=tk.CENTER)
        self.table.heading("Developer", text="Developer", anchor=tk.CENTER)

        # Buttons
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

        self.add_to_cat_button = tk.Button(self.buttons_frame, text="Add Item to Category", command=self.add_to_category_popup)
        self.add_to_cat_button.grid(row=0, column=5, padx=10, pady=10)
        self.add_to_cat_button["state"] = "disabled"

        # Bindings for selecting table rows or dropdown items
        self.table.bind("<ButtonRelease-1>", lambda x : self.enable_buttons(""))
        self.dropdown_menu.bind("<<ComboboxSelected>>", lambda x : self.change_category(""))
        
        self.display_category = 0 # Initial dropdown key to display 0 = "All"
        
        # Populate table and dropdown
        self.update_table()
        self.update_dropdown_categories()
    
    def edit_item_popup(self):
        """Popup window for editing items"""
        selected_item = self.table.focus()
        if selected_item == '':
            return
        
        values = self.table.item(selected_item, 'values')
        
        self.edit_window = tk.Tk()
        self.edit_window.title("Add item")
        self.edit_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Name")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1 = tk.Entry(text_field_frame, width=30)
        self.entry1.grid(row=0, column=1)
        self.entry1.insert(0, values[1])

        label2 = tk.Label(text_field_frame, text="Platform")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.entry2 = tk.Entry(text_field_frame, width=30)
        self.entry2.grid(row=1, column=1)
        self.entry2.insert(0, values[2])

        label3 = tk.Label(text_field_frame, text="Developer")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.entry3 = tk.Entry(text_field_frame, width=30)
        self.entry3.grid(row=2, column=1)
        self.entry3.insert(0, values[3])

        # Buttons
        button_frame = tk.LabelFrame(self.edit_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        edit_button_popup = tk.Button(button_frame, text="Done", command=lambda : self.edit_item(values[0]))
        edit_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.edit_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
    
    def edit_item(self, record_id):
        """Command exectured after confirming details when editing items"""
        record = [self.entry1.get(), self.entry2.get(), self.entry3.get()]
        self.media_tables.edit_record(record_id, name=record[0], platform=record[1], developer=record[2])
        self.edit_window.destroy()
        self.update_table()
        self.disable_buttons()
    
    def add_item_popup(self):
        """Popup window for adding new media items"""
        self.add_window = tk.Tk()
        self.add_window.title("Add item")
        self.add_window.geometry(f"300x200")

        # Text fields
        text_field_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        text_field_frame.pack(fill="x", expand="yes", padx=20)
        
        label1 = tk.Label(text_field_frame, text="Name")
        label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1 = tk.Entry(text_field_frame, width=30)
        self.entry1.grid(row=0, column=1)

        label2 = tk.Label(text_field_frame, text="Platform")
        label2.grid(row=1, column=0, padx=10, pady=5)
        self.entry2 = tk.Entry(text_field_frame, width=30)
        self.entry2.grid(row=1, column=1)

        label3 = tk.Label(text_field_frame, text="Developer")
        label3.grid(row=2, column=0, padx=10, pady=5)
        self.entry3 = tk.Entry(text_field_frame, width=30)
        self.entry3.grid(row=2, column=1)

        # Buttons
        button_frame = tk.LabelFrame(self.add_window, borderwidth=0, highlightthickness=0)
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button_popup = tk.Button(button_frame, text="Add", command=self.add_item)
        add_button_popup.pack(padx=10, pady=10)

        cancel_button_popup = tk.Button(button_frame, text="Cancel", command=self.add_window.destroy)
        cancel_button_popup.pack(padx=10, pady=10)
    

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

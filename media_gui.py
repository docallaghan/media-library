import tkinter as tk
from tkinter import ttk
import media_tables

class GUI(tk.Tk):
    def __init__(self, title="Media Library", w=800, h=500):
        super().__init__()
        self.title(title)
        self.geometry(f"{w}x{h}")
        self.w = w
        self.h = h
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
        window.pack()

        movies_frame = tk.Frame(window, width=self.w, height=self.h, bg="blue")
        games_frame = tk.Frame(window, width=self.w, height=self.h, bg="red")
        music_frame = tk.Frame(window, width=self.w, height=self.h, bg="green")

        movies_frame.pack(fill="both", expand=1)
        games_frame.pack(fill="both", expand=1)
        music_frame.pack(fill="both", expand=1)

        window.add(movies_frame, text="Movies")
        window.add(games_frame, text="Games")
        window.add(music_frame, text="Music")

        movies_tab = MoviesTab(movies_frame)
        games_tab = GamesTab(games_frame)
        music_tab = MusicTab(music_frame)


class MediaTab:
    def __init__(self, master):
        # Frame for table
        self.table_frame = tk.Frame(master)
        self.table_frame.pack(pady=20)

        # Define scrollbar for table
        self.table_scroll = tk.Scrollbar(self.table_frame)
        self.table_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Table is a Treeview object
        self.table = ttk.Treeview(self.table_frame, yscrollcommand=self.table_scroll.set, selectmode="extended")
        self.table.pack()

        # Attach scrollbar
        self.table_scroll.config(command=self.table.yview)


class MoviesTab(MediaTab):
    def __init__(self, master):
        super().__init__(master)

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
    def __init__(self, master):
        super().__init__(master)

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
    def __init__(self, master):
        super().__init__(master)

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

        # data = [
        #     [0, "The Chain", "Rumours", "Fleetwood Mac"],
        #     [1, 'Wake Up', 'Funeral', 'Arcade Fire'],
        #     [2, 'Digital Love', 'Discovery', 'Daft Punk'],
        # ]

        # self.table.tag_configure("oddrow", background="white")
        # self.table.tag_configure("evenrow", background="lightblue")

        # count = 0
        # for record in data:
        #     if count % 2 == 0:
        #         self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("evenrow",))
        #     else:
        #         self.table.insert(parent="", index="end", iid=count, text="", values=tuple(record), tags=("oddrow",))
        #     count += 1

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

if __name__ == "__main__":
    gui = GUI()
    gui.connect_to_database("media.db")
    gui.mainloop()

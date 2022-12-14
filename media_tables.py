import abc
import sqlite3

class MediaTable(abc.ABC):

    @abc.abstractmethod
    def add_record(self, record):
        """Adds a record to the associated table
        Parameters:
            record (tuple): values of record to add
        """
        pass
    
    @abc.abstractmethod
    def edit_record(self, id, **kwargs):
        """Edits values of a specified record in the table
        Parameters:
            id (int): rowid of the record to be edited
            **kwargs: new key-value pair(s) for the record being edited
        """
        pass
    
    @abc.abstractmethod
    def delete_record(self, id):
        """Deletes a specified record in the table
        Parameters:
            id (int): rowid of the record to be deleted
        """
        pass

    @abc.abstractmethod
    def add_new_category(self, category_name):
        """Adds a new category
        Parameters:
            category_name (str): name of category to add record to
        """
        pass

    @abc.abstractmethod
    def add_to_category(self, id, category_name):
        """Adds a specified record to a category
        Parameters:
            id (int): rowid of the record
            category_name (str): name of category to add record to
        """
        pass
    
    @abc.abstractmethod
    def remove_from_category(self, id, category_name):
        """Adds a specified record to a category
        Parameters:
            id (int): rowid of the record
            category_name (str): name of category to add record to
        """
        pass


class MoviesTable(MediaTable):
    
    def __init__(self, db_connection, db_cursor):
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.__table_name = "movies_table"
        db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.__table_name} (
            title text,
            director text,
            year integer
            )""")
    
    def add_record(self, record):
        self.__db_cursor.execute(f"INSERT INTO {self.__table_name} VALUES (?, ?, ?)", record)
        self.__db_connection.commit()
    
    def edit_record(self, id, **kwargs):
        for key in kwargs:
            self.__db_cursor.execute(f"UPDATE {self.__table_name} SET {key} = '{kwargs[key]}' WHERE rowid = '{id}'")
            self.__db_connection.commit()
        self.__edit_record_in_categories(id, **kwargs)
    
    def __edit_record_in_categories(self, id, **kwargs):
        table_names = self.__get_table_names()
        for table_name in table_names:
            if self.__table_name != table_name:
                for key in kwargs:
                    self.__db_cursor.execute(f"UPDATE {table_name} SET {key} = '{kwargs[key]}' WHERE orig_id = '{id}'")
                    self.__db_connection.commit()

    
    def delete_record(self, id):
        self.__db_cursor.execute(f"DELETE from {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
        self.__delete_record_in_categories(id)
    
    def __delete_record_in_categories(self, id):
        table_names = self.__get_table_names()

        for table_name in table_names:
            if self.__table_name != table_name:
                self.__db_cursor.execute(f"DELETE from {table_name} WHERE orig_id = '{id}'")
                self.__db_connection.commit()
    
    def get_all_records(self):
        tables = {}
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} ORDER BY rowid")
        self.__db_connection.commit()
        fetched_data = self.__db_cursor.fetchall()
        tables[self.__table_name] = fetched_data
        table_names = self.__get_table_names()
        for table_name in table_names:
            if self.__table_name != table_name:
                self.__db_cursor.execute(f"SELECT rowid, * FROM {table_name} ORDER BY rowid")
                self.__db_connection.commit()
                fetched_data = self.__db_cursor.fetchall()
                tables[table_name] = fetched_data
        return tables
    
    def add_new_category(self, category_name):
        # Add category table if it doesn't exist
        table_name = f"{self.__table_name}_{category_name}"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            orig_id int,
            title text,
            director text,
            year integer
            )""")
        self.__db_connection.commit()

    def add_to_category(self, id, category_name):
        # Get record
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
        record = self.__db_cursor.fetchone()
        # Add category table if it doesn't exist
        table_name = f"{self.__table_name}_{category_name}"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            orig_id int,
            title text,
            director text,
            year integer
            )""")
        # Add record to new category (but only if it hasn't already been added)
        self.__db_cursor.execute(f"SELECT rowid, * FROM {table_name} WHERE orig_id = '{id}'")
        self.__db_connection.commit()
        fetched_data = self.__db_cursor.fetchone()
        if fetched_data is None:
            self.__db_cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", record)
            self.__db_connection.commit()
    
    def remove_from_category(self, id, category_name):
        table_name = f"{self.__table_name}_{category_name}"
        # Remove record from category
        self.__db_cursor.execute(f"DELETE from {table_name} WHERE orig_id = '{id}'")
        self.__db_connection.commit()

    def __get_table_names(self):
        self.__db_cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        self.__db_connection.commit()
        data = self.__db_cursor.fetchall()
        table_names = [x[0] for x in data]
        table_names = [x for x in table_names if self.__table_name in x]
        return table_names

    
class GamesTable(MediaTable):
    
    def __init__(self, db_connection, db_cursor):
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.__table_name = "games_table"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.__table_name} (
            name text,
            platform text,
            developer text
            )""")
    
    def add_record(self, record):
        self.__db_cursor.execute(f"INSERT INTO {self.__table_name} VALUES (?, ?, ?)", record)
        self.__db_connection.commit()
    
    def edit_record(self, id, **kwargs):
        for key in kwargs:
            self.__db_cursor.execute(f"UPDATE {self.__table_name} SET {key} = '{kwargs[key]}' WHERE rowid = '{id}'")
            self.__db_connection.commit()
        self.__edit_record_in_categories(id, **kwargs)
    
    def __edit_record_in_categories(self, id, **kwargs):
        table_names = self.__get_table_names()
        for table_name in table_names:
            if self.__table_name != table_name:
                for key in kwargs:
                    self.__db_cursor.execute(f"UPDATE {table_name} SET {key} = '{kwargs[key]}' WHERE orig_id = '{id}'")
                    self.__db_connection.commit()

    
    def delete_record(self, id):
        self.__db_cursor.execute(f"DELETE from {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
        self.__delete_record_in_categories(id)
    
    def __delete_record_in_categories(self, id):
        table_names = self.__get_table_names()

        for table_name in table_names:
            if self.__table_name != table_name:
                self.__db_cursor.execute(f"DELETE from {table_name} WHERE orig_id = '{id}'")
                self.__db_connection.commit()
    
    def get_all_records(self):
        tables = {}
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} ORDER BY rowid")
        self.__db_connection.commit()
        fetched_data = self.__db_cursor.fetchall()
        tables[self.__table_name] = fetched_data
        table_names = self.__get_table_names()
        for table_name in table_names:
            if self.__table_name != table_name:
                self.__db_cursor.execute(f"SELECT rowid, * FROM {table_name} ORDER BY rowid")
                self.__db_connection.commit()
                fetched_data = self.__db_cursor.fetchall()
                tables[table_name] = fetched_data
        return tables
    
    def add_new_category(self, category_name):
        # Add category table if it doesn't exist
        table_name = f"{self.__table_name}_{category_name}"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            orig_id int,
            name text,
            platform text,
            developer text
            )""")
        self.__db_connection.commit()

    def add_to_category(self, id, category_name):
        # Get record
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
        record = self.__db_cursor.fetchone()
        # Add category table if it doesn't exist
        table_name = f"{self.__table_name}_{category_name}"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            orig_id int,
            name text,
            platform text,
            developer text
            )""")
        # Add record to new category (but only if it hasn't already been added)
        self.__db_cursor.execute(f"SELECT rowid, * FROM {table_name} WHERE orig_id = '{id}'")
        self.__db_connection.commit()
        fetched_data = self.__db_cursor.fetchone()
        if fetched_data is None:
            self.__db_cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", record)
            self.__db_connection.commit()
    
    def remove_from_category(self, id, category_name):
        table_name = f"{self.__table_name}_{category_name}"
        # Remove record from category
        self.__db_cursor.execute(f"DELETE from {table_name} WHERE orig_id = '{id}'")
        self.__db_connection.commit()

    def __get_table_names(self):
        self.__db_cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        self.__db_connection.commit()
        data = self.__db_cursor.fetchall()
        table_names = [x[0] for x in data]
        table_names = [x for x in table_names if self.__table_name in x]
        return table_names


class MusicTable(MediaTable):
    
    def __init__(self, db_connection, db_cursor):
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.__table_name = "music_table"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.__table_name} (
            song text,
            album text,
            artist text
            )""")
    
    def add_record(self, record):
        self.__db_cursor.execute(f"INSERT INTO {self.__table_name} VALUES (?, ?, ?)", record)
        self.__db_connection.commit()
    
    def edit_record(self, id, **kwargs):
        for key in kwargs:
            self.__db_cursor.execute(f"UPDATE {self.__table_name} SET {key} = '{kwargs[key]}' WHERE rowid = '{id}'")
            self.__db_connection.commit()
        self.__edit_record_in_categories(id, **kwargs)
    
    def __edit_record_in_categories(self, id, **kwargs):
        table_names = self.__get_table_names()

        for table_name in table_names:
            if self.__table_name != table_name:
                for key in kwargs:
                    self.__db_cursor.execute(f"UPDATE {table_name} SET {key} = '{kwargs[key]}' WHERE orig_id = '{id}'")
                    self.__db_connection.commit()

    
    def delete_record(self, id):
        self.__db_cursor.execute(f"DELETE from {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
        self.__delete_record_in_categories(id)
    
    def __delete_record_in_categories(self, id):
        table_names = self.__get_table_names()

        for table_name in table_names:
            if self.__table_name != table_name:
                self.__db_cursor.execute(f"DELETE from {table_name} WHERE orig_id = '{id}'")
                self.__db_connection.commit()
    
    def get_all_records(self):
        tables = {}
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} ORDER BY rowid")
        self.__db_connection.commit()
        fetched_data = self.__db_cursor.fetchall()
        tables[self.__table_name] = fetched_data
        table_names = self.__get_table_names()
        for table_name in table_names:
            if self.__table_name != table_name:
                self.__db_cursor.execute(f"SELECT rowid, * FROM {table_name} ORDER BY rowid")
                self.__db_connection.commit()
                fetched_data = self.__db_cursor.fetchall()
                tables[table_name] = fetched_data
        return tables
    
    def add_new_category(self, category_name):
        # Add category table if it doesn't exist
        table_name = f"{self.__table_name}_{category_name}"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            orig_id int,
            song text,
            album text,
            artist integer
            )""")
        self.__db_connection.commit()

    def add_to_category(self, id, category_name):
        # Get record
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
        record = self.__db_cursor.fetchone()
        # Add category table if it doesn't exist
        table_name = f"{self.__table_name}_{category_name}"
        self.__db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            orig_id int,
            song text,
            album text,
            artist text
            )""")
        # Add record to new category (but only if it hasn't already been added)
        self.__db_cursor.execute(f"SELECT rowid, * FROM {table_name} WHERE orig_id = '{id}'")
        self.__db_connection.commit()
        fetched_data = self.__db_cursor.fetchone()
        if fetched_data is None:
            self.__db_cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", record)
            self.__db_connection.commit()
    
    def remove_from_category(self, id, category_name):
        table_name = f"{self.__table_name}_{category_name}"
        # Remove record from category
        self.__db_cursor.execute(f"DELETE from {table_name} WHERE orig_id = '{id}'")
        self.__db_connection.commit()

    def __get_table_names(self):
        self.__db_cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        self.__db_connection.commit()
        data = self.__db_cursor.fetchall()
        table_names = [x[0] for x in data]
        table_names = [x for x in table_names if self.__table_name in x]
        return table_names


def print_tables(table_obj):
    tables = table_obj.get_all_records()
    for table in tables:
        print(table)
        for record in tables[table]:
            print("\t", record)
    print()

if __name__ == "__main__":
    # persistent storage DB
    db_connection = sqlite3.connect('media.db')

    # create cursor
    db_cursor = db_connection.cursor()

    movies_table = MoviesTable(db_connection, db_cursor)
    games_table = GamesTable(db_connection, db_cursor)
    music_table = MusicTable(db_connection, db_cursor)

    movie_record = ('The Shawshank Redemption', 'Frank Darabont', 1994)
    movies_table.add_record(movie_record)
    print_tables(movies_table)
    
    game_record = ('Red Dead Redemption 2', 'Rockstar Games', 'PlayStation 4')
    games_table.add_record(game_record)
    print_tables(games_table)
    
    music_record = ('Smells Like Teen Spirit', 'Nevermind', 'Nirvana')
    music_table.add_record(music_record)
    print_tables(music_table)

    
    movies_table.add_to_category(1, "favourites")
    print_tables(movies_table)
    movies_table.edit_record(1, year=2005)
    print_tables(movies_table)

    db_connection.close()
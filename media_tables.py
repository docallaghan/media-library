import abc
import sqlite3

class MediaTable(abc.ABC):

    @abc.abstractmethod
    def add_record(self, record):
        pass
    
    @abc.abstractmethod
    def edit_record(self, id, **kwargs):
        pass
    
    @abc.abstractmethod
    def delete_record(self, id):
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
            db_cursor.execute(f"UPDATE {self.__table_name} SET {key} = '{kwargs[key]}' WHERE rowid = '{id}'")
    
    def delete_record(self, id):
        self.__db_cursor.execute(f"DELETE from {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
    
    def get_all_records(self):
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} ORDER BY rowid")
        fetched_data = self.__db_cursor.fetchall()
        return fetched_data

    
class GamesTable(MediaTable):
    
    def __init__(self, db_connection, db_cursor):
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.__table_name = "games_table"
        db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.__table_name} (
            name text,
            platform text,
            developer text
            )""")
    
    def add_record(self, record):
        self.__db_cursor.execute(f"INSERT INTO {self.__table_name} VALUES (?, ?, ?)", record)
        self.__db_connection.commit()
    
    def edit_record(self, id, **kwargs):
        for key in kwargs:
            db_cursor.execute(f"UPDATE {self.__table_name} SET {key} = '{kwargs[key]}' WHERE rowid = '{id}'")
    
    def delete_record(self, id):
        self.__db_cursor.execute(f"DELETE from {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
    
    def get_all_records(self):
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} ORDER BY rowid")
        fetched_data = self.__db_cursor.fetchall()
        return fetched_data


class MusicTable(MediaTable):
    
    def __init__(self, db_connection, db_cursor):
        self.__db_connection = db_connection
        self.__db_cursor = db_cursor
        self.__table_name = "music_table"
        db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.__table_name} (
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
    
    def delete_record(self, id):
        self.__db_cursor.execute(f"DELETE from {self.__table_name} WHERE rowid = '{id}'")
        self.__db_connection.commit()
    
    def get_all_records(self):
        self.__db_cursor.execute(f"SELECT rowid, * FROM {self.__table_name} ORDER BY rowid")
        fetched_data = self.__db_cursor.fetchall()
        return fetched_data


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
    movies_records = movies_table.get_all_records()
    for x in movies_records:
        print(x)
    
    game_record = ('Red Dead Redemption 2', 'Rockstar Games', 'PlayStation 4')
    games_table.add_record(game_record)
    games_records = games_table.get_all_records()
    for x in games_records:
        print(x)
    
    music_record = ('Smells Like Teen Spirit', 'Nevermind', 'Nirvana')
    music_table.add_record(music_record)
    music_records = music_table.get_all_records()
    for x in music_records:
        print(x)

    music_table.edit_record(1, song="Come as You Are")
    music_table.delete_record(1)
    
    db_connection.close()
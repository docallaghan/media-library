import unittest
import media_tables
import sqlite3
import datetime
import os
os.makedirs('./test_databases', exist_ok=True)

class MediaTablesTesting(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.table_name = "test_table"
        # persistent storage DB
        self.db_connection = sqlite3.connect(f'./test_databases/test_{time_str}.db')
        # create cursor
        self.db_cursor = self.db_connection.cursor()
        self.test_media_table = media_tables.MediaTable(self.db_connection, self.db_cursor, main_table_name=self.table_name, 
            column_dict={"col1": "text", "col2": "text", "col3": "text"})

    def test_add(self):
        """Add a record to the database and then check it is present in the database"""
        record = ("val1", "val2", "val3")
        self.test_media_table.add_record(record)
        table = self.test_media_table.get_all_records()[self.table_name]
        self.assertTrue(len(table)>0)
        record_retrieved = tuple(list(table[-1])[1:]) 
        self.assertTrue(record==record_retrieved)
    
    def test_add_and_delete(self):
        """Add a record to the database and delete it and then make sure it is deleted"""
        record = ("val1", "val2", "val3")
        self.test_media_table.add_record(record)
        table = self.test_media_table.get_all_records()[self.table_name]
        record_id = table[-1][0]
        self.test_media_table.delete_record(record_id)
        table = self.test_media_table.get_all_records()[self.table_name]
        if len(table)>0:
            # Table empty so record has been deleted
            self.assertTrue(True)
        else:
            # Make sure record is not in table
            record_id_retrieved = table[-1][0]
            self.assertTrue(record_id!=record_id_retrieved)


if __name__ == '__main__':
    unittest.main()

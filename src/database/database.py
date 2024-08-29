import sqlite3

from config import database_path


class dbhandler:
    def __init__(self) -> None:
        if not database_path.exists():
            # 新建一个数据库
            con = sqlite3.connect(database_path)
            con.cursor().execute(
                """
                CREATE TABLE thumbnail (
                    path TEXT PRIMARY KEY,
                    uuid TEXT,
                    left REAL,
                    bottom REAL,
                    right REAL,
                    top REAL
                )
                """
            )
            con.commit()
            con.close()
            con = None

        self.conn = sqlite3.connect(database_path, check_same_thread=False)

        # self.conn.enable_load_extension(True)
        # platform = sys.platform
        # if platform == 'win32':
        #     self.conn.load_extension('mod_spatialite.dll')
        # elif platform == 'darwin':
        #     self.conn.load_extension('mod_spatialite.dylib')
        # elif platform.startswith('linux'):
        #     self.conn.load_extension('mod_spatialite.so')
        # else:
        #     raise Exception('Cannot recognize platform {!r}'.format(platform))

    def get_thumb(self, path):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT uuid, left, bottom, right, top FROM thumbnail WHERE path=?", (path,)
        )
        result = cursor.fetchone()

        cursor.close()
        return result

    def insert_thumb(self, path, uuid, extent):
        left, bottom, right, top = extent

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO thumbnail VALUES (?, ?, ?, ?, ?, ?)",
            (path, uuid, left, bottom, right, top),
        )

        self.conn.commit()
        cursor.close()
        return True


if __name__ == "__main__":
    from pathlib import Path

    db_handler = dbhandler(Path(r"C:\Users\xianyu\source\gc-backend\data\db.sqlite3"))
    db_handler.insert_thumb(
        r"D:\Projects\gc_data\2020\2020-01-01\2020-01-01_0000.tif", "123", (1, 2, 3, 4)
    )
    db_handler.get_thumb(r"D:\Projects\gc_data\2020\2020-01-01\2020-01-01_0000.tif")

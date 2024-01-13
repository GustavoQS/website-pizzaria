import mysql.connector


class DB():
    def __init__(self):
        try:
            self.connection = None
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='pizzaria_database'
            )
        except Exception as e:
            print(f'MySQL error: {e}')
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def select(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()

        return resultado

    def select_att(self, sql, arg):
        cursor = self.connection.cursor()
        cursor.execute(sql, arg)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    def edit(self, sql, args):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, args)
        except Exception as e:
            print(f'MySQL: {e}')
            self.connection.rollback()
        finally:
            self.connection.commit()
            cursor.close()
            return 0

    def close(self):
        if self.connection:
            self.connection.close()

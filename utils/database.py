import pyodbc
import os


class Database():
    def __init__(self):
        self.connection = pyodbc.connect(f'Driver={{ODBC Driver 17 for SQL Server}};'
                                         f'Server={os.getenv("SERVER")};'
                                         f'Database={os.getenv("DATABASE")};'
                                         'Trusted_Connection=yes;')
        self.cursor = self.connection.cursor()

    def add_user(self, idPeople, login, password, id_telegram):
        try:
            self.cursor.execute("{CALL InsertUser (?, ?, ?, ?)}", [idPeople, login, password, id_telegram])
            self.connection.commit()
        except pyodbc.Error as Error:
            print('Ошибка при создании пользователя:', Error)

    def check_people(self, name, surname, middlename, phone):
        try:
            self.cursor.execute("{CALL CheckPeopleExists (?, ?, ?, ?)}", [name, surname, middlename, phone])
            row = self.cursor.fetchone()
            if row:
                id_people = row[0]
                return id_people
        except pyodbc.Error as Error:
            print('Ошибка при поиске данных о человеке:', Error)

    def check_user(self, id_people):
        try:
            self.cursor.execute("{CALL CheckUser (?)}", [id_people])
            row = self.cursor.fetchone()
            if row:
                return True
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при поиске пользователя:', Error)


    def check_login(self, login):
        # Тут какая-то проблема, надо проверить почему не отрабатывает.
        try:
            self.cursor.execute("{CALL CheckLogin (?)}", [login])
            row = self.cursor.fetchone()
            if row:
                return True
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при поиске логина:', Error)

    def add_people(self, name, surname, middlename, phone):
        try:
            self.cursor.execute("{CALL AddPeople (?, ?, ?, ?)}", [name, surname, middlename, phone])
            self.connection.commit()
            row = Database.check_people(self, name, surname, middlename, phone)
            if row:
                id_people = row
                return id_people
        except pyodbc.Error as Error:
            print('Ошибка при добавлении данных о человеке:', Error)


    def check_user_data(self, login):
        try:
            self.cursor.execute('{CALL CheckUserData (?)}', [login])
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при проверке данных пользователя:', Error)


    def update_user_tg(self, id_telegram, id_user):
        try:
            self.cursor.execute('{CALL UpdateUserTg (?, ?)}', [id_telegram, id_user])
            self.connection.commit()
        except pyodbc.Error as Error:
            print('Ошибка при обновлении данных телеграмма пользователя:', Error)


    def update_user_tg_null(self, id_telegram):
        try:
            self.cursor.execute('{CALL UpdateUserTgNull (?)}', [id_telegram])
            self.connection.commit()
        except pyodbc.Error as Error:
            print('Ошибка при сбросе пользовательского ID_TELEGRAM:', Error)


    def get_user_pass(self, login):
        try:
            self.cursor.execute('{CALL GetUserPass (?)}', [login])
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при получении пароля пользователя:', Error)


    def get_user_data(self, id_telegram):
        try:
            self.cursor.execute('{ CALL GetUserData (?)}', [id_telegram])
            row = self.cursor.fetchone()
            if row:
                return row
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при получении данных о пользователе:', Error)

    def update_people(self, id_people, name=None, surname=None, middle_name=None, phone_number=None):
        try:
            self.cursor.execute('{ CALL UpdatePeople (?, ?, ?, ?, ?)}',
                                [id_people, name, surname, middle_name, phone_number])
            self.cursor.commit()
        except pyodbc.Error as Error:
            print('Ошибка при обновлении данных о пользователе:', Error)


    def get_user_login(self, id_telegram, id_people = None):
        try:
            self.cursor.execute('{ CALL GetUserLogin (?, ?)}', [id_telegram, id_people])
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при получении логина:', Error)


    def update_pass(self, id_telegram, password):
        try:
            self.cursor.execute('{ CALL UpdateUserPass (?, ?, ?)}', [id_telegram, None, password])
            self.cursor.commit()
        except pyodbc.Error as Error:
            print('Ошибка при получении логина:', Error)


    def find_package(self, id_package, id_people):
        try:
            self.cursor.execute('{ CALL GetPackageData (?, ?)}', [id_package, id_people])
            row = self.cursor.fetchone()
            if row:
                return row
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при поиске посылки:', Error)


    def get_packages(self, id_people, table):
        try:
            self.cursor.execute('{ CALL GetPackages (?, ?)}', [id_people, table])
            row = self.cursor.fetchall()
            if row:
                return row
            else:
                return False
        except pyodbc.Error as Error:
            print('Ошибка при поиске посылки:', Error)


    def __del__(self):
        self.cursor.close()
        self.connection.close()
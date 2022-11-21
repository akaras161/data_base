import os
import mysql.connector


class Guest:
    role = 'guest'

    def __init__(self, new_name: str = 'Guest', new_role: str = 'guest', new_counter: int = 0) -> None:
        self.name = new_name
        self.role = new_role
        self.counter = new_counter
        print('Utworzono obiekt ' + self.name)

    def __del__(self):
        print('Obiekt został usunięty')

    def show_menu(self):
        print('1. Wyszukaj produkt')
        print('2. Zaloguj')
        print('3. Załóż konto')
        print('4. Exit')

    def who_am_i(self) -> None:
        print('Zalogowano jako: ' + self.name)

    def what_is_my_role(self) -> None:
        print('Moja rola to: ' + self.role)


class Unverified(Guest):

    def __del__(self):
        print('Obiekt został usunięty')

    def show_menu(self):
        print('1. Wyszukaj produkt')
        print('2. Zarzadzaj kontem')
        print('3. Wyloguj')
        print('4. Exit')

    def reset_parameters(self):
        self.name = ''
        self.role = ''
        self.counter = 0


class Verified(Unverified):
    def __del__(self):
        print('Obiekt został usunięty')

    def show_menu(self):
        print('1. Wyszukaj produkt')
        print('2. Zarzadzaj kontem')
        print('3. Wyloguj')
        print('4. Exit')


class Admin(Verified):
    def __del__(self):
        print('Obiekt został usunięty')

    def show_menu(self):
        print('1. Zarzadzaj bazą danych')
        print('2. Zarządzaj kontem')
        print('3. Przeglądaj kolejkę')
        print('4. Przeglądaj proponowane produkty')
        print('5. Wyloguj')
        print('6. Exit')


def clear_view():
    os.system('cls')


def create_object(nick, role, counter):
    if role == 'unverified':
        tmp_user = Unverified(nick, role, counter)
    elif role == 'verified':
        tmp_user = Verified(nick, role, counter)
    elif role == 'admin':
        tmp_user = Admin(nick, role, counter)
    return tmp_user


def register():
    print("Rejestracja")
    new_login = input("Login: ")
    new_password = input("Haslo: ")
    new_email = input("Email: ")
    new_nick = input("Nazwa w systemie: ")

    mycursor.execute("SELECT login, haslo, email, nazwa_w_systemie from uzytkownicy")
    myresult = mycursor.fetchall()

    is_there_any = False

    for login, password, email, nick in myresult:
        if login == new_login:
            print("Użytkownik o podanym loginie już istnieje!")
            is_there_any = True
            register()
        elif email == new_email:
            print("Uzytkownik o podanym email już istnieje!")
            is_there_any = True
            register()
        elif nick == new_nick:
            print("Nazwa użytkownika jest zajęta!")
            is_there_any = True
            register()
    if not is_there_any:
        sql_command = "INSERT INTO uzytkownicy (login, haslo, nazwa_w_systemie, email) VALUES (%s, %s, %s, %s)"
        values_to_insert = (new_login, new_password, new_nick, new_email)
        mycursor.execute(sql_command, values_to_insert)
        mydb.commit()
        main_menu()


# def del_acc(current_user):
#     sql_command = "UPDATE uzytkownicy SET login = '', email = '', haslo = '' WHERE nazwa_w_systemie = " + current_user.name
#     mycursor.execute(sql_command)
#     mydb.commit()
#     main_menu()


def log_in():
    username = input("Nazwa użuytkownika: ")
    password = input("Hasło: ")

    sql_command = "SELECT login, haslo, nazwa_w_systemie, rola, licznik FROM uzytkownicy WHERE login ='%s'" % username
    mycursor.execute(sql_command)
    myresult = mycursor.fetchall()

    if username == myresult[0][0] and password == myresult[0][1]:
        print('Zalogowano pomyślnie!')
        current_user = create_object(myresult[0][2], myresult[0][3], myresult[0][4])
        main_menu(current_user)
    else:
        print('Błędny login lub hasło!')
        print('1. Spróbuj ponownie')
        print('2. Powrót do menu')
        choice = input(":")
        if choice == '1':
            log_in()
        elif choice == '2':
            main_menu()


def log_out(current_user):
    del current_user
    main_menu()


def guest_menu():
    print('1. Wyszukaj produkt')
    print('2. Zaloguj')
    print('3. Załóż konto')
    print('4. Exit')


def acc_management_menu(current_user):
    print('1. Usuń konto')
    print("2. Powrót do menu głównego")

    choice = input(":")

    if choice == '1':
        print("Czy na pewno chcesz to zrobić? Tej operacji nie można odwrócić!")
        print("1. TAK")
        print("2. NIE")
        choice = input(":")
        if choice == '1':
            pass
            #del_acc(current_user)
        elif choice == '2':
            acc_management_menu(current_user)
    elif choice == '2':
        main_menu(current_user)


def main_menu(current_user: Guest = Guest) -> None:
    clear_view()
    print('MENU \n')

    if current_user.role == 'guest':
        guest_menu()
    elif current_user.role == 'unverified':
        current_user.show_menu()
    elif current_user.role == 'verified':
        current_user.show_menu()
    elif current_user.role == 'admin':
        current_user.show_menu()

    choice = input(":")

    if current_user.role == 'guest':
        if choice == '1':
            pass
            #search product
        elif choice == '2':
            log_in()
        elif choice == '3':
            register()
            #register
        elif choice == '4':
            exit()
    elif current_user.role == 'unverified' or current_user.role == 'verified':
        if choice == '1':
            pass
            #search product
        elif choice == '2':
            acc_management_menu(current_user)
            #account manage
        elif choice == '3':
            log_out(current_user)
        elif choice == '4':
            exit()
    elif current_user.role == 'admin':
        if choice == '1':
            pass
            #data base management
        elif choice == '2':
            acc_management_menu(current_user)
            #account management
        elif choice == '3':
            pass
            #opinion queue
        elif choice == '4':
            pass
            #new product queue
        elif choice == '5':
            log_out(current_user)
        elif choice == '6':
            exit()


if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="akaras171",
        database="system_logowania"
    )
    mycursor = mydb.cursor()

    main_menu()

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


def log_in():
    mycursor.execute("SELECT login, haslo, nazwa_w_systemie, rola, licznik FROM uzytkownicy")
    myresult = mycursor.fetchall()

    username = input("Nazwa użuytkownika: ")
    password = input("Hasło: ")

    is_logged_in = False

    for login, haslo, nazwa_w_systemie, rola, licznik in myresult:
        if username == login and password == haslo:
            print('Zalogowano pomyślnie!')
            is_logged_in = True
            current_user = create_object(nazwa_w_systemie, rola, licznik)
            main_menu(current_user)
    if not is_logged_in:
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
            pass
            #register
        elif choice == '4':
            exit()
    elif current_user.role == 'unverified' or current_user.role == 'verified':
        if choice == '1':
            pass
            #search product
        elif choice == '2':
            pass
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
            pass
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

from models.models import AddressBook, Record, Phone, Birthday, ClassErrors
from saving_data.data_saving import save_data, load_data
from MENU import menu


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return 'Enter the argument for the command.'
        except KeyError:
            return f"Contact '{args[0][0]}' doesn't exist."
        except ClassErrors as e:
            return str(e)
        
    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    
    if record and record.phones:
        return f"{name}'s phone: {', '.join(phone.value for phone in record.phones)}"
    
    return "Contact doesn't exist"


@input_error
def change_contact_phone(args, book): #Я поменял название функции с change_contact на change_contact_phone, чтоб было понятнее, ведь мы изменяем именно телефон контакта
    name, old_phone, new_phone = args
    record = book.find(name)

    if record:
        record.edit_phone(old_phone, new_phone)

        return "Contact updated."

    return "Contact doesn't exist"
    
    
@input_error
def add_contact(args, book):
    name, phone = args

    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        
    if phone and phone not in [p.value for p in record.phones]:
        record.add_phone(phone)

    return "Contact added."


@input_error
def add_birthday(args, book):
    name, birthday = args

    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        
        return 'Birthday added'
    
    return "Contact doesn't exist"

@input_error
def show_birthday(args, book):
    name = args[0]

    record = book.find(name)

    if record and record.birthday:
        user_birthday = record.birthday.value.strftime("%d.%m.%Y")
        return f"{name}'s birthday: {user_birthday}"
    
    return f"{name}'s birthday doesn't exist"

@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()

    if isinstance(upcoming, str):
        return upcoming
    return "\n".join(
        f"{entry['name']} - Congratulations on {entry['congratulation_date']}" 
        for entry in upcoming
    )
    

def main():
    book = AddressBook()
    book = load_data()
    print(menu)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
            

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "menu":
            print(menu)
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact_phone(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == 'all':
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        elif command == '':
            print('Invalid command.')
        else:
            print("Invalid command.")
    
    save_data(book)


if __name__ == "__main__":
    main()
    

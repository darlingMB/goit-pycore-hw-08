from collections import UserDict
from datetime import datetime
from datetime import timedelta


class ClassErrors(Exception):
    def __init__(self, message, field_type=None):
        super().__init__(message)
        self.message = message
        self.field_type = field_type

    def __str__(self):
        return f"{self.field_type} Error: {self.message}" if self.field_type else self.message


class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass       

class Phone(Field):
    def __init__(self, value):
        if self.validation(value):
            super().__init__(value)
        else:
            raise ValueError("ValueError")
        
    @staticmethod
    def validation(phone):
        if not (phone.isdigit() and len(phone) == 10):
            raise ClassErrors(f"Validation for phone '{phone}' is declined")
        return phone

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ClassErrors("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    

    def add_phone(self, phone):
        self.phones.append(Phone(phone))


    def remove_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)
                return True
        return False


    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False


    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return phone
        return None


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


    def find(self, name):
        if name in self.data:
            return self.data.get(name, None)


    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        
        return False
    

    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        upcoming_birthdays = []
        
        for user, record in self.data.items():
            if record.birthday is not None:

                user_birthday = record.birthday.value
                birthday_this_year = user_birthday.replace(year = current_date.year)
                
                if  birthday_this_year < current_date:
                    birthday_this_year = birthday_this_year.replace(year = current_date.year + 1)
                
                days_to_birthday = (birthday_this_year - current_date).days
                
                if 0 <= days_to_birthday <= 7:
                    if birthday_this_year.weekday() in [5, 6]:
                        days_to_monday = (7 - birthday_this_year.weekday()) % 7
                        congratulation_date = birthday_this_year + timedelta(days=days_to_monday)
                    else:
                        congratulation_date = birthday_this_year
                    
                    upcoming_birthdays.append(
                        {
                        "name": user,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                        }
                    )

        return upcoming_birthdays if upcoming_birthdays else "Nobody have birthday in 7 days"



    def __str__(self):
        contacts_info = []

        for record in self.data.values():
            contacts_info.append(str(record))

        return "\n".join(contacts_info)
    

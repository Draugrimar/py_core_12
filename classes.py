from collections import UserDict
from datetime import date


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)


class Name(Field):
    pass


class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        if len(new_value) == 13 and new_value.startswith("+"):
            self.__value = new_value
        else:
            raise ValueError


class Birthday(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        if len(new_value) == 10:
            self._value = new_value
        else:
            raise ValueError

class Record():
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = None
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = birthday
        
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"Phone {phone} added to contact {self.name}"
        return f"Phone {phone} already in the contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone.value:
                self.phones[idx] = new_phone
                return f"Old phone {old_phone} has been changed to {new_phone}"
        return f"Phone {old_phone} not in the list of phones of contact {self.name}"
    
    def days_to_birthday(self, birthday):
        bday = birthday.value.split(".")
        bday = date(int(bday[2]), int(bday[1]), int(bday[0]))
        today = date.today()
        next_birthday = date(
            today.year, bday.month, bday.day)
        if next_birthday < today:
            next_birthday = date(today.year + 1, bday.month, bday.day)
        return f"{(next_birthday - today).days} days left till birthday"

    def __str__(self):
        if self.birthday:
            return f"{self.name}: {', '.join(str(p) for p in self.phones)} with birthday at {self.birthday.value}"
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"
    
    def __repr__(self):
        if self.birthday:
            return f"{self.name}: {', '.join(str(p) for p in self.phones)} with birthday at {self.birthday.value}"
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Record with name {record.name} saved"
    
    def iterator(self, n=3):
        result = ""
        counter = 0
        for r in self.data.values():
            result += str(r) + "\n"
            counter += 1
            if counter >= n:
                yield result
                result = ""
                counter = 0
        if result:
            yield result


    
    def __str__(self):
        return f"\n".join(str(r) for r in self.data.values())
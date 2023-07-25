from classes import Name, Phone, Birthday, Record, AddressBook
import pickle

# address_book = AddressBook()


def input_error(func):
    def inner_func(*args):
        try:
            return func(*args)
        except IndexError:
            return "Please enter command, name and phone number"
        except KeyError:
            return "No such name in the phone book"
        except ValueError:
            return "Phone number is not correct. It should start with + and be 13 digits total and birthday should be dd.mm.yyyy"

    return inner_func

def hi(*args):
    return "Hi! How can I help you?"

def exit(*args):
    return "Goodbye!"

def show_all(*args):
    return address_book

@input_error
def add(*args):
    if len(args[0]) < 2:
        return "Name is too short"
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if len(args) >= 2:
        if len(args[1]) == 10:
            birthday = Birthday(args[1])
            if len(args) == 3 and len(args[2] == 13):
                phone = Phone(args[2])
                return address_book.add_record(Record(name, phone, birthday))
            return address_book.add_record(Record(name, birthday=birthday))
        phone = Phone(args[1])
        if rec:
            rec.add_phone(phone)
            return address_book.add_record(rec)
        if len(args) == 3:
            birthday = Birthday(args[2])
            return address_book.add_record(Record(name, phone, birthday))
        return address_book.add_record(Record(name, phone))
    return address_book.add_record(Record(name))

@input_error
def phone(*args):
    rec: Record = address_book.get(args[0])
    return ', '.join(str(p) for p in rec.phones)

@input_error
def pages(*args):
    result = ""
    for r in address_book.iterator(int(args[0])):
        result += "\n" + r + "\n" + "Page" + "\n"
    return result

@input_error
def search(*args):
    result = []
    for s in address_book.data.values():
        if args[0] in str(s):
            result.append(s)
    return result

    
@input_error
def delta(*args):
    rec: Record = address_book.get(args[0])
    if rec.birthday:
        return rec.days_to_birthday(rec.birthday)
    else:
        return "We still don`t know the birthday of this contact"

def unknown_command(*args):
    return "Wrong command"

COMMANDS = {
    show_all: ("show all", ),
    hi: ("hello", "hi"),
    add: ("add", "create", "+", "append"),
    phone: ("phone", "show phones"),
    pages: ("iterator", "show", "show pages", "pages"),
    search: ("search", "find"),
    delta: ("delta", "days to birthday"),
    exit: ("exit", "close", "bye", "goodbye", "end")
}

def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split(" ")
                return cmd, data
    return unknown_command, []


def main():
    while True:

        try:
            with open("ab_storage", "rb") as f:
                global address_book
                address_book = pickle.load(f)
        except FileNotFoundError:
            address_book = AddressBook()
        user_input = input("Enter your command: ")
        cmd, data = parser(user_input)
        result = cmd(*data)
        print(result)
        with open("Ab_storage", "wb") as f:
            pickle.dump(address_book, f)
        if cmd == exit:
            break


if __name__ == "__main__":
    main()

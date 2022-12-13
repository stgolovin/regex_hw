from pprint import pprint
import csv
import re


def main():
    contacts_list = open_phonebook()
    header = get_header(contacts_list)
    fix_columns(contacts_list)
    dict_names = terminate_doubles(contacts_list)
    contacts_list_f = dict_to_list(dict_names, contacts_list)
    save_phonebook(contacts_list_f, header)


def open_phonebook():
    with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list

def save_phonebook(contacts_list_f, header):
    pprint(contacts_list_f)
    contacts_list_f.insert(0, header)
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list_f)


def get_header(contacts_list):
    header = contacts_list.pop(0)
    return header


def fix_columns(contacts_list):
    for row in contacts_list:
        if len(row[0].split()) > 2:
            surname = row[0].split().pop()
            row[2] = surname
        if len(row[0].split()) > 1:
            firstname = row[0].split().pop(1)
            row[1] = firstname
        if len(row[0].split()) > 1:
            lastname = row[0].split().pop(0)
            row[0] = lastname
        if len(row[1].split()) > 1:
            surname = row[1].split().pop()
            row[2] = surname
        if len(row[1].split()) > 1:
            firstname = row[1].split().pop(0)
            row[1] = firstname
        text = row[5]
        pattern = '(\+7|8)\s?\(?(\d\d\d)\)?\s?-?(\d\d\d)-?\s?(\d\d)-?\s?(\d\d)\s?\(?(\w+\.)?\s?(\d+)?\)?'
        substitution = r'+7(\2)\3-\4-\5 \6\7'
        result = re.sub(pattern, substitution, text).strip()
        row[5] = result
    return contacts_list


def terminate_doubles(contacts_list: list):
    dict_names = dict()
    for row in contacts_list:
        if row[0] in dict_names.keys():
            if row[3]:
                dict_names[row[0]]['organization'] = row[3]
            if row[4]:
                dict_names[row[0]]['position'] = row[4]
            if row[5]:
                dict_names[row[0]]['phone'] = row[5]
            if row[6]:
                dict_names[row[0]]['email'] = row[6]
        else:
            dict_names[row[0]] = {
                'lastname': row[0],
                'firstname': row[1],
                'surname': row[2],
                'organization': row[3],
                'position': row[4],
                'phone': row[5],
                'email': row[6]
                }
    return dict_names


def dict_to_list(dict_names, contacts_list):
    contacts_list_f = list()
    for chunk in dict_names.values():
        contacts_list = list(chunk.values())
        contacts_list_f.append(contacts_list)
    return contacts_list_f


if __name__ == '__main__':
    main()

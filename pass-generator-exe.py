import tkinter as tk
import secrets
import string
import pyperclip
import json
import os
from tkinter.scrolledtext import ScrolledText


SPECIAL_CHARACTERS = '!?@#$%^*&'

root = tk.Tk()

root.title('Password-Generator')
root.configure(bg='#E8E8E8')
font = ('Arial', 16)

# 'LEFT' FRAME CREATING
left_frame = tk.Frame(root, background='#F5F5F5', padx=5, pady=5)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# 'RIGHT' FRAME CREATING
right_frame = tk.Frame(root, background='#F5F5F5', padx=5, pady=5)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

# WORKING WITH THE LEFT FRAME FIRST ##################################################
# 'LENGTH' FRAME CREATING
length = tk.IntVar()
length_frame = tk.LabelFrame(left_frame, font=font, background='#F5F5F5', padx=5, pady=5, text='Set a password length...')
length_frame.pack(padx=10, pady=10)

# CREATE RADIO BUTTONS FOR PASS LENGTH SELECTION
for i, value in enumerate(range(8, 17, 2)):
    radio = tk.Radiobutton(length_frame, font=font, text=value, variable=length, value=value)
    radio.grid(row=0, column=i, padx=12, pady=5)


# 'PASSWORD' FRAME CREATING
password_frame = tk.LabelFrame(left_frame, font=font, background='#F5F5F5', padx=5, pady=5, text='Your password is:')
password_frame.pack(padx=10, pady=10)

password_entry = tk.Entry(password_frame, font=font, width=30, state='readonly')
password_entry.grid(row=0, columnspan=2, padx=15, pady=15)


def create_password() -> None:
    """Simple function that creates a strong random password from allowed characters"""
    letters = string.ascii_letters
    digits = string.digits
    allowed_characters = digits + letters + digits + SPECIAL_CHARACTERS
    result = ''.join(secrets.choice(allowed_characters) for _ in range(length.get()))

    password_entry.config(state='normal')
    password_entry.delete(0, tk.END)
    password_entry.insert(0, result)
    password_entry.config(state='readonly')

# ADD 'CREATE' BUTTON
create_button = tk.Button(password_frame, text='Create password', font=('Arial', 14), command=create_password)
create_button.grid(row=1, column=0)


def copy_password() -> None:
    """Copies the password to the clipboard"""
    pyperclip.copy(password_entry.get())


# ADD 'COPY' BUTTON
copy_button = tk.Button(password_frame, text='Copy password', font=('Arial', 14), command=copy_password)
copy_button.grid(row=1, column=1)


def display_hidden_save_frame() -> None:
    """Displays hidden_frame"""
    hidden_frame.grid()
    save_success_frame.grid_forget()
    source_entry.delete(0, tk.END)
    login_entry.delete(0, tk.END)


# ADD 'SAVE THIS PASSWORD' BUTTON
save_button = tk.Button(left_frame, foreground='white', background='#ff66b3', text='Save this password', font=('Arial', 14), command=display_hidden_save_frame)
save_button.pack(padx=10, pady=10)


# 'SAVE' FRAME CREATING
save_frame = tk.LabelFrame(left_frame, font=font, background='#F5F5F5', padx=5, pady=5)
save_frame.pack(padx=10, pady=10)

# HIDDEN BUILTIN FRAME CREATING
hidden_frame = tk.LabelFrame(save_frame, font=font, text='Enter data', background='#F5F5F5', padx=5, pady=5)
hidden_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
hidden_frame.grid_forget()


# SOURCE LABEL AND ENTRY
source_label = tk.Label(hidden_frame, text='Source name', font=('Arial', 12))
source_label.pack()

source_entry = tk.Entry(hidden_frame, font=font, width=30)
source_entry.pack(padx=15, pady=15)

# LOGIN LABEL AND ENTRY
login_label = tk.Label(hidden_frame, text='Source login', font=('Arial', 12))
login_label.pack()

login_entry = tk.Entry(hidden_frame, font=font, width=30)
login_entry.pack(padx=15, pady=15)


# 'SUCCESSFULLY SAVED' FRAME AND LABEL
save_success_frame = tk.LabelFrame(save_frame, font=font, background='#F5F5F5', padx=5, pady=5)
save_success_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

save_success_label = tk.Label(save_success_frame, width=40, text='You can save additional data with password.', font=('Arial', 12))
save_success_label.pack()


def save_data_to_json() -> None:
    """Saves data to json, makes hidden_frame hidden"""
    hidden_frame.grid_forget()
    save_success_frame.config(text='Successfully saved!')
    save_success_frame.grid()

    source_name = source_entry.get().strip()
    login = login_entry.get().strip()
    password = password_entry.get().strip()

    # SAVING DATA IS POSSIBLE ONLY IF ALL FIELDS ARE FILLED
    if source_name and login and password:
        new_data = {'source': source_name, 'login': login, 'password': password}

        try:
            with open(os.path.join(os.getcwd(), 'data.json'), 'r') as file:
                data: list = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            data = list()

        data.append(new_data)

        with open(os.path.join(os.getcwd(), 'data.json'), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    display_saved_data()

# ADD 'DONE' BUTTON
done_button = tk.Button(hidden_frame, foreground='white', background='#ff66b3', text='Done', font=('Arial', 14), command=save_data_to_json)
done_button.pack(padx=10, pady=10)

# WORKING WITH THE RIGHT FRAME ##################################################


def display_saved_data() -> None:
    # ENSURE THE FILE EXISTS
    try:
        with open(os.path.join(os.getcwd(), 'data.json'), 'r', encoding='utf-8') as file:
            data: list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('data.json', 'w', encoding='utf-8') as file:
            data = list()

    saved_data_list.config(state='normal')
    saved_data_list.delete('1.0', 'end')

    for item in reversed(data):
        source = item.get('source')
        login = item.get('login')
        password = item.get('password')

        saved_data_list.insert(tk.END, f'<<< {source.upper()} >>>\nLogin: {login}\nPassword: {password}\n>>>  >>>  >>>\n\n')

    saved_data_list.config(state='disabled')


# CREATING SCROLLED TEXT WITH EXISTING PASSWORDS DATA 
saved_data_list = ScrolledText(right_frame, width=30, font=('Arial', 12))
saved_data_list.grid()
display_saved_data()


if __name__ == '__main__':
    root.mainloop()







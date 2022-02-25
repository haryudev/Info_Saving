from tkinter import *
from tkinter import messagebox
import random
import os.path
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generating():
    password = ""
    password_text.delete(0, END)
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    letters_upper = [letter.upper() for letter in letters]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    symbols = "{ } [ ] ( ) ! @ # $ % & * \ / ? ° | : ; ^ ~ + = - _".split()
    randomization = [letters, letters_upper, numbers, symbols]
    for letter in range(random.randint(7, 11)):
        password += f"{random.choice(random.choice(randomization))}"
    password_text.insert(0, password)
# ---------------------------- SAVE PASSWORD ------------------------------- #

#   Save the information


def saving():
    if len(password_text.get()) >= 6 and "@" in email_user_text.get() and len(website_text.get()) >= 1:
        infos_dict = {website_text.get(): {
            "Email:": email_user_text.get(),
            "Password:": password_text.get()
        }}
        try:
            with open("Passwords.json", 'r') as save:
                data = json.load(save)
        #   Create a json doc
        except (UnboundLocalError, json.decoder.JSONDecodeError, FileNotFoundError):
            with open("Passwords.json", 'w') as creating_file:
                json.dump(infos_dict, creating_file)
        #   Append into the json doc
        else:
            data.update(infos_dict)
            with open("Passwords.json", 'w') as save_writing:
                json.dump(data, save_writing, indent=4)
            #   Updating email
        if email_exists:
            if variable_saved_email != email_user_text.get():
                email_saving = messagebox.askquestion(title="Saving Email", message="Do you want to save your email for future use?")
                if email_saving == "yes":
                    with open("Email.json", "w") as email:
                        json.dump(email_user_text.get(), email)
            #   Saving email for future use
        else:
            with open("Email.json", "w") as first_email:
                json.dump(email_user_text.get(), first_email)
        #   Saving box
        messagebox.showinfo(title="Infos Saved", message="Your infos were saved inside of 'Password.text'")
        password_text.delete(0, END)

    #   ERRORS
    #   Nothing Inserted
    elif len(password_text.get()) < 6 and "@" not in email_user_text.get() and len(website_text.get()) < 1:
        messagebox.showerror(title="Nothing Inserted", message="Your password was not saved. It has less than 6 characters,"
                                                               " the website was not inserted and the email is not valid.")
    #   Short and Invalid
    elif len(password_text.get()) < 6 and "@" not in email_user_text.get():
        messagebox.showerror(title="Short and Invalid", message="Your password was not saved. It has less than 6 characters "
                                                                "and the email is not valid.")
    #   Short and Nonexistent
    elif len(password_text.get()) < 6 and len(website_text.get()) < 1:
        messagebox.showerror(title="Short and Nonexistent", message="Your password was not saved. It has less than 6 characters "
                                                              "and you have not inserted a website")
    #   Not an email and Nonexistent
    elif "@" not in email_user_text.get() and len(website_text.get()) < 1:
        messagebox.showerror(title="Not an email and Nonexistent", message="Your password was not saved. You have not inserted a "
                                                                           "website and the email is not valid.")
    #   Short Pass
    elif len(password_text.get()) < 6:
        messagebox.showerror(title="Short Pass", message="Your password was not saved. It should have 6 or more characters")
    #   Not an Email
    elif "@" not in email_user_text.get():
        messagebox.showerror(title="Not an Email", message="Your password was not saved. Your email is not valid.")
    #   Not a website
    else:
        messagebox.showerror(title="Not a website", message="Your password was not saved. You have not inserted a website")


def search():
    #   If you already wrote a site information, it will show you them
    try:
        with open("Passwords.json", "r") as information:
            website_data = json.load(information)
            infos = website_data[website_text.get()]
    except KeyError:
        messagebox.showinfo(title="Not registered site", message="You have not registered any account from this site.")
    else:
        messagebox.showinfo(title=website_text.get(), message=f"Email: {infos['Email:']}\nPassword: {infos['Password:']}")
# ---------------------------- UI SETUP ------------------------------- #

#   Screen configuration

screen = Tk()
screen.title("Password Manager")
screen.config(pady=20, padx=20)
password_image = PhotoImage(file='logo.png')
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=password_image)

#   Website
website_title = Label(text="Website:")
website_text = Entry(width=32)
website_text.focus()

#   Email
email_user = Label(text="Email/Username:")
email_user_text = Entry(width=35)
email_exists = os.path.exists("Email.json")
variable_saved_email = email_user_text.get()
if email_exists:
    try:
        saved_email = open("Email.json", 'r')
        variable_saved_email += json.load(saved_email)
    except json.decoder.JSONDecodeError:
        cheating = open("Email.json", 'w')
        json.dump("", cheating)
    else:
        email_user_text.insert(0, variable_saved_email)
        saved_email.close()

#   Password
password_title = Label(text="Password:")
password_text = Entry(width=32)
password_button = Button(text="Generate Password", width=14, command=password_generating)

#   Add button
add_button = Button(text="Add", width=36, command=saving)

#   Search button
search_button = Button(text="Search", command=search, width=14)

#   Setting positions
canvas.grid(column=1, row=0)

website_title.grid(column=0, row=1)
website_text.grid(column=1, row=1, columnspan=2, sticky="W")

email_user.grid(column=0, row=2)
email_user_text.grid(column=1, row=2, columnspan=2, sticky="EW")

password_title.grid(column=0, row=3)
password_text.grid(column=1, row=3, sticky="W")
password_button.grid(column=2, row=3, sticky="EW")

add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

search_button.grid(column=2, row=1, sticky="E")
screen.mainloop()

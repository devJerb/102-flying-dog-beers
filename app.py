from tkinter import messagebox, END
from tkinter import ttk
import tkinter as Tk
import sqlite3
import json

FONT = ("Helvetica", 20)
BG_COLOR = "#89CFF0"
FONT_COLOR = "#FFF"

global NAME


class Controller(Tk.Tk):
    def __init__(self, *args, **kwargs):  # Controller function; use * and ** for easy argument/parameter validation
        Tk.Tk.__init__(self, *args, **kwargs)  # Tk function

        # frame structure
        container = Tk.Frame(self)
        container.pack(side="bottom", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=5)
        container.grid_columnconfigure(0, weight=5)

        self.frames = {}  # store frames within array

        # iterate through classes and store through a dictionary
        for pages in (MainPage, CreateAccount, LogIn, Contacts, AddContact, DeleteContact, ListContact):
            frame = pages(container, self)
            self.frames[pages] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(MainPage)

    # responsible for navigating through frames
    def show_frame(self, next_frame):
        frame = self.frames[next_frame]
        frame.tkraise()  # holds frames in place


class MainPage(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent, width=100, height=100)
        description = Tk.Label(self, text="""
        


        A simple app that stores
        phone numbers!

        A list of phone numbers of people
        can be found within the preview.
        """, justify="left", bg=BG_COLOR, fg=FONT_COLOR, width=40)
        description.grid(row=0, column=0, padx=0, pady=0)

        description2 = Tk.Label(self, text="""
        Per individual has his/her own log in
        to specify whose phone book 
        is being used.

        Happy Trails! 🍂




        """, justify="left", bg=BG_COLOR, fg=FONT_COLOR, width=40)
        description2.grid(row=1, column=0, padx=0, pady=0)
        description3 = Tk.Label(self, text="""

        """, justify="left", bg=BG_COLOR, fg=FONT_COLOR, width=40)
        description3.grid(row=2, column=0, padx=0, pady=0)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        create_account_btn = Tk.Button(self, text="Create Your Account",
                                       command=lambda: controller.show_frame(CreateAccount), width=20)
        create_account_btn.grid(row=2, column=1, padx=50, pady=0)

        login_btn = Tk.Button(self, text="Log Into Your Account",
                              command=lambda: controller.show_frame(LogIn), width=20)
        login_btn.grid(row=1, column=1, padx=50, pady=0)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        # space = Tk.Label(self, text="           ")
        # space.grid(row=0, column=0, padx=0, pady=10)

        label = Tk.Label(self, text="PHONE BOOK", font=FONT)
        label.grid(row=0, column=1, padx=50, pady=0)


class CreateAccount(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        return_btn = Tk.Button(self, text="Proceed",
                               command=self.create_account, width=20)
        return_btn.grid(row=6, column=2, padx=10, pady=10)

        confirm_btn = Tk.Button(self, text="Back",
                                command=lambda: controller.show_frame(MainPage), width=20)
        confirm_btn.grid(row=6, column=1, padx=10, pady=10)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

        create_account_label = Tk.Label(self, text="Create Account", font=FONT, justify="left")
        create_account_label.grid(row=0, column=2, padx=10, pady=10)

        # Username
        username = Tk.Label(self, text="Username: ", font=FONT, justify="left")
        username.grid(row=1, column=1, padx=10, pady=10)

        self.username_entry = Tk.Entry(self, width=30)
        self.username_entry.grid(row=1, column=2, padx=10, pady=10)

        # Password
        password = Tk.Label(self, text="Password: ", font=FONT, justify="left")
        password.grid(row=3, column=1, padx=10, pady=10)

        self.password_entry = Tk.Entry(self, width=30)
        self.password_entry.grid(row=3, column=2, padx=10, pady=10)

        # Email
        email = Tk.Label(self, text="Email: ", font=FONT, justify="left")
        email.grid(row=4, column=1, padx=10, pady=10)

        self.email_entry = Tk.Entry(self, width=30)
        self.email_entry.grid(row=4, column=2, padx=10, pady=10)

        # Contact Number
        contact_number = Tk.Label(self, text="Contact Number: ", font=FONT, justify="left")
        contact_number.grid(row=5, column=1, padx=10, pady=10)

        self.contact_entry = Tk.Entry(self, width=30)
        self.contact_entry.grid(row=5, column=2, padx=10, pady=10)

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

        self.controller = controller

    def create_account(self):
        if len(self.username_entry.get()) == 0 and len(self.password_entry.get()) == 0 and \
                len(self.email_entry.get()) == 0:
            messagebox.showinfo("Invalid Input", "Please do not leave any fields empty!")
        else:
            if len(self.contact_entry.get()) == 10 and (self.contact_entry.get()).isnumeric():
                login_values = {
                    str(self.username_entry.get().title()): {
                        "username": str(self.username_entry.get()),
                        "password": str(self.password_entry.get()),
                        "email": str(self.email_entry.get()),
                        "contact_number": str(self.contact_entry.get()),
                    }
                }

                try:
                    with open("login.json", mode="r") as data_file:
                        data = json.load(data_file)
                except FileNotFoundError:
                    with open("login.json", mode="w") as data_file:
                        json.dump(login_values, data_file, indent=4)
                else:
                    data.update(login_values)
                    with open("login.json", mode="w") as data_file:
                        json.dump(data, data_file, indent=4)
                finally:
                    # database creation
                    conn = sqlite3.connect(f"{self.username_entry.get().upper()}_BOOTH.db")
                    conn.execute(f'''CREATE TABLE {str(self.username_entry.get().upper())}
                                (NAME TEXT NOT NULL,
                                 CONTACT_NUMBER TEXT NOT NULL
                                )''')
                    # create database while storing it inside its own
                    conn.execute(f"INSERT INTO {str(self.username_entry.get().upper())} (NAME, CONTACT_NUMBER) "
                                 f"VALUES ('{str(self.username_entry.get().title())}', '{str(self.contact_entry.get())}')")
                    conn.close()
                    # proceed to contact forms
                    self.controller.show_frame(MainPage)

                    global NAME
                    NAME = self.username_entry.get()

                    self.username_entry.delete(0, END)
                    self.password_entry.delete(0, END)
                    self.email_entry.delete(0, END)
                    self.contact_entry.delete(0, END)
            else:
                messagebox.showinfo("Invalid Input", "Contact Number must be numeric!")


class LogIn(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        confirm_btn = Tk.Button(self, text="Proceed",
                                command=self.log_in, width=20)
        confirm_btn.grid(row=6, column=2, padx=30, pady=10)

        return_btn = Tk.Button(self, text="Back",
                               command=lambda: controller.show_frame(MainPage), width=20)
        return_btn.grid(row=6, column=1, padx=30, pady=10)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

        label = Tk.Label(self, text="Log In", font=FONT)
        label.grid(row=0, column=2, padx=10, pady=10)

        username_label = Tk.Label(self, text="Username: ", font=FONT, justify="left")
        username_label.grid(row=1, column=1, padx=10, pady=10)

        self.username_entry = Tk.Entry(self, width=30)
        self.username_entry.grid(row=1, column=2, padx=10, pady=10)

        password = Tk.Label(self, text="Password: ", font=FONT, justify="left")
        password.grid(row=3, column=1, padx=10, pady=10)

        self.password_entry = Tk.Entry(self, width=30)
        self.password_entry.grid(row=3, column=2, padx=10, pady=10)

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

        self.controller = controller

    def log_in(self):
        if len(self.username_entry.get()) == 0 or len(self.password_entry.get()) == 0:
            messagebox.showinfo("Invalid Input", "Please do not leave any fields empty!")
        else:
            with open("login.json", mode="r") as data_file:
                data = json.load(data_file)
                specific = data[self.username_entry.get().title()]
                if specific["username"].lower() == self.username_entry.get().lower() and \
                        specific["password"].lower() == self.password_entry.get().lower():
                    self.controller.show_frame(Contacts)

                    global NAME
                    NAME = self.username_entry.get()

                    self.username_entry.delete(0, END)
                    self.password_entry.delete(0, END)
                else:
                    messagebox.showinfo("Invalid Input", "Incorrect username or password!")


class Contacts(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        add_button = Tk.Button(self, text="Add Number",
                               command=lambda: controller.show_frame(AddContact))
        add_button.grid(row=1, column=1, padx=10, pady=10)

        delete_button = Tk.Button(self, text="Delete Number",
                                  command=lambda: controller.show_frame(DeleteContact))
        delete_button.grid(row=2, column=1, padx=10, pady=10)

        list_button = Tk.Button(self, text="Display List",
                                command=lambda: controller.show_frame(ListContact))
        list_button.grid(row=3, column=1, padx=10, pady=10)

        return_btn = Tk.Button(self, text="Back",
                               command=lambda: controller.show_frame(MainPage))
        return_btn.grid(row=6, column=1, padx=10, pady=10)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #


class AddContact(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        button1 = Tk.Button(self, text="Proceed",
                            command=self.add_contact)
        button1.grid(row=6, column=2, padx=10, pady=10)

        button1 = Tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(Contacts))
        button1.grid(row=6, column=1, padx=10, pady=10)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

        label = Tk.Label(self, text="Add Contacts", font=FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # First Name
        username = Tk.Label(self, text="First Name: ", font=FONT)
        username.grid(row=1, column=2, padx=10, pady=10)

        self.username_entry = Tk.Entry(self)
        self.username_entry.grid(row=1, column=3, padx=10, pady=10)

        # Contact Number
        contact_number = Tk.Label(self, text="Contact Number: ", font=FONT)
        contact_number.grid(row=3, column=2, padx=10, pady=10)

        self.contact_entry = Tk.Entry(self)
        self.contact_entry.grid(row=3, column=3, padx=10, pady=10)

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

    def add_contact(self):
        if len(self.username_entry.get()) == 0 and len(self.contact_entry.get()) < 10 and \
                (not self.contact_entry.get().isnumeric()):
            messagebox.showinfo("Invalid Input", "Please do not leave any fields empty!")
        else:
            conn = sqlite3.connect(F"{str(NAME.upper())}_BOOTH.db")
            conn.execute(
                f"INSERT INTO {str(NAME.upper())} (NAME, CONTACT_NUMBER) VALUES ('{str(self.username_entry.get())}', '{str(self.contact_entry.get())}')")
            print(f"Successful\nTotal Changes Made: {conn.total_changes}")
            conn.commit()
            conn.close()

            self.username_entry.delete(0, END)
            self.contact_entry.delete(0, END)


class DeleteContact(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        confirm_btn = Tk.Button(self, text="Proceed",
                                command=self.delete_contact)
        confirm_btn.grid(row=6, column=2, padx=10, pady=10)

        return_btn = Tk.Button(self, text="Back",
                               command=lambda: controller.show_frame(Contacts))
        return_btn.grid(row=6, column=1, padx=10, pady=10)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

        label = Tk.Label(self, text="Delete Contacts", font=FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # First Name
        username = Tk.Label(self, text="First Name: ", font=FONT)
        username.grid(row=1, column=2, padx=10, pady=10)

        self.username_entry = Tk.Entry(self)
        self.username_entry.grid(row=1, column=3, padx=10, pady=10)

        # ---------------------------------------------- ENTRIES -------------------------------------------- #

    def delete_contact(self):
        if self.username_entry.get() == 0:
            messagebox.showinfo("Invalid Input", "Please do not leave any fields empty!")
        else:
            conn = sqlite3.connect(f"{str(NAME.upper())}_BOOTH.db")
            conn.execute(f"DELETE from {str(NAME.upper())} where NAME = '{self.username_entry.get()}'")
            print(f"Successful\nTotal Changes Made: {conn.total_changes}")
            conn.commit()
            conn.close()


class ListContact(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

        confirm_btn = Tk.Button(self, text="Proceed",
                                command=self.list_contact)
        confirm_btn.grid(row=6, column=2, padx=10, pady=10)

        return_btn = Tk.Button(self, text="Back",
                               command=lambda: controller.show_frame(Contacts))
        return_btn.grid(row=6, column=1, padx=10, pady=10)

        # ------------------------------------------ ACCESS BUTTONS ----------------------------------------- #

    def list_contact(self):
        conn = sqlite3.connect(f"{str(NAME.upper())}_BOOTH.db")
        cursor = conn.execute(f"SELECT NAME, CONTACT_NUMBER from {str(NAME.upper())}")
        for row in cursor:
            list_label = Tk.Label(self, text=f"Name: {row[0]}\nContact Number: {row[1]}")
            list_label.grid(row=2, column=0, padx=10, pady=10)
        print(f"\nSuccessful\nTotal Changes Made: {conn.total_changes}")

        conn.close()


Controller()
Tk.mainloop()

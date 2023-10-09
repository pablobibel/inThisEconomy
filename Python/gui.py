import requests
from tkinter import *
from tkinter import messagebox
from datetime import datetime, date
import expense_database
import sys
from tkinter import ttk

expense_database.create_database()
root = Tk()

root.title("IN THIS ECONOMY?!")
root.iconbitmap(bitmap=r"C:\Users\Pablo\Desktop\Python\icon.ico")

root.geometry("1280x720")
root.minsize(1280, 720)

style = ttk.Style()


light_bg = "#f5f5f5"
light_fg = "#000000"
light_button = "#d4d4d4"

dark_bg = "#14171A"
dark_fg = "#ffffff"
dark_button = "#001641"


current_mode = "light"


def fetch_dolar_blue():
    url = "https://api.bluelytics.com.ar/v2/latest"
    response = requests.get(url)
    data = response.json()

    blue_rate = data["blue"]["value_sell"]
    dolar_blue_label.config(text=f"Dolar Blue: {blue_rate:.2f}")


def refresh_label():
    current_balance = expense_database.fetch_balance()
    expenses = expense_database.total_expenses()
    remaining_balance = current_balance - expenses
    balance_label.config(text=f"CURRENT BALANCE: {remaining_balance:.2f} PESOS")


def update_balance_label():
    refresh_label()

    current_balance = expense_database.fetch_balance()
    expenses = expense_database.total_expenses()
    remaining_balance = current_balance - expenses

    if remaining_balance < 0:
        warning_window = Toplevel(root)
        warning_window.title("Warning!")
        warning_label = Label(
            warning_window,
            text="Balance has gone below 0!",
            font=("Arial", 15),
            fg="red",
        )
        warning_label.pack(padx=20, pady=20)
        ok_button = Button(warning_window, text="OK", command=warning_window.destroy)
        ok_button.pack(pady=10)


def update_entry():
    if tree.selection():
        selected_item = tree.selection()[0]
        item_id = tree.item(selected_item, "values")[0]

        item_name = item_name_var.get()
        item_price = item_price_var.get()
        city = city_var.get()
        purchase_date = purchase_date_var.get()

        try:
            item_price = float(item_price)
        except ValueError:
            messagebox.showwarning("Invalid item price", "Please insert a nuber")
            return
        try:
            purchase_date = datetime.strptime(purchase_date, "%d/%m").date()
        except ValueError:
            messagebox.showwarning("Invalid purchase date", "Please use DD / MM format")

            return

        expense_database.update_expense(
            item_id, item_price, item_name, city, purchase_date
        )

        refresh()
        refresh_label()
    else:
        messagebox.showwarning("Warning", "Please select a row to load")


def refresh():
    expenses = expense_database.fetch_expenses()

    for item in tree.get_children():
        tree.delete(item)

    for expense in expenses:
        tree.insert("", "end", values=expense)


def create_entry():
    item_name = item_name_var.get()
    item_price = item_price_var.get()
    city = city_var.get()
    purchase_date = purchase_date_var.get()
    if not item_name or not item_price or not city or not purchase_date:
        messagebox.showinfo("Fill", "Please fill all the fields")
        return
    try:
        item_price = float(item_price)
    except ValueError:
        messagebox.showinfo("Error", "Invalid Price")
        return
    try:
        purchase_date = datetime.strptime(purchase_date, "%d/%m").date()

    except ValueError:
        messagebox.showwarning("Invalid purchase date", "Please use DD / MM format")
        return
    expense_database.insert_expense(item_price, item_name, city, purchase_date)

    item_name_var.set("")
    item_price_var.set("")
    city_var.set("")
    purchase_date_var.set("")
    refresh()
    update_balance_label()
    refresh_label()


def open_balance_window():
    balance_window = Toplevel(root)
    balance_window.title("Balance")
    balance_window.geometry("600x200")
    balance_label = Label(
        balance_window,
        text="How much money do you have to spend on the month?",
        font=("Arial", 15),
    )
    balance_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    balance_entry = Entry(balance_window, font=("Arial", 15))
    balance_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    def save_balance():
        balance = balance_entry.get()
        try:
            balance = float(balance)
        except ValueError:
            messagebox.showerror("ERROR", "Invalid Balance")
            return
        expense_database.update_balance(balance)
        refresh_label()
        refresh()
        balance_window.destroy()

    balance_button = Button(
        balance_window, text="Save Balance", font=("Arial", 15), command=save_balance
    )
    balance_button.grid(row=2, column=0, padx=10, pady=10)

    close_button = Button(
        balance_window, text="Close", font=("Arial", 15), command=balance_window.destroy
    )
    close_button.grid(row=2, column=1, padx=10, pady=10)


def set_current_date():
    today = date.today()

    formatted_date = today.strftime("%d/%m")
    purchase_date_var.set(formatted_date)
    refresh()
    refresh_label()


def delete_expense():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showwarning("Warning", "Please select an expense to delete.")
        return

    item_values = tree.item(selected_item, "values")

    response = messagebox.askyesno(
        "Confirmation", f"Do you want to delete the expense: {item_values[2]}?"
    )
    if response:
        expense_database.delete_expense(item_values[0])
        refresh()
        refresh_label()


item_name_var = StringVar()
item_price_var = StringVar()
city_var = StringVar()
purchase_date_var = StringVar()

item_name_label = Label(root, text="ITEM NAME:", font=("Arial", 20))
item_name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

item_name_entry = Entry(root, textvariable=item_name_var, font=("Arial", 20))
item_name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")


create_button = Button(
    root,
    text="Create",
    font=("Arial", 20),
    command=create_entry,
)
create_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")


balance_button = Button(
    root, text="Balance", command=open_balance_window, font=("Arial", 20)
)
balance_button.grid(row=5, column=2, padx=10, pady=10, sticky="ew")

item_price_label = Label(root, text="ITEM PRICE:", font=("Arial", 20))
item_price_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
item_price_entry = Entry(root, textvariable=item_price_var, font=("Arial", 20))
item_price_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")


update_button = Button(root, text="Update", font=("Arial", 20), command=update_entry)
update_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")


delete_button = Button(root, text="Delete", font=("Arial", 20), command=delete_expense)
delete_button.grid(row=4, column=2, padx=10, pady=10, sticky="ew")


city_label = Label(root, text="CITY OF PURCHASE:", font=("Arial", 20))
city_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
city_entry = Entry(root, textvariable=city_var, font=("Arial", 20))
city_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

balance_label = Label(root, text="", font=("Arial", 20))
balance_label.grid(row=0, column=0, padx=10, pady=10, sticky="w", columnspan=5)

purchase_date_label = Label(root, text="PURCHASE DATE:", font=("Arial", 20))
purchase_date_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

purchase_date_entry = Entry(root, textvariable=purchase_date_var, font=("Arial", 20))
purchase_date_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

dolar_blue_label = Label(root, text="", font=("Arial", 20))
dolar_blue_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")


# purchase_date_format_label = Label(
#    root, text="Format: DD / MM", font=("Arial", 12), fg="grey")
# purchase_date_format_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")


current_date_button = Button(
    root, text="Current Date", font=("Arial", 20), command=set_current_date
)
current_date_button.grid(row=6, column=1, padx=10, pady=10, sticky="ew")


tree = ttk.Treeview(
    root,
    columns=("ID", "Amount", "Name", "City", "Date"),
    show="headings",
)

tree.heading("ID", text="ID")
tree.heading("Amount", text="Amount")
tree.heading("Name", text="Name")
tree.heading("City", text="City")
tree.heading("Date", text="Date")


tree.column("ID", width=10)
tree.column("Amount", width=8)
tree.column("Name", width=10)
tree.column("City", width=10)
tree.column("Date", width=10)

tree.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")


refresh()


def toggle_mode():
    global current_mode
    if current_mode == "light":
        root.config(bg=dark_bg)
        mode_button.config(bg=dark_button, fg=dark_fg, text="Light Mode")

        create_button.config(bg=dark_button, fg=dark_fg)
        current_date_button.config(bg=dark_button, fg=dark_fg)
        delete_button.config(bg=dark_button, fg=dark_fg)
        update_button.config(bg=dark_button, fg=dark_fg)
        balance_button.config(bg=dark_button, fg=dark_fg)

        item_name_label.config(bg=dark_bg, fg=dark_fg)
        item_price_label.config(bg=dark_bg, fg=dark_fg)
        city_label.config(bg=dark_bg, fg=dark_fg)
        purchase_date_label.config(bg=dark_bg, fg=dark_fg)
        dolar_blue_label.config(bg=dark_bg, fg=dark_fg)
        balance_label.config(bg=dark_bg, fg=dark_fg)

        current_mode = "dark"
    else:
        root.config(bg=light_bg)
        mode_button.config(bg=light_button, fg=light_fg, text="Dark Mode")

        create_button.config(bg=light_button, fg=light_fg)
        current_date_button.config(bg=light_button, fg=light_fg)
        delete_button.config(bg=light_button, fg=light_fg)
        update_button.config(bg=light_button, fg=light_fg)
        balance_button.config(bg=light_button, fg=light_fg)

        item_name_label.config(bg=light_bg, fg=light_fg)
        item_price_label.config(bg=light_bg, fg=light_fg)
        city_label.config(bg=light_bg, fg=light_fg)
        purchase_date_label.config(bg=light_bg, fg=light_fg)
        dolar_blue_label.config(bg=light_bg, fg=light_fg)
        balance_label.config(bg=light_bg, fg=light_fg)
        current_mode = "light"


mode_button = Button(root, font=30, text="💡", command=toggle_mode)
mode_button.grid(row=0, column=5, padx=10, pady=10)


def on_tree_select(event):
    selected_item = tree.selection()[0]
    item_data = tree.item(selected_item, "values")

    item_name_var.set(item_data[2])
    item_price_var.set(item_data[1])
    city_var.set(item_data[3])
    purchase_date_var.set(item_data[4])


tree.bind("<ButtonRelease-1>", on_tree_select)


def initialize_app():
    update_balance_label()
    refresh()
    refresh_label()
    fetch_dolar_blue()


initialize_app()


def exit_app():
    root.destroy()
    sys.exit()


root.mainloop()

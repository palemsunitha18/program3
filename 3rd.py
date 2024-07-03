import random
import string
from tkinter import *
from tkinter import messagebox

class InvalidInputError(Exception):
    pass

root_window = None  # Define root_window as a global variable

def generate_password(pw_length):
    # Define character classes for password generation
    character_classes = [
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
        string.ascii_lowercase
    ]

    # Generate password with characters from each class
    password = ''.join(random.choice(char_class) for char_class in character_classes)

    # Add additional random characters to meet the desired length
    for _ in range(pw_length - 3):
        character_class = random.choice(character_classes)
        password += random.choice(character_class)

    # Shuffle password characters for randomness
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

def generate_passwords(num_passwords, password_lengths):
    passwords = []
    for _ in range(num_passwords):
        password_length = random.choice(password_lengths)
        password = generate_password(password_length)
        passwords.append(password)
    return passwords

def generate_passwords_gui():
    global root_window  # Declare root_window as a global variable
    def generate_passwords_callback():
        result_text.delete(1.0, END)  # Clear previous results
        try:
            # Get number of passwords and password lengths from input
            num_passwords = int(num_passwords_entry.get())
            password_lengths_str = lengths_entry.get().split(',')
            password_lengths = [max(3, int(length)) for length in password_lengths_str]

            # Validate input values
            if num_passwords <= 0 or any(length < 3 for length in password_lengths):
                raise InvalidInputError("Invalid input. Please enter valid values.")

            # Generate passwords and display results
            passwords = generate_passwords(num_passwords, password_lengths)
            for i, password in enumerate(passwords, start=1):
                result_text.insert(END, f"Password #{i}: {password}\n")

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
        except InvalidInputError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Set up the main GUI window
    root_window = Tk()
    root_window.title("Password Generator")
    root_window.geometry("500x400")
    root_window.configure(bg="#EFEFEF")

    # GUI components
    num_passwords_label = Label(root_window, text="Number of Passwords:")
    lengths_label = Label(root_window, text="Enter Password Lengths (Minimum 3, separated by commas):")

    num_passwords_entry = Entry(root_window)
    lengths_entry = Entry(root_window)

    result_text = Text(root_window, wrap=WORD, height=10, width=40)
    scrollbar = Scrollbar(root_window, command=result_text.yview)

    generate_button = Button(root_window, text="Generate Passwords", command=generate_passwords_callback, bg="#83E0F2")

    # Grid Layout
    num_passwords_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
    num_passwords_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

    lengths_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
    lengths_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

    generate_button.grid(row=2, column=0, columnspan=2, pady=10)

    result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=W + E + N + S)
    scrollbar.grid(row=3, column=2, sticky=N + S)

    result_text.config(yscrollcommand=scrollbar.set)

    root_window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event
    root_window.mainloop()

def on_closing():
    global root_window  # Access root_window as a global variable
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root_window.destroy()  # Use root_window instead of root

if __name__ == "__main__":
    generate_passwords_gui()

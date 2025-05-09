import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import google.generativeai as genai
import tkinter as tk
from tkinter import Toplevel, Label, Text, Entry, Button, END, WORD, X, BOTH
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def get_db_connection():
    return sqlite3.connect('donation_platform.db')
def send_email_notification(new_need_details):
    # Connect to the database to fetch all users' emails
    conn = sqlite3.connect('donation_platform.db')
    cursor = conn.cursor()
    
    # Fetch emails of all users (assuming a table named "users" exists with an "email" column)
    cursor.execute("SELECT email FROM users")
    user_emails = cursor.fetchall()
    conn.close()

    # Email setup
    sender_email = "sangamspoorthyreddy@gmail.com"
    sender_password = "gwpl lgdg cbsa bhcy"  # You can use an app-specific password if using Gmail
    subject = "New Need Registered on Donation Platform"
    
    # Create the email content
    body = f"""
    A new need has been registered on the platform:
    
    {new_need_details}

    Please log in to view more details and donate.
    """


    # Connect to Gmail's SMTP server and send emails to all users
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            
            for user_email in user_emails:
            # Create a fresh email message for each recipient
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = user_email[0]
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
            
                server.sendmail(sender_email, user_email[0], msg.as_string())
        
        print("Emails sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
# Connect to database

# Password check for login
def login_user():
    username = login_username.get()
    password = login_password.get()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Success", f"Welcome back, {user[1]}!")
        root.withdraw()  # Hide the login/register window
        open_main_menu(user)  # Pass the user data
        # You can redirect to main menu here later
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Register a new user
def register_user():
    name = reg_name.get()
    email = reg_email.get()
    username = reg_username.get()
    password = reg_password.get()

    if not (name and email and username and password):
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
                       (name, email, username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        reg_name.delete(0, tk.END)
        reg_email.delete(0, tk.END)
        reg_username.delete(0, tk.END)
        reg_password.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    conn.close()
def open_my_donations(user_id):
    donations_window = tk.Toplevel()
    donations_window.title("My Donations")
    donations_window.geometry("600x400")

    tk.Label(donations_window, text="My Donations", font=("Helvetica", 14)).pack(pady=10)

    # Treeview to show donations
    tree = ttk.Treeview(donations_window, columns=("Need Type", "Place", "Message"), show='headings')
    tree.heading("Need Type", text="Need Type")
    tree.heading("Place", text="Place")
    tree.heading("Message", text="Message")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Fetch user donations
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT needs.need_type, needs.place, donations.message
        FROM donations
        JOIN needs ON donations.need_id = needs.id
        WHERE donations.user_id = ?
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            tree.insert('', 'end', values=row)
    else:
        tk.Label(donations_window, text="You haven't made any donations yet.", fg="gray").pack(pady=10)

def open_main_menu(user):
    main_menu = tk.Toplevel()
    main_menu.title("Main Menu")
    main_menu.geometry("400x300")

    tk.Label(main_menu, text=f"Hello, {user[1]}", font=("Helvetica", 14)).pack(pady=10)

    # Check if user is verified
    if user[5] == 1:
        tk.Button(main_menu, text="Donate", width=20, command=lambda: open_donation_screen(user[0])).pack(pady=10)

    tk.Button(main_menu, text="Register a Need", width=20, command=lambda: open_register_need(user[0])).pack(pady=10)


    # Show admin panel button if is_admin = 1
    if user[6] == 1:
        tk.Button(main_menu, text="Admin Panel", width=20, command=open_admin_panel).pack(pady=10)
    tk.Button(main_menu, text="View My Donations", width=20, command=lambda: open_my_donations(user[0])).pack(pady=10)
    tk.Button(main_menu, text="Chatbot", width=20, command=chatbot).pack(pady=10)
    tk.Button(main_menu, text="Logout", width=20, command=lambda: (main_menu.destroy(), root.deiconify())).pack(pady=20)
def open_register_need(user_id):
    need_window = tk.Toplevel()
    need_window.title("Register a Need")
    need_window.geometry("400x400")

    tk.Label(need_window, text="Type of Need").pack(pady=5)
    need_type_entry = tk.Entry(need_window)
    need_type_entry.pack()

    tk.Label(need_window, text="Description").pack(pady=5)
    description_entry = tk.Entry(need_window)
    description_entry.pack()

    tk.Label(need_window, text="Place").pack(pady=5)
    place_entry = tk.Entry(need_window)
    place_entry.pack()

    tk.Label(need_window, text="Contact Details").pack(pady=5)
    contact_entry = tk.Entry(need_window)
    contact_entry.pack()

    def submit_need():
        need_type = need_type_entry.get()
        description = description_entry.get()
        place = place_entry.get()
        contact = contact_entry.get()

        if not (need_type and place and contact):
            messagebox.showwarning("Missing Info", "Please fill in all required fields.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO needs (need_type, description, place, contact)
            VALUES (?, ?, ?, ?)
        ''', (need_type, description, place, contact))
        new_need_details = f"Type: {need_type}\nDescription: {description}\nPlace: {place}\nContact: {contact}"
        send_email_notification(new_need_details)

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Need registered successfully!\nAwaiting admin verification.")
        need_window.destroy()

    tk.Button(need_window, text="Submit Need", command=submit_need).pack(pady=20)
def open_donation_screen(user_id):
    donation_window = tk.Toplevel()
    donation_window.title("Donate to a Need")
    donation_window.geometry("700x400")

    tk.Label(donation_window, text="Select a Need to Donate", font=("Helvetica", 14)).pack(pady=10)

    needs_tree = ttk.Treeview(donation_window, columns=("ID", "Need Type", "Place", "Contact"), show='headings')
    needs_tree.heading("ID", text="ID")
    needs_tree.heading("Need Type", text="Need Type")
    needs_tree.heading("Place", text="Place")
    needs_tree.heading("Contact", text="Contact")
    needs_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_verified_needs(user_id):  # <-- Add parameter here
        needs_tree.delete(*needs_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, need_type, place, contact
            FROM needs
            WHERE is_verified = 1 AND id NOT IN (
                SELECT need_id FROM donations WHERE user_id = ?
            )
        ''', (user_id,))
        results = cursor.fetchall()
        conn.close()

        if not results:
            messagebox.showinfo("No Needs Available", "You have already donated to all available verified needs.")
        else:
            for row in results:
                needs_tree.insert('', 'end', values=row)

    load_verified_needs(user_id)  # <-- Now pass user_id here


    def donate_to_selected():
        selected = needs_tree.selection()
        if not selected:
            messagebox.showwarning("Select a Need", "Please select a need to donate.")
            return

        need_id = needs_tree.item(selected[0])['values'][0]

        def confirm_donation():
            message = donation_msg.get()

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO donations (user_id, need_id, message)
                VALUES (?, ?, ?)
            ''', (user_id, need_id, message))
            conn.commit()
            conn.close()

            messagebox.showinfo("Thank You", "Your donation has been recorded!")
            confirm_win.destroy()
            donation_window.destroy()

        confirm_win = tk.Toplevel()
        confirm_win.title("Confirm Donation")
        confirm_win.geometry("350x200")

        tk.Label(confirm_win, text="Enter a message for the recipient (optional)").pack(pady=5)
        donation_msg = tk.Entry(confirm_win, width=40)
        donation_msg.pack(pady=5)

        tk.Button(confirm_win, text="Confirm Donation", command=confirm_donation).pack(pady=10)

    tk.Button(donation_window, text="Donate to Selected Need", command=donate_to_selected).pack(pady=10)

    load_verified_needs(user_id)
def show_confirmation_page(need_details, message):
    confirmation_win = tk.Toplevel()
    confirmation_win.title("Donation Confirmed")
    confirmation_win.geometry("400x300")

    tk.Label(confirmation_win, text="🎉 Donation Successful!", font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Label(confirmation_win, text="Thank you for your kindness!", font=("Helvetica", 12)).pack(pady=5)

    tk.Label(confirmation_win, text=f"Donated To: {need_details[1]}", font=("Helvetica", 10)).pack(pady=5)
    tk.Label(confirmation_win, text=f"Location: {need_details[2]}", font=("Helvetica", 10)).pack(pady=5)
    tk.Label(confirmation_win, text=f"Contact: {need_details[3]}", font=("Helvetica", 10)).pack(pady=5)
    tk.Label(confirmation_win, text=f"Your Message: {message}", wraplength=350, justify="center").pack(pady=10)

    tk.Button(confirmation_win, text="Close", command=confirmation_win.destroy).pack(pady=20)


def open_admin_panel():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("700x500")

    notebook = ttk.Notebook(admin_window)
    notebook.pack(fill='both', expand=True)

    # ========== USERS TAB ==========
    user_tab = ttk.Frame(notebook)
    notebook.add(user_tab, text='Verify Users')

    user_tree = ttk.Treeview(user_tab, columns=("ID", "Name", "Email", "Username"), show='headings')
    user_tree.heading("ID", text="ID")
    user_tree.heading("Name", text="Name")
    user_tree.heading("Email", text="Email")
    user_tree.heading("Username", text="Username")
    user_tree.pack(pady=10, fill="both", expand=True)

    def load_unverified_users():
        user_tree.delete(*user_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, username FROM users WHERE is_verified=0 AND is_admin=0")
        for row in cursor.fetchall():
            user_tree.insert('', 'end', values=row)
        conn.close()

    def verify_selected_user():
        selected = user_tree.selection()
        if selected:
            user_id = user_tree.item(selected[0])['values'][0]
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_verified=1 WHERE id=?", (user_id,))
            conn.commit()
            conn.close()
            load_unverified_users()
            messagebox.showinfo("Verified", "User verified successfully.")

    tk.Button(user_tab, text="Verify Selected User", command=verify_selected_user).pack(pady=10)

    # ========== NEEDS TAB ==========
    needs_tab = ttk.Frame(notebook)
    notebook.add(needs_tab, text='Verify Needs')

    needs_tree = ttk.Treeview(needs_tab, columns=("ID", "Type", "Place", "Contact"), show='headings')
    needs_tree.heading("ID", text="ID")
    needs_tree.heading("Type", text="Type")
    needs_tree.heading("Place", text="Place")
    needs_tree.heading("Contact", text="Contact")
    needs_tree.pack(pady=10, fill="both", expand=True)

    def load_unverified_needs():
        needs_tree.delete(*needs_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, need_type, place, contact FROM needs WHERE is_verified=0")
        for row in cursor.fetchall():
            needs_tree.insert('', 'end', values=row)
        conn.close()

    def verify_selected_need():
        selected = needs_tree.selection()
        if selected:
            need_id = needs_tree.item(selected[0])['values'][0]
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE needs SET is_verified=1 WHERE id=?", (need_id,))
            conn.commit()
            conn.close()
            load_unverified_needs()
            messagebox.showinfo("Verified", "Need verified successfully.")

    tk.Button(needs_tab, text="Verify Selected Need", command=verify_selected_need).pack(pady=10)

    # Load data on open
    load_unverified_users()
    load_unverified_needs()



# Configure the Gemini API Key
genai.configure(api_key="AIzaSyBUkd0VzVOyPSWGlR8JPwNzePRBUWUikJE")

# ===== GUI APP FUNCTION =====
def chatbot():
    top = Toplevel()
    top.geometry("600x700")
    top.title("Donation Platform Chatbot - Gemini")

    Label(top, text="Ask your donation-related questions!", font=("Arial", 16, "bold"), bg="lightgreen", pady=10).pack(fill=X)

    text_area = Text(top, wrap=WORD, font=("Arial", 12))
    text_area.pack(padx=10, pady=10, expand=True, fill=BOTH)

    entry = Entry(top, font=("Arial", 14))
    entry.pack(padx=10, pady=5, fill=X)

    # Initialize a **chat session**
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Using the available Gemini model
    chat = model.start_chat(history=[])

    def ask_gemini():
        question = entry.get()
        if not question.strip():
            return
        text_area.insert(END, f"You: {question}\n")

        try:
            response = chat.send_message(question)
            answer = response.text.strip()
            text_area.insert(END, f"chatbot: {answer}\n\n")
        except Exception as e:
            text_area.insert(END, f"Error: {str(e)}\n\n")

        entry.delete(0, END)

    Button(top, text="Ask", font=("Arial", 14), bg="lightblue", command=ask_gemini).pack(pady=5)

    top.mainloop()


# GUI setup
root = tk.Tk()
root.title("Donation Platform - Login/Register")
root.geometry("400x400")

tabControl = ttk.Notebook(root)

# Login Tab
login_tab = ttk.Frame(tabControl)
tabControl.add(login_tab, text='Login')

tk.Label(login_tab, text="Username").pack(pady=10)
login_username = tk.Entry(login_tab)
login_username.pack()

tk.Label(login_tab, text="Password").pack(pady=10)
login_password = tk.Entry(login_tab, show='*')
login_password.pack()

tk.Button(login_tab, text="Login", command=login_user).pack(pady=20)

# Register Tab
register_tab = ttk.Frame(tabControl)
tabControl.add(register_tab, text='Register')

tk.Label(register_tab, text="Name").pack(pady=5)
reg_name = tk.Entry(register_tab)
reg_name.pack()

tk.Label(register_tab, text="Email").pack(pady=5)
reg_email = tk.Entry(register_tab)
reg_email.pack()

tk.Label(register_tab, text="Username").pack(pady=5)
reg_username = tk.Entry(register_tab)
reg_username.pack()

tk.Label(register_tab, text="Password").pack(pady=5)
reg_password = tk.Entry(register_tab, show='*')
reg_password.pack()

tk.Button(register_tab, text="Register", command=register_user).pack(pady=20)

tabControl.pack(expand=1, fill='both')

root.mainloop()
#location
#
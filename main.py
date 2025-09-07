import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
from mysql.connector import Error
import datetime
import os
import csv

COLORS = {
    'bg': '#0f1419',
    'panel': '#1a1f29',
    'card': '#242937',
    'primary': '#3b82f6',
    'primary_hover': '#2563eb',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'text': '#ffffff',
    'text_dim': '#94a3b8',
    'input_bg': '#2d3342',
    'border': '#374151'
}
try:
    conn = mysql.connector.connect(
        user='root',
        host='localhost',
        password='12345',
        database='railwaymanagement',
        auth_plugin='mysql_native_password'
    )
    cur = conn.cursor(buffered=True)
    print("Database connected successfully")
except Error as e:
    messagebox.showerror("Database Error", f"Failed to connect: {e}")
    exit()
current_user = None
root = tk.Tk()
root.title('🚂 Indian Railway Management System')
root.geometry('1400x850')
root.configure(bg=COLORS['bg'])
root.resizable(False, False)
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - 700
y = (root.winfo_screenheight() // 2) - 425
root.geometry(f'1400x850+{x}+{y}')
title_font = ('Segoe UI', 28, 'bold')
heading_font = ('Segoe UI', 16, 'bold')
normal_font = ('Segoe UI', 11)
button_font = ('Segoe UI', 11, 'bold')
def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except:
        return False

def validate_time(time_str):
    try:
        datetime.datetime.strptime(time_str, '%H:%M')
        return True
    except:
        return False

def show_frame(frame):
    frame.tkraise()

def create_styled_button(parent, text, command, bg_color=None, width=15):
    if bg_color is None:
        bg_color = COLORS['primary']
    
    btn = tk.Button(parent, text=text, command=command,
                   bg=bg_color, fg=COLORS['text'],
                   font=button_font, bd=0,
                   padx=20, pady=12,
                   cursor='hand2',
                   activebackground=COLORS['primary_hover'],
                   width=width)
    def on_enter(e):
        if bg_color == COLORS['primary']:
            btn['background'] = COLORS['primary_hover']
        elif bg_color == COLORS['success']:
            btn['background'] = '#059669'
        elif bg_color == COLORS['danger']:
            btn['background'] = '#dc2626'
    
    def on_leave(e):
        btn['background'] = bg_color
    
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    
    return btn

def create_styled_entry(parent, show=None, width=30):
    entry = tk.Entry(parent, bg=COLORS['input_bg'], fg=COLORS['text'],
                    font=normal_font, bd=0, insertbackground=COLORS['text'],
                    width=width, show=show)
    entry.configure(highlightbackground=COLORS['border'], highlightthickness=1)
    return entry

def create_styled_label(parent, text, font_style=None):
    if font_style is None:
        font_style = normal_font
    return tk.Label(parent, text=text, bg=COLORS['bg'], fg=COLORS['text'], font=font_style)

def create_table(parent, columns, headings, height=15):
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Treeview',
                   background=COLORS['card'],
                   fieldbackground=COLORS['card'],
                   foreground=COLORS['text'],
                   borderwidth=0,
                   font=normal_font)
    
    style.configure('Treeview.Heading',
                   background=COLORS['primary'],
                   foreground=COLORS['text'],
                   borderwidth=0,
                   font=button_font)
    
    style.map('Treeview',
             background=[('selected', COLORS['primary'])],
             foreground=[('selected', COLORS['text'])])
    
    table_frame = tk.Frame(parent, bg=COLORS['panel'])
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=height)
    vsb = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    
    for col, head in zip(columns, headings):
        tree.heading(col, text=head)
        tree.column(col, anchor='center', width=120)
    
    tree.tag_configure('odd', background=COLORS['card'])
    tree.tag_configure('even', background=COLORS['panel'])
    
    return tree

def refresh_table(tree, rows):
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tag = 'odd' if i % 2 == 0 else 'even'
        tree.insert('', 'end', values=row, tags=(tag,))

login_frame = tk.Frame(root, bg=COLORS['bg'])
register_frame = tk.Frame(root, bg=COLORS['bg'])
client_frame = tk.Frame(root, bg=COLORS['bg'])
admin_frame = tk.Frame(root, bg=COLORS['bg'])

for frame in [login_frame, register_frame, client_frame, admin_frame]:
    frame.place(relwidth=1, relheight=1)

# LOGIN FRAME
def create_login_ui():
    for widget in login_frame.winfo_children():
        widget.destroy()
    
    container = tk.Frame(login_frame, bg=COLORS['panel'], padx=40, pady=40)
    container.place(relx=0.5, rely=0.5, anchor='center')
    
    title_label = tk.Label(container, text='🚂 Indian Railways', 
                          bg=COLORS['panel'], fg=COLORS['text'], 
                          font=('Segoe UI', 32, 'bold'))
    title_label.pack(pady=(0, 10))
    
    subtitle = tk.Label(container, text='Management System', 
                        bg=COLORS['panel'], fg=COLORS['text_dim'], 
                        font=('Segoe UI', 14))
    subtitle.pack(pady=(0, 30))
    
    form_frame = tk.Frame(container, bg=COLORS['panel'])
    form_frame.pack()
    
    tk.Label(form_frame, text='Username', bg=COLORS['panel'], 
            fg=COLORS['text_dim'], font=normal_font).grid(row=0, column=0, sticky='w', pady=5)
    username_entry = create_styled_entry(form_frame)
    username_entry.grid(row=1, column=0, pady=(0, 15))
    
    tk.Label(form_frame, text='Password', bg=COLORS['panel'], 
            fg=COLORS['text_dim'], font=normal_font).grid(row=2, column=0, sticky='w', pady=5)
    password_entry = create_styled_entry(form_frame, show='*')
    password_entry.grid(row=3, column=0, pady=(0, 25))
    
    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning('Input Required', 'Please enter both username and password')
            return
        
        try:
            cur.execute('SELECT userid, usertype, passengerid FROM users WHERE username=%s AND password=%s',
                       (username, password))
            result = cur.fetchone()
            
            if result:
                global current_user
                current_user = {
                    'userid': result[0],
                    'usertype': result[1],
                    'passengerid': result[2],
                    'username': username
                }
                login_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                history_file = 'login_history.csv'
                file_exists = os.path.isfile(history_file)
                if not file_exists:
                    with open(history_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Username', 'UserType', 'LoginTime'])
                        writer.writerow([username, result[1], login_time])
                else:
                    with open(history_file, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([username, result[1], login_time])
                
                messagebox.showinfo('Success', f'Welcome back, {username}! 🎉')
                
                if result[1] == 'client':
                    setup_client_dashboard()
                    show_frame(client_frame)
                else:
                    setup_admin_dashboard()
                    show_frame(admin_frame)
            
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
            else:
                messagebox.showerror('Login Failed', 'Invalid username or password')
        except Error as e:
            messagebox.showerror('Database Error', f'Login failed: {e}')

    login_btn = create_styled_button(form_frame, 'Login', login, width=25)
    login_btn.grid(row=4, column=0, pady=(0, 10))
    
    register_btn = create_styled_button(form_frame, 'Create Account', 
                                       lambda: show_frame(register_frame),
                                       bg_color=COLORS['success'], width=25)
    register_btn.grid(row=5, column=0)
    def exit_app():
        root.destroy()
        os._exit(0)
    exit_btn = create_styled_button(form_frame, 'Exit', exit_app, bg_color=COLORS['danger'], width=25)
    exit_btn.grid(row=6, column=0, pady=(10, 0))

# REGISTER FRAME
def create_register_ui():
    for widget in register_frame.winfo_children():
        widget.destroy()
    
    container = tk.Frame(register_frame, bg=COLORS['panel'], padx=40, pady=30)
    container.place(relx=0.5, rely=0.5, anchor='center')
    
    title_label = tk.Label(container, text='Create New Account', 
                          bg=COLORS['panel'], fg=COLORS['text'], 
                          font=('Segoe UI', 24, 'bold'))
    title_label.pack(pady=(0, 20))
    
    form_frame = tk.Frame(container, bg=COLORS['panel'])
    form_frame.pack()
    
    tk.Label(form_frame, text='Username', bg=COLORS['panel'], 
            fg=COLORS['text_dim'], font=normal_font).grid(row=0, column=0, sticky='w', pady=5)
    reg_username = create_styled_entry(form_frame)
    reg_username.grid(row=0, column=1, padx=(20, 0), pady=5)
    
    tk.Label(form_frame, text='Password', bg=COLORS['panel'], 
            fg=COLORS['text_dim'], font=normal_font).grid(row=1, column=0, sticky='w', pady=5)
    reg_password = create_styled_entry(form_frame, show='*')
    reg_password.grid(row=1, column=1, padx=(20, 0), pady=5)
    
    tk.Label(form_frame, text='Account Type', bg=COLORS['panel'], 
            fg=COLORS['text_dim'], font=normal_font).grid(row=2, column=0, sticky='w', pady=5)
    
    user_type_var = tk.StringVar(value='client')
    type_frame = tk.Frame(form_frame, bg=COLORS['panel'])
    type_frame.grid(row=2, column=1, padx=(20, 0), pady=5, sticky='w')
    
    tk.Radiobutton(type_frame, text='Client', variable=user_type_var, value='client',
                  bg=COLORS['panel'], fg=COLORS['text'], selectcolor=COLORS['panel'],
                  font=normal_font).pack(side='left', padx=(0, 20))
    tk.Radiobutton(type_frame, text='Admin', variable=user_type_var, value='admin',
                  bg=COLORS['panel'], fg=COLORS['text'], selectcolor=COLORS['panel'],
                  font=normal_font).pack(side='left')
    
    tk.Label(form_frame, text='Full Name', bg=COLORS['panel'], 
            fg=COLORS['text_dim'], font=normal_font).grid(row=3, column=0, sticky='w', pady=5)
    reg_fullname = create_styled_entry(form_frame)
    reg_fullname.grid(row=3, column=1, padx=(20, 0), pady=5)
    
    tk.Label(form_frame, text='Contact', bg=COLORS['panel'], 
            fg=COLORS['text_dim'], font=normal_font).grid(row=4, column=0, sticky='w', pady=5)
    reg_contact = create_styled_entry(form_frame)
    reg_contact.grid(row=4, column=1, padx=(20, 0), pady=5)
    
    def register():
        username = reg_username.get().strip()
        password = reg_password.get().strip()
        usertype = user_type_var.get()
        
        if not username or not password:
            messagebox.showwarning('Input Required', 'Username and password are required')
            return
        
        try:
            cur.execute('SELECT userid FROM users WHERE username=%s', (username,))
            if cur.fetchone():
                messagebox.showerror('Registration Failed', 'Username already exists')
                return
            
            passenger_id = None
            
            if usertype == 'client':
                fullname = reg_fullname.get().strip()
                contact = reg_contact.get().strip()
                
                if not fullname or not contact:
                    messagebox.showwarning('Input Required', 'Please fill in all client information')
                    return
                
                cur.execute('INSERT INTO passengers(name, contact) VALUES(%s, %s)',
                           (fullname, contact))
                passenger_id = cur.lastrowid
            
            cur.execute('INSERT INTO users(username, password, usertype, passengerid) VALUES(%s, %s, %s, %s)',
                       (username, password, usertype, passenger_id))
            conn.commit()
            
            messagebox.showinfo('Success', 'Account created successfully! 🎉')
            show_frame(login_frame)
            
            reg_username.delete(0, tk.END)
            reg_password.delete(0, tk.END)
            reg_fullname.delete(0, tk.END)
            reg_contact.delete(0, tk.END)
            
        except Error as e:
            conn.rollback()
            messagebox.showerror('Registration Failed', f'Error: {e}')
    
    button_frame = tk.Frame(container, bg=COLORS['panel'])
    button_frame.pack(pady=(30, 0))
    
    register_btn = create_styled_button(button_frame, 'Create Account', register,
                                       bg_color=COLORS['success'], width=20)
    register_btn.pack(side='left', padx=5)
    
    back_btn = create_styled_button(button_frame, 'Back to Login', 
                                   lambda: show_frame(login_frame),
                                   bg_color=COLORS['danger'], width=20)
    back_btn.pack(side='left', padx=5)

# CLIENT DASHBOARD
def setup_client_dashboard():
    for widget in client_frame.winfo_children():
        widget.destroy()
    
    header = tk.Frame(client_frame, bg=COLORS['panel'], height=80)
    header.pack(fill='x', padx=0, pady=0)
    header.pack_propagate(False)
    
    title_frame = tk.Frame(header, bg=COLORS['panel'])
    title_frame.pack(side='left', padx=30, pady=20)
    
    tk.Label(title_frame, text='🚂 Client Dashboard', 
            bg=COLORS['panel'], fg=COLORS['text'], 
            font=('Segoe UI', 20, 'bold')).pack(side='left')
    
    if current_user:
        user_label = tk.Label(header, text=f'Welcome, {current_user["username"]}! 👤',
                             bg=COLORS['panel'], fg=COLORS['text_dim'],
                             font=('Segoe UI', 12))
        user_label.pack(side='right', padx=30)
    
    nav_frame = tk.Frame(client_frame, bg=COLORS['bg'])
    nav_frame.pack(fill='x', padx=20, pady=20)
    
    def load_trains():
        try:
            cur.execute('''SELECT trid, platno, depart, depart_time, arrival, arrival_time, status 
                          FROM trains ORDER BY depart DESC, depart_time''')
            rows = cur.fetchall()
            refresh_table(train_tree, rows)
        except Error as e:
            messagebox.showerror('Error', f'Failed to load trains: {e}')
    
    def load_bookings():
        if not current_user:
            return
        try:
            cur.execute('''SELECT bookingid, trid, from_stid, to_stid, 
                          dateofdepart, timeofdepart, status, price 
                          FROM bookings 
                          WHERE passengerid=%s 
                          ORDER BY dateofdepart DESC, timeofdepart DESC''',
                       (current_user['passengerid'],))
            rows = cur.fetchall()
            refresh_table(booking_tree, rows)
        except Error as e:
            messagebox.showerror('Error', f'Failed to load bookings: {e}')
    
    def book_ticket():
        booking_window = tk.Toplevel(root)
        booking_window.title('Book New Ticket')
        booking_window.geometry('600x500')
        booking_window.configure(bg=COLORS['bg'])
        
        booking_window.transient(root)
        booking_window.grab_set()
        
        container = tk.Frame(booking_window, bg=COLORS['panel'], padx=30, pady=30)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(container, text='Book Your Journey', 
                bg=COLORS['panel'], fg=COLORS['text'],
                font=('Segoe UI', 18, 'bold')).pack(pady=(0, 20))
        
        form = tk.Frame(container, bg=COLORS['panel'])
        form.pack()
        
        tk.Label(form, text='Train ID:', bg=COLORS['panel'], 
                fg=COLORS['text_dim'], font=normal_font).grid(row=0, column=0, sticky='w', pady=10)
        train_id_entry = create_styled_entry(form, width=25)
        train_id_entry.grid(row=0, column=1, padx=(20, 0))
        
        tk.Label(form, text='Travel Date (YYYY-MM-DD):', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=1, column=0, sticky='w', pady=10)
        date_entry = create_styled_entry(form, width=25)
        date_entry.grid(row=1, column=1, padx=(20, 0))
        
        tk.Label(form, text='From Station:', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=2, column=0, sticky='w', pady=10)
        from_entry = create_styled_entry(form, width=25)
        from_entry.grid(row=2, column=1, padx=(20, 0))
        
        tk.Label(form, text='To Station:', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=3, column=0, sticky='w', pady=10)
        to_entry = create_styled_entry(form, width=25)
        to_entry.grid(row=3, column=1, padx=(20, 0))
       
        tk.Label(form, text='Departure Time:', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=4, column=0, sticky='w', pady=10)
        
        time_var = tk.StringVar(value='06:00')
        time_combo = ttk.Combobox(form, textvariable=time_var,
                                  values=['06:00', '10:00', '14:00', '18:00', '22:00'],
                                  state='readonly', width=22)
        time_combo.grid(row=4, column=1, padx=(20, 0))
        
        def confirm_booking():
            train_id = train_id_entry.get().strip()
            travel_date = date_entry.get().strip()
            from_station = from_entry.get().strip()
            to_station = to_entry.get().strip()
            dep_time = time_var.get()
            
            if not all([train_id, travel_date, from_station, to_station]):
                messagebox.showwarning('Input Required', 'Please fill all fields')
                return
            
            if not train_id.isdigit():
                messagebox.showwarning('Invalid Input', 'Train ID must be a number')
                return
            
            if not validate_date(travel_date):
                messagebox.showwarning('Invalid Date', 'Please enter date in YYYY-MM-DD format')
                return
            
            try:
                cur.execute('SELECT trid FROM trains WHERE trid=%s', (train_id,))
                if not cur.fetchone():
                    messagebox.showerror('Error', 'Train not found')
                    return
                
                cur.execute('''SELECT seatid, seatnum, class, price 
                              FROM seats WHERE trid=%s AND status='Available' LIMIT 1''', 
                           (train_id,))
                seat = cur.fetchone()
                
                if not seat:
                    messagebox.showinfo('No Seats', 'No seats available for this train')
                    return
                
                seat_id, seat_num, seat_class, price = seat
                
                cur.execute('''INSERT INTO bookings(trid, passengerid, from_stid, to_stid, 
                              dateofdepart, timeofdepart, seatnum, price, status) 
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'Confirmed')''',
                           (train_id, current_user['passengerid'], from_station, to_station,
                            travel_date, dep_time, seat_num, price))
                
                booking_id = cur.lastrowid
                
                cur.execute('UPDATE seats SET status="Booked" WHERE seatid=%s', (seat_id,))
                
                cur.execute('INSERT INTO payments(bookingid, price) VALUES(%s, %s)',
                           (booking_id, price))
                
                conn.commit()
                
                messagebox.showinfo('Success', 
                                   f'Booking confirmed! 🎉\nBooking ID: {booking_id}\n'
                                   f'Seat: {seat_num} ({seat_class})\nPrice: ₹{price}')
                booking_window.destroy()
                load_bookings()
                
            except Error as e:
                conn.rollback()
                messagebox.showerror('Booking Failed', f'Error: {e}')
        
        btn_frame = tk.Frame(container, bg=COLORS['panel'])
        btn_frame.pack(pady=(30, 0))
        
        confirm_btn = create_styled_button(btn_frame, 'Confirm Booking', confirm_booking,
                                          bg_color=COLORS['success'])
        confirm_btn.pack(side='left', padx=5)
        
        cancel_btn = create_styled_button(btn_frame, 'Cancel', booking_window.destroy,
                                         bg_color=COLORS['danger'])
        cancel_btn.pack(side='left', padx=5)
    
    def check_seat_availability():
        check_window = tk.Toplevel(root)
        check_window.title('Check Seat Availability')
        check_window.geometry('700x500')
        check_window.configure(bg=COLORS['bg'])
        
        check_window.transient(root)
        check_window.grab_set()
        
        container = tk.Frame(check_window, bg=COLORS['panel'], padx=20, pady=20)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(container, text='Check Seat Availability',
                bg=COLORS['panel'], fg=COLORS['text'],
                font=('Segoe UI', 18, 'bold')).pack(pady=(0, 20))

        input_frame = tk.Frame(container, bg=COLORS['panel'])
        input_frame.pack()
        
        tk.Label(input_frame, text='Train ID:', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=0, column=0, padx=5)
        train_entry = create_styled_entry(input_frame, width=15)
        train_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text='Date (YYYY-MM-DD):', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=0, column=2, padx=5)
        date_entry = create_styled_entry(input_frame, width=15)
        date_entry.grid(row=0, column=3, padx=5)
        
        result_tree = create_table(container, 
                                  ['class', 'available', 'total', 'price'],
                                  ['Class', 'Available', 'Total', 'Price (₹)'],
                                  height=8)
        
        def check_availability():
            train_id = train_entry.get().strip()
            check_date = date_entry.get().strip()
            
            if not train_id or not check_date:
                messagebox.showwarning('Input Required', 'Please enter both Train ID and Date')
                return
            
            if not train_id.isdigit():
                messagebox.showwarning('Invalid Input', 'Train ID must be a number')
                return
            
            if not validate_date(check_date):
                messagebox.showwarning('Invalid Date', 'Please enter date in YYYY-MM-DD format')
                return
            
            try:
                cur.execute('''SELECT class, COUNT(*), MIN(price) 
                              FROM seats WHERE trid=%s 
                              GROUP BY class''', (train_id,))
                seat_data = cur.fetchall()
                
                if not seat_data:
                    messagebox.showinfo('No Data', 'No seats found for this train')
                    return
                
                results = []
                for seat_class, total, price in seat_data:
    
                    cur.execute('''SELECT COUNT(*) FROM bookings b 
                                  JOIN seats s ON b.seatnum = s.seatnum AND b.trid = s.trid
                                  WHERE s.trid=%s AND s.class=%s 
                                  AND b.dateofdepart=%s AND b.status='Confirmed' ''',
                               (train_id, seat_class, check_date))
                    booked = cur.fetchone()[0]
                    available = total - booked
                    results.append((seat_class, available, total, price))
                
                refresh_table(result_tree, results)
                
            except Error as e:
                messagebox.showerror('Error', f'Failed to check availability: {e}')
        
        check_btn = create_styled_button(input_frame, 'Check', check_availability,
                                        bg_color=COLORS['success'])
        check_btn.grid(row=0, column=4, padx=10)
    
    def exit_app():
        root.destroy()
        os._exit(0)

    nav_buttons = [
        ('View Trains', load_trains, COLORS['primary']),
        ('Book Ticket', book_ticket, COLORS['success']),
        ('My Bookings', load_bookings, COLORS['primary']),
        ('Check Availability', check_seat_availability, COLORS['warning']),
        ('Logout', lambda: show_frame(login_frame), COLORS['danger']),
        ('Exit', exit_app, COLORS['danger'])
    ]
    
    for text, command, color in nav_buttons:
        btn = create_styled_button(nav_frame, text, command, bg_color=color, width=18)
        btn.pack(side='left', padx=5)
    
    content_frame = tk.Frame(client_frame, bg=COLORS['bg'])
    content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    tk.Label(content_frame, text='Available Trains', 
            bg=COLORS['bg'], fg=COLORS['text'],
            font=heading_font).pack(anchor='w', pady=(0, 10))
    
    train_tree = create_table(content_frame,
                             ['trid', 'platno', 'depart', 'depart_time', 'arrival', 'arrival_time', 'status'],
                             ['Train ID', 'Platform', 'Depart Date', 'Depart Time', 'Arrival Date', 'Arrival Time', 'Status'],
                             height=8)
    
    tk.Label(content_frame, text='My Bookings', 
            bg=COLORS['bg'], fg=COLORS['text'],
            font=heading_font).pack(anchor='w', pady=(20, 10))
    
    booking_tree = create_table(content_frame,
                                ['bookingid', 'trid', 'from_stid', 'to_stid', 'dateofdepart', 'timeofdepart', 'status', 'price'],
                                ['Booking ID', 'Train ID', 'From', 'To', 'Date', 'Time', 'Status', 'Price (₹)'],
                                height=8)
    
    load_trains()
    load_bookings()

# ADMIN DASHBOARD
def setup_admin_dashboard():

    for widget in admin_frame.winfo_children():
        widget.destroy()
      
    header = tk.Frame(admin_frame, bg=COLORS['panel'], height=80)
    header.pack(fill='x')
    header.pack_propagate(False)
    
    title_frame = tk.Frame(header, bg=COLORS['panel'])
    title_frame.pack(side='left', padx=30, pady=20)
    
    tk.Label(title_frame, text='⚙️ Admin Dashboard', 
            bg=COLORS['panel'], fg=COLORS['text'], 
            font=('Segoe UI', 20, 'bold')).pack(side='left')
    
    if current_user:
        user_label = tk.Label(header, text=f'Admin: {current_user["username"]} 👤',
                             bg=COLORS['panel'], fg=COLORS['text_dim'],
                             font=('Segoe UI', 12))
        user_label.pack(side='right', padx=30)
    
    nav_frame = tk.Frame(admin_frame, bg=COLORS['bg'])
    nav_frame.pack(fill='x', padx=20, pady=20)
    
    def load_all_trains():
        try:
            cur.execute('''SELECT trid, platno, status FROM trains ORDER BY trid''')
            rows = cur.fetchall()
            refresh_table(admin_train_tree, rows)
        except Error as e:
            messagebox.showerror('Error', f'Failed to load trains: {e}')
    
    def add_train():
        add_window = tk.Toplevel(root)
        add_window.title('Add New Train')
        add_window.geometry('600x550')
        add_window.configure(bg=COLORS['bg'])
        
        add_window.transient(root)
        add_window.grab_set()
        
        container = tk.Frame(add_window, bg=COLORS['panel'], padx=30, pady=30)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(container, text='Add New Train',
                bg=COLORS['panel'], fg=COLORS['text'],
                font=('Segoe UI', 18, 'bold')).pack(pady=(0, 20))
        
        form = tk.Frame(container, bg=COLORS['panel'])
        form.pack()
        
        fields = [
            ('Platform Number:', 'platform'),
            ('Departure Date (YYYY-MM-DD):', 'depart_date'),
            ('Departure Time (HH:MM):', 'depart_time'),
            ('Arrival Date (YYYY-MM-DD):', 'arrival_date'),
            ('Arrival Time (HH:MM):', 'arrival_time')
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg=COLORS['panel'],
                    fg=COLORS['text_dim'], font=normal_font).grid(row=i, column=0, sticky='w', pady=8)
            entry = create_styled_entry(form, width=25)
            entry.grid(row=i, column=1, padx=(20, 0))
            entries[key] = entry
        
        tk.Label(form, text='Status:', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=len(fields), column=0, sticky='w', pady=8)
        
        status_var = tk.StringVar(value='On Time')
        status_combo = ttk.Combobox(form, textvariable=status_var,
                                    values=['On Time', 'Delayed', 'Cancelled'],
                                    state='readonly', width=22)
        status_combo.grid(row=len(fields), column=1, padx=(20, 0))
        
        def save_train():
            try:
                platform = entries['platform'].get().strip()
                depart_date = entries['depart_date'].get().strip()
                depart_time = entries['depart_time'].get().strip()
                arrival_date = entries['arrival_date'].get().strip()
                arrival_time = entries['arrival_time'].get().strip()
                status = status_var.get()
                
                if not all([platform, depart_date, depart_time, arrival_date, arrival_time]):
                    messagebox.showwarning('Input Required', 'Please fill all fields')
                    return
                
                if not platform.isdigit():
                    messagebox.showwarning('Invalid Input', 'Platform must be a number')
                    return
                
                if not validate_date(depart_date) or not validate_date(arrival_date):
                    messagebox.showwarning('Invalid Date', 'Please enter dates in YYYY-MM-DD format')
                    return
                
                if not validate_time(depart_time) or not validate_time(arrival_time):
                    messagebox.showwarning('Invalid Time', 'Please enter times in HH:MM format')
                    return
                
                cur.execute('''INSERT INTO trains(platno, depart, depart_time, arrival, arrival_time, status) 
                              VALUES(%s, %s, %s, %s, %s, %s)''',
                           (platform, depart_date, depart_time, arrival_date, arrival_time, status))
                
                train_id = cur.lastrowid

                seat_classes = [
                    ('General', 100, 500),
                    ('Sleeper', 60, 800),
                    ('AC 3-Tier', 40, 1200),
                    ('AC 2-Tier', 30, 1800),
                    ('AC 1st', 20, 2500)
                ]
                
                for class_name, num_seats, price in seat_classes:
                    for i in range(1, num_seats + 1):
                        seat_num = f'{class_name[:2].upper()}{i:03d}'
                        cur.execute('''INSERT INTO seats(trid, seatnum, class, price, status) 
                                      VALUES(%s, %s, %s, %s, 'Available')''',
                                   (train_id, seat_num, class_name, price))
                
                conn.commit()
                
                messagebox.showinfo('Success', f'Train added successfully!\nTrain ID: {train_id}')
                add_window.destroy()
                load_all_trains()
                
            except Error as e:
                conn.rollback()
                messagebox.showerror('Error', f'Failed to add train: {e}')
        
        btn_frame = tk.Frame(container, bg=COLORS['panel'])
        btn_frame.pack(pady=(30, 0))
        
        save_btn = create_styled_button(btn_frame, 'Save Train', save_train,
                                       bg_color=COLORS['success'])
        save_btn.pack(side='left', padx=5)
        
        cancel_btn = create_styled_button(btn_frame, 'Cancel', add_window.destroy,
                                         bg_color=COLORS['danger'])
        cancel_btn.pack(side='left', padx=5)
    
    def edit_train():
        edit_window = tk.Toplevel(root)
        edit_window.title('Edit Train Status')
        edit_window.geometry('500x300')
        edit_window.configure(bg=COLORS['bg'])

        edit_window.transient(root)
        edit_window.grab_set()

        container = tk.Frame(edit_window, bg=COLORS['panel'], padx=30, pady=30)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(container, text='Update Train Status',
                bg=COLORS['panel'], fg=COLORS['text'],
                font=('Segoe UI', 18, 'bold')).pack(pady=(0, 30))

        form = tk.Frame(container, bg=COLORS['panel'])
        form.pack()

        tk.Label(form, text='Train ID:', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=0, column=0, sticky='w', pady=10)
        train_id_entry = create_styled_entry(form, width=20)
        train_id_entry.grid(row=0, column=1, padx=(20, 0))

        tk.Label(form, text='New Status:', bg=COLORS['panel'],
                fg=COLORS['text_dim'], font=normal_font).grid(row=1, column=0, sticky='w', pady=10)

        status_var = tk.StringVar(value='Running')
        status_combo = ttk.Combobox(form, textvariable=status_var,
                                    values=['Running', 'Down'],
                                    state='readonly', width=17)
        status_combo.grid(row=1, column=1, padx=(20, 0))

        def update_train():
            train_id = train_id_entry.get().strip()
            new_status = status_var.get()

            if not train_id:
                messagebox.showwarning('Input Required', 'Please enter Train ID')
                return

            if not train_id.isdigit():
                messagebox.showwarning('Invalid Input', 'Train ID must be a number')
                return

            try:
                cur.execute('UPDATE trains SET status=%s WHERE trid=%s', (new_status, train_id))

                if cur.rowcount == 0:
                    messagebox.showwarning('Not Found', 'Train ID not found')
                    return

                conn.commit()
                messagebox.showinfo('Success', f'Train {train_id} status updated to {new_status}')
                edit_window.destroy()
                load_all_trains()

            except Error as e:
                conn.rollback()
                messagebox.showerror('Error', f'Failed to update train: {e}')

        btn_frame = tk.Frame(container, bg=COLORS['panel'])
        btn_frame.pack(pady=(30, 0))

        update_btn = create_styled_button(btn_frame, 'Update', update_train,
                                         bg_color=COLORS['success'])
        update_btn.pack(side='left', padx=5)

        cancel_btn = create_styled_button(btn_frame, 'Cancel', edit_window.destroy,
                                         bg_color=COLORS['danger'])
        cancel_btn.pack(side='left', padx=5)
    
    def add_route():
        route_window = tk.Toplevel(root)
        route_window.title('Add Route')
        route_window.geometry('600x500')
        route_window.configure(bg=COLORS['bg'])

        route_window.transient(root)
        route_window.grab_set()

        container = tk.Frame(route_window, bg=COLORS['panel'], padx=30, pady=30)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(container, text='Add Route',
                bg=COLORS['panel'], fg=COLORS['text'],
                font=('Segoe UI', 18, 'bold')).pack(pady=(0, 20))

        form = tk.Frame(container, bg=COLORS['panel'])
        form.pack()

        fields = [
            ('Train ID:', 'trid'),
            ('Station Name:', 'station_name'),
            ('Stop Number:', 'stopnum'),
            ('Arrival Date (YYYY-MM-DD):', 'arrival_date'),
            ('Arrival Time (HH:MM):', 'arrival_time'),
            ('Departure Date (YYYY-MM-DD):', 'depart_date'),
            ('Departure Time (HH:MM):', 'depart_time')
        ]
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg=COLORS['panel'], fg=COLORS['text_dim'], font=normal_font).grid(row=i, column=0, sticky='w', pady=8)
            entry = create_styled_entry(form, width=25)
            entry.grid(row=i, column=1, padx=(20, 0))
            entries[key] = entry

        def save_route():
            trid = entries['trid'].get().strip()
            station_name = entries['station_name'].get().strip()
            stopnum = entries['stopnum'].get().strip()
            arrival_date = entries['arrival_date'].get().strip()
            arrival_time = entries['arrival_time'].get().strip()
            depart_date = entries['depart_date'].get().strip()
            depart_time = entries['depart_time'].get().strip()

            if not all([trid, station_name, stopnum, arrival_date, arrival_time, depart_date, depart_time]):
                messagebox.showwarning('Input Required', 'Please fill all fields')
                return
            if not trid.isdigit():
                messagebox.showwarning('Invalid Input', 'Train ID must be a number')
                return
            if not stopnum.isdigit():
                messagebox.showwarning('Invalid Input', 'Stop Number must be a number')
                return
            if not validate_date(arrival_date) or not validate_date(depart_date):
                messagebox.showwarning('Invalid Date', 'Please enter dates in YYYY-MM-DD format')
                return
            if not validate_time(arrival_time) or not validate_time(depart_time):
                messagebox.showwarning('Invalid Time', 'Please enter times in HH:MM format')
                return
            try:
                cur.execute('''INSERT INTO routes(trid, station_name, stopnum, arrival_date, arrival_time, depart_date, depart_time) VALUES(%s, %s, %s, %s, %s, %s, %s)''',
                    (trid, station_name, stopnum, arrival_date, arrival_time, depart_date, depart_time))
                conn.commit()
                messagebox.showinfo('Success', 'Route added successfully!')
                route_window.destroy()
            except Error as e:
                conn.rollback()
                messagebox.showerror('Error', f'Failed to add route: {e}')

        btn_frame = tk.Frame(container, bg=COLORS['panel'])
        btn_frame.pack(pady=(30, 0))
        save_btn = create_styled_button(btn_frame, 'Save Route', save_route, bg_color=COLORS['success'])
        save_btn.pack(side='left', padx=5)
        cancel_btn = create_styled_button(btn_frame, 'Cancel', route_window.destroy, bg_color=COLORS['danger'])
        cancel_btn.pack(side='left', padx=5)

    def view_all_bookings():
        bookings_window = tk.Toplevel(root)
        bookings_window.title('All Bookings')
        bookings_window.geometry('1200x600')
        bookings_window.configure(bg=COLORS['bg'])
        
        bookings_window.transient(root)
        
        container = tk.Frame(bookings_window, bg=COLORS['bg'], padx=20, pady=20)
        container.pack(fill='both', expand=True)
        
        tk.Label(container, text='All System Bookings',
                bg=COLORS['bg'], fg=COLORS['text'],
                font=('Segoe UI', 18, 'bold')).pack(pady=(0, 20))
        
        filter_frame = tk.Frame(container, bg=COLORS['bg'])
        filter_frame.pack(anchor='w', pady=(0, 10))

        tk.Label(filter_frame, text='Filter by Status:', bg=COLORS['bg'], fg=COLORS['text_dim'], font=normal_font).pack(side='left')
        status_var = tk.StringVar(value='All')
        status_options = ['All', 'Confirmed', 'Cancelled', 'Pending']
        status_combo = ttk.Combobox(filter_frame, textvariable=status_var, values=status_options, state='readonly', width=12)
        status_combo.pack(side='left', padx=10)

        bookings_tree = create_table(container,
                                    ['bookingid', 'trid', 'passengerid', 'from_stid', 'to_stid', 
                                     'dateofdepart', 'timeofdepart', 'status', 'price'],
                                    ['Booking ID', 'Train ID', 'Passenger ID', 'From', 'To', 
                                     'Date', 'Time', 'Status', 'Price (₹)'],
                                    height=20)

        def load_bookings_by_status():
            selected_status = status_var.get()
            try:
                if selected_status == 'All':
                    cur.execute('''SELECT bookingid, trid, passengerid, from_stid, to_stid,
                                  dateofdepart, timeofdepart, status, price
                                  FROM bookings ORDER BY bookingdate DESC''')
                else:
                    cur.execute('''SELECT bookingid, trid, passengerid, from_stid, to_stid,
                                  dateofdepart, timeofdepart, status, price
                                  FROM bookings WHERE status=%s ORDER BY bookingdate DESC''', (selected_status,))
                rows = cur.fetchall()
                refresh_table(bookings_tree, rows)
            except Error as e:
                messagebox.showerror('Error', f'Failed to load bookings: {e}')

        status_combo.bind('<<ComboboxSelected>>', lambda e: load_bookings_by_status())
        load_bookings_by_status()
    
    def exit_app():
        root.destroy()
        os._exit(0)

    nav_buttons = [
        ('View Trains', load_all_trains, COLORS['primary']),
        ('Add Train', add_train, COLORS['success']),
        ('Edit Train Status', edit_train, COLORS['warning']),
        ('Add Route', add_route, COLORS['success']),
        ('View All Bookings', view_all_bookings, COLORS['primary']),
        ('Logout', lambda: show_frame(login_frame), COLORS['danger']),
        ('Exit', exit_app, COLORS['danger'])
    ]
    for text, command, color in nav_buttons:
        btn = create_styled_button(nav_frame, text, command, bg_color=color, width=18)
        btn.pack(side='left', padx=5)
    
    content_frame = tk.Frame(admin_frame, bg=COLORS['bg'])
    content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    tk.Label(content_frame, text='Train Management',
        bg=COLORS['bg'], fg=COLORS['text'],
        font=heading_font).pack(anchor='w', pady=(0, 10))

    admin_train_tree = create_table(content_frame,
                   ['trid', 'platno', 'status'],
                   ['Train ID', 'Platform', 'Status'],
                   height=20)

    load_all_trains()

create_login_ui()
create_register_ui()

try:
    cur.execute('ALTER TABLE trains ADD COLUMN depart DATE')
    cur.execute('ALTER TABLE trains ADD COLUMN depart_time TIME')
    cur.execute('ALTER TABLE trains ADD COLUMN arrival DATE')
    cur.execute('ALTER TABLE trains ADD COLUMN arrival_time TIME')
    conn.commit()
except:
    pass  

show_frame(login_frame)

root.mainloop()

conn.close()

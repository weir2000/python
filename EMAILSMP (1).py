import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests,sys
from tkinter import simpledialog, messagebox
import requests
listbox = None

def authenticate(password, device):
    SERVER_URL = "http://severdtreotool.x10.mx/severd.php"
    try:
        response = requests.post(SERVER_URL, json={"password": password, "device": device})
        if response.status_code == 200:
            return response.json()["authenticated"]
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False

def authenticate_and_open_main_interface():
    entered_device = device_entry.get()
    password = password_entry.get()
    if entered_device:
        if authenticate(password, entered_device):
            print("ĐĂNG NHẬP THÀNH CÔNG")
            show_notification()
        else:
            print("ĐĂNG NHẬP THẤT BẠI")
            messagebox.showerror("Lỗi", "Mật khẩu hoặc tên thiết bị không đúng!")
    else:
        print("Missing device!")
        messagebox.showerror("Lỗi", "Vui lòng nhập tên thiết bị!")

def show_notification():
    notification_window = tk.Toplevel()
    notification_window.title("Thông báo")
    notification_window.geometry("500x500")
    notification_window.configure(bg='#000000')  # Set background color to black

    notification_text = """LƯU Ý:
XIN HÃY ĐỌC KỸ CÁC ĐIỀU KHOẢN CỦA BẢN THỎA THUẬN SỬ DỤNG DƯỚI ĐÂY TRƯỚC KHI SỬ DỤNG PHẦN MỀM CỦA CHÚNG TÔI. BẠN CHỈ CÓ THỂ SỬ DỤNG PHẦN MỀM KHI BẠN ĐỒNG Ý TẤT CẢ CÁC ĐIỀU KHOẢN THỎA THUẬN SỬ DỤNG NÀY.NẾU BẠN ĐỒNG Ý VỚI TẤT CẢ CÁC ĐIỀU KHOẢN CỦA BẢN THỎA THUẬN, HÃY CHỌN "Tôi đã đọc và chấp nhận các điều khoản trên” BẤM VÀO NÚT “TIẾP TỤC".
_ Không sử dụng phần mềm để tiết lộ thông tin cá nhân của người khác
_ Không sử dụng phần mềm vào mục đích thương mại
Người sử dụng nếu có hành vi vi phạm pháp luật sẽ tự chịu trách nhiệm và không liên quan đến chúng tôi .

MỌI THẮC MẮC CẦN GIẢI ĐÁP VUI LÒNG LIÊN HỆ ZALO 0773870929 """

    notification_label = tk.Label(notification_window, text=notification_text, justify="left", wraplength=380)
    notification_label.pack(padx=10, pady=10)


    accept_terms = tk.BooleanVar()


    def check_acceptance():
        if accept_terms.get():
            continue_button.config(state=tk.NORMAL)  
        else:
            continue_button.config(state=tk.DISABLED)  


    accept_checkbox = tk.Checkbutton(notification_window, text="Tôi đã đọc và chấp nhận các điều khoản trên", variable=accept_terms, command=check_acceptance)
    accept_checkbox.pack(pady=5)


    def close_notification():
        notification_window.destroy()
        password_window.destroy()


    continue_button = tk.Button(notification_window, text="Tiếp tục", command=close_notification, state=tk.DISABLED)
    continue_button.pack(pady=5)

    notification_window.mainloop()

def on_entry_click(event, entry_widget, placeholder):
    if entry_widget.get() == placeholder:
        entry_widget.delete(0, tk.END)
        entry_widget.config(fg='black')

def on_text_click(event, text_widget, placeholder):
    if text_widget.get("1.0", tk.END).strip() == placeholder:
        text_widget.delete("1.0", tk.END)
        text_widget.config(fg='black')

def on_text_focus_out(event, text_widget, placeholder):
    if not text_widget.get("1.0", tk.END).strip():
        text_widget.insert(tk.END, placeholder + '\n')
        text_widget.config(fg='#808080')

def on_entry_focus_out(event, entry_widget, placeholder):
    if not entry_widget.get().strip():
        entry_widget.insert(0, placeholder)
        entry_widget.config(fg='#808080')

def display_info(console_text, info_list):
    for info in info_list:
        console_text.insert(tk.END, f"{info}\n", "normal")

    console_text.see(tk.END)
    console_text.update_idletasks()

def show_file_selected_message(filename, console_text, entry_num_emails):
    with open(filename, 'r', encoding='utf-8') as file:
        num_emails = sum(1 for line in file)
        message = f'Có tổng {num_emails} email'
        console_text.insert(tk.END, f'{message}\n', "info")
        entry_num_emails.delete(0, tk.END)
        entry_num_emails.insert(0, str(num_emails))

def read_html_file(html_path):
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    return html_content

def display_html_content(html_content):
    entry_content.delete("1.0", tk.END)
    entry_content.insert(tk.END, html_content)

def browse_html():
    html_path = filedialog.askopenfilename(initialdir="/", title="Chọn file HTML", filetypes=(("HTML files", "*.html"), ("all files", "*.*")))
    if html_path:
        html_content = read_html_file(html_path)
        display_html_content(html_content)

def get_available_commands(text):
    available_commands = ["name", "address", "phone", "gioitinh"]
    return [cmd for cmd in available_commands if cmd.startswith(text)]

def show_command_suggestions(commands):
    listbox.delete(0, tk.END)
    for cmd in commands:
        listbox.insert(tk.END, cmd)

def on_listbox_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_command = listbox.get(selected_index[0])
        insert_command(selected_command)

def insert_command(selected_command):
    current_text = entry_content.get("1.0", tk.END).strip()
    index = current_text.find('/')
    entry_content.delete("1.0", tk.END)
    entry_content.insert("1.0", current_text[:index] + selected_command + current_text[index + 1:])

def on_entry_key(event):
    current_text = entry_content.get("1.0", tk.END).strip()
    if '/' in current_text:
        commands = get_available_commands(current_text)
        show_command_suggestions(commands)

def send_emails(accounts_file, recipient_file, subject, content, num_emails, console_text, image_path=None):
    with open(accounts_file.strip(), 'r', encoding='utf-8') as acc_file:
        accounts = [line.strip().split('|') for line in acc_file]

    with open(recipient_file.strip(), 'r', encoding='utf-8') as file:
        recipients = [line.strip().split('|') for line in file]

    num_emails_per_account = int(num_emails) // len(accounts)
    remaining_emails = int(num_emails) % len(accounts)

    info_list = []

    for i, account in enumerate(accounts):
        sender_email, password = account
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()

        try:
            session.login(sender_email, password)

            emails_to_send = num_emails_per_account
            if i < remaining_emails:
                emails_to_send += 1

            for j in range(emails_to_send):
                recipient_email, recipient_name, recipient_address, recipient_phone, recipient_gender = recipients[i * num_emails_per_account + j]

                # Thêm thẻ <br> sau mỗi dòng trong nội dung email
                content_lines = content.split('\n')
                content_with_line_breaks = '<br>'.join(content_lines)
                personalized_content = content_with_line_breaks

                msg = MIMEMultipart()
                msg.attach(MIMEText(personalized_content, 'html', 'utf-8')) # Changed to HTML
                msg['Subject'] = subject

                if image_path:
                    with open(image_path, 'rb') as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header('Content-Disposition', 'attachment', filename="image.png")
                        msg.attach(img)

                try:
                    session.sendmail(sender_email, recipient_email, msg.as_string())
                    info_list.append(f'Email {i + 1} đã gửi tin nhắn đến {recipient_email}')
                except Exception as e:
                    info_list.append(f'Gửi thất bại từ {sender_email} đến {recipient_email}. Lỗi: {str(e)}')
                finally:
                    console_text.tag_configure("info", foreground="#4CAF50")
                    display_info(console_text, info_list)
        except smtplib.SMTPAuthenticationError as e:
            info_list.append(f'Đăng nhập thất bại cho tài khoản {sender_email}. Lỗi: {str(e)}')
            display_info(console_text, info_list)
        finally:
            session.quit()

    total_sent_messages = num_emails_per_account * len(accounts) + remaining_emails
    console_text.insert(tk.END, f'Tổng số lượng tin nhắn gửi đi: {total_sent_messages}\n', "info")

def send_emails_from_gui():
    accounts_file = entry_accounts.get()
    recipient_file = entry_file.get()
    subject = entry_subject.get()
    content = entry_content.get("1.0", tk.END).strip()
    num_emails = entry_num_emails.get().strip()
    image_path = entry_image_path.get()

    send_emails(accounts_file, recipient_file, subject, content, num_emails, console_text, image_path)

def browse_file(entry_widget, file_type, placeholder, console_text, entry_num_emails):
    filename = filedialog.askopenfilename(initialdir="/", title=f"Chọn tệp tin {file_type}", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)
        show_file_selected_message(filename, console_text, entry_num_emails)
        return filename
    return ''

def browse_image():
    image_path = filedialog.askopenfilename(initialdir="/", title="Chọn hình ảnh", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("all files", "*.*")))
    if image_path:
        entry_image_path.delete(0, tk.END)
        entry_image_path.insert(0, image_path)

password_window = tk.Tk()
password_window.title("Xác thực mật khẩu")
password_window.geometry("300x150")

def on_closing():
    if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát?"):
        password_window.destroy()
        sys.exit() 

tk.Label(password_window, text="Nhập thiết bị:").grid(row=0, column=0, padx=10, pady=10)
device_entry = tk.Entry(password_window)
device_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(password_window, text="Nhập mật khẩu:").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(password_window, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(password_window, text="Xác thực", command=authenticate_and_open_main_interface).grid(row=2, column=0, columnspan=2, pady=5)
password_window.protocol("WM_DELETE_WINDOW", on_closing)
password_window.mainloop()
root = tk.Tk()
root.title("Phần Mềm Gửi Email Hàng Loạt  - SMP")
root.configure(bg='#F0F0F0')

style = ttk.Style()
style.configure("TFrame", background='#F0F0F0')
style.configure("TButton", foreground='black', background='#F0F0F0')  
style.configure("TEntry", foreground='black', background='#F0F0F0')  
style.configure("TLabel", foreground='black', background='#F0F0F0')  
frame_left = ttk.Frame(root)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

frame_right = ttk.Frame(root)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

entry_subject = ttk.Entry(frame_left, width=40)
entry_subject.grid(row=0, column=1, pady=5, padx=10, sticky='w')
entry_subject.insert(0, 'Nhập tiêu đề ở đây')
entry_subject.bind('<FocusIn>', lambda event: on_entry_click(event, entry_subject, 'Nhập tiêu đề ở đây'))
entry_subject.bind('<FocusOut>', lambda event: on_entry_focus_out(event, entry_subject, 'Nhập tiêu đề ở đây'))

entry_content = tk.Text(frame_left, height=10, width=40)
entry_content.grid(row=1, column=1, pady=5, padx=10, sticky='w')
entry_content.insert(tk.END, 'Nhập nội dung ở đây\n')
entry_content.bind('<FocusIn>', lambda event: on_text_click(event, entry_content, 'Nhập nội dung ở đây'))
entry_content.bind('<FocusOut>', lambda event: on_text_focus_out(event, entry_content, 'Nhập nội dung ở đây'))
entry_content.bind('<Key>', on_entry_key)
entry_num_emails = ttk.Entry(frame_left, width=20)
entry_num_emails.grid(row=2, column=1, pady=5, padx=10, columnspan=4, sticky='w')
entry_num_emails.insert(0, 'Số lượng email nhận')
entry_num_emails.bind('<FocusIn>', lambda event: on_entry_click(event, entry_num_emails, 'Số lượng email nhận'))
entry_num_emails.bind('<FocusOut>', lambda event: on_entry_focus_out(event, entry_num_emails, 'Số lượng email nhận'))

entry_accounts = ttk.Entry(frame_left, width=40)
entry_accounts.grid(row=3, column=1, pady=6, padx=5, sticky='w')

button_browse_accounts = ttk.Button(frame_left, text="File Email Gửi", command=lambda: browse_file(entry_accounts, "tài khoản", 'Nhập tài khoản và mật khẩu ở đây', console_text, entry_num_emails))
button_browse_accounts.grid(row=3, column=1, pady=6, padx=15, sticky='e')

entry_file = ttk.Entry(frame_left, width=40)
entry_file.grid(row=4, column=1, pady=8, padx=15, sticky='w')

button_browse = ttk.Button(frame_left, text="File Email Nhận", command=lambda: browse_file(entry_file, "địa chỉ email", 'Chọn tệp chứa địa chỉ email nhận', console_text, entry_num_emails))
button_browse.grid(row=4, column=1, pady=8, padx=15, sticky='e')
entry_image_path = ttk.Entry(frame_left, width=40)
entry_image_path.grid(row=5, column=1, pady=8, padx=15, sticky='w')
style.configure("TButton", padding=1, relief="flat", background="#F0F0F0", foreground="black", borderwidth=10, width=15)
button_browse_image = ttk.Button(frame_left, text="Chọn Hình Ảnh", command=browse_image)
button_browse_image.grid(row=5, column=1, pady=8, padx=15, sticky='e')

button_browse_html = ttk.Button(frame_left, text="Chọn HTML", command=browse_html)
button_browse_html.grid(row=8, column=1, pady=8, padx=15, sticky='w')
style.configure("TButton.browse_html.TButton", font=("Arial", 5))
button_send = ttk.Button(frame_left, text="Gửi Email", command=send_emails_from_gui)
button_send.grid(row=7, column=1, pady=10, padx=10, sticky='nsew')

console_text = tk.Text(frame_right, height=20, width=60, fg='#4CAF50', bg='#000000')
console_text.pack(expand=True, fill='both')
console_text.tag_configure("info", foreground="#4CAF50")

root.mainloop()

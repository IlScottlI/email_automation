import imaplib
import pprint
import time
import datetime
import base64
import os
import email


def read_return():

    filename = 'B680_JUNK_AUDIT.csv'

    infile = open(filename, 'r')
    data = infile.read()
    infile.close()

    arr = []

    data_split = data.splitlines()

    for item in data_split:
        item_split = item.split('|')
        if len(item_split) == 11:
            isnumber = item_split[2].strip()
            if isnumber.isnumeric() == True:
                context = {
                    'SLoc': item_split[1].split(', ')[0].strip(),
                    'Material': item_split[2].split(', ')[0].strip(),
                    'Material_Description': item_split[3].split(', ')[0].strip(),
                    'Batch': item_split[4].split(', ')[0].strip(),
                    'Unrestr': item_split[5].split(', ')[0].strip(),
                    'Blocked': item_split[6].split(', ')[0].strip(),
                    'Qual_Insp': item_split[7].split(', ')[0].strip(),
                    'Total_Value_0': item_split[8].split(', ')[0].strip(),
                    'Total_Value_1': item_split[9].split(', ')[0].strip(),
                }
                arr.append(context)
            else:
                pass
    return arr


def email_save_attachment():
    arr = []
    plusmail = 'tsdatauser.im@gmail.com'
    googlepass = 'DataMin3r1'

    # time.sleep(5)
    # Waiting 5 seconds before checking email
    email_address = plusmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        mail.login(email_address, googlepass)
        print("Logged in to: " + email_address)

        rv, mailboxes = mail.list()
        rv, data = mail.select("INBOX")
        if rv == 'OK':
            print("Processing mailbox...")
            typ, data = mail.search(None, 'ALL')
            mail_ids = data[0]
            id_list = mail_ids.split()
            print(id_list)
            for num in data[0].split():
                typ, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                # converts byte literal to string removing b''
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
            # downloading attachments
                for part in email_message.walk():
                    # this part comes from the snipped I don't understand yet...
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()
                    fileName = 'B680_JUNK_AUDIT.csv'
                    if bool(fileName):
                        filePath = os.path.join(
                            '', fileName)
                        if not os.path.isfile(filePath):
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                        subject = str(email_message).split(
                            "Subject: ", 1)[1].split("\nTo:", 1)[0]
                        print(f"{filePath}")
                        mail.store("1:*", '+FLAGS', '\\Deleted')
                        try:
                            if do_expunge:
                                # See Gmail Settings -> Forwarding and POP/IMAP -> Auto-Expunge
                                mail.expunge()  # not need if auto-expunge enabled
                        except:
                            print("Expunge was skipped.")
            mail.close()
        mail.logout()
        arr = read_return()
    except imaplib.IMAP4.error:
        print("Unable to login to: " + email_address + ". Was not verified\n")
    return arr


def connect_imap():
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    print("{0} Connecting to mailbox via IMAP...".format(
        datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
    m.login('tsdatauser.im@gmail.com', 'DataMin3r1')
    return m


def disconnect_imap(m):
    print("{0} Done. Closing connection & logging out.".format(
        datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
    m.close()
    m.logout()
    print("All Done.")
    return

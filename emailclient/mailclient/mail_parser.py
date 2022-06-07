import imaplib
import email
from datetime import datetime
from email.header import decode_header
import webbrowser
import os

from .models import *


class MailParser:
    def __int__(self):
        pass

    def save_messages(self, messages: list, user) -> None:
        num_of_messages = len(messages)

        for msg in messages:
            id_on_server = msg.pop()
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])

                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes) and encoding is not None:
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    else:
                        pass
                        # TODO: Сделать нормальное исключение
                        # raise RuntimeError("isinstance(subject, bytes) == False")

                    # decode From
                    from_email, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(from_email, bytes) and encoding is not None:
                        from_email = from_email.decode(encoding)
                    else:
                        pass
                        # TODO: Сделать нормальное исключение и отлавливать его

                    # decode To
                    to_email, encoding = decode_header(msg.get("To"))[0]
                    if isinstance(to_email, bytes) and encoding is not None:
                        to_email = to_email.decode(encoding)
                    else:
                        pass
                        # TODO: Сделать нормальное исключение и отлавливать его

                    # decode Date
                    date_str, encoding = decode_header(msg.get("Date"))[0]
                    if isinstance(date_str, bytes) and encoding is not None:
                        date_str = date_str.decode(encoding)
                    else:
                        pass
                        # TODO: Сделать нормальное исключение и отлавливать его
                    date_str = date_str.split()
                    print(f"Data str: {date_str}")
                    date_str = date_str[0: 5: 1]
                    print(f"Data str: {date_str}")
                    date_str = " ".join(date_str)
                    print(f"Data str2: {date_str}")
                    date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S")
                    print(f"Date: {date}")
                    print(f"Date type: {type(date)}")
                    # decode body
                    if not msg.is_multipart():
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        # if content_type == "text/plaint":
                        #     # print only text email parts
                        #     # TODO: Изменить вывод в консоль, а return или запись в БД
                        #
                        # if content_type == "text/html":
                        #     # if it's HTML, create a new HTML file and open  it in browser
                        #     folder_name = self._clean(subject)
                        #     if not os.path.isdir(folder_name):
                        #         os.mkdir(folder_name)
                        #         filename = "index.html"
                        #         filepath = os.path.join(folder_name, filename)
                        #         with open(filepath, "w") as f:
                        #             f.write(body)
                        #         webbrowser.open(filepath)
                        #     print("=" * 100)
                    else:
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print("text/plain")
                                # print text/plain emails and skip attachments
                                # TODO: Не распечатывать тело, а возвращать его или как-то иначе записывать в БД
                                # print(body)
                            elif "attachment" in content_disposition:
                                # skip attachment
                                pass

                    Email.objects.create(user=user, from_address=from_email, recipients=to_email, subject=subject,
                                         body=body, timestamp=date)

    # def get_messages(self, num_messages: int, dir_name: str = "INBOX") -> None:
    #     self._connect()
    #     status, messages = self._imap4_server.select(dir_name)
    #     # TODO: Удалить строчку ниже потом, возможно добавить исключение, если не удалось прочитать
    #     if status != "OK":
    #         raise Exception("get_messages, status != 'OK'")  # TODO: заменить на нормальный
    #     print(f"Status: {status}")
    #     print(f"Type {type(status)}")
    #     messages = int(messages[0])
    #     for i in range(messages, messages - num_messages, -1):
    #         # fetch the email message by ID
    #         res, msg = self._imap4_server.fetch(str(i), "(RFC822)")
    #         for response in msg:
    #             if isinstance(response, tuple):
    #                 # parse a bytes email into a message object
    #                 msg = email.message_from_bytes(response[1])
    #                 # decode the email subject
    #                 subject, encoding = decode_header(msg["Subject"])[0]
    #                 if isinstance(subject, bytes):
    #                     # if it's a bytes, decode to str
    #                     subject = subject.decode(encoding)
    #                 else:
    #                     pass
    #                     # raise RuntimeError("isinstance(subject, bytes) == False")
    #                 # decode email sender
    #                 from_email, encoding = decode_header(msg.get("From"))[0]
    #                 if isinstance(from_email, bytes):
    #                     from_email = from_email.decode(encoding)
    #                 print("Subject: ", subject)
    #                 print("From:", from_email)
    #                 # if the email message is multipart
    #                 if msg.is_multipart():
    #                     # iterate over email parts
    #                     for part in msg.walk():
    #                         # extract content type of email
    #                         content_type = part.get_content_type()
    #                         content_disposition = str(part.get("Content-Disposition"))
    #                         try:
    #                             # get the email body
    #                             body = part.get_payload(decode=True).decode()
    #                         except:
    #                             pass
    #                         if content_type == "text/plain" and "attachment" not in content_disposition:
    #                             print("text/plain")
    #                             # print text/plain emails and skip attachments
    #                             # TODO: Не распечатывать тело, а возвращать его или как-то иначе записывать в БД
    #                             # print(body)
    #                         elif "attachment" in content_disposition:
    #                             # download attachment
    #                             filename = part.get_filename()
    #                             if filename:
    #                                 folder_name = self._clean(subject)
    #                                 if not os.path.isdir(folder_name):
    #                                     # make a folder for this email (named after the subject)
    #                                     os.mkdir(folder_name)
    #                                 filepath = os.path.join(folder_name, filename)
    #                                 # download attachment and save it
    #                                 with open(filepath, "wb") as f:
    #                                     f.write(part.get_payload(decode=True))
    #                 else:
    #                     # extract content type of email
    #                     content_type = msg.get_content_type()
    #                     # get the email body
    #                     body = msg.get_payload(decode=True).decode()
    #                     if content_type == "text/plaint":
    #                         # print only text email parts
    #                         # TODO: Изменить вывод в консоль, а return или запись в БД
    #                         print(body)
    #                 if content_type == "text/html":
    #                     # if it's HTML, create a new HTML file and open  it in browser
    #                     folder_name = self._clean(subject)
    #                     if not os.path.isdir(folder_name):
    #                         os.mkdir(folder_name)
    #                     filename = "index.html"
    #                     filepath = os.path.join(folder_name, filename)
    #                     with open(filepath, "w") as f:
    #                         f.write(body)
    #                     webbrowser.open(filepath)
    #                 print("=" * 100)
    #     self._disconnect()

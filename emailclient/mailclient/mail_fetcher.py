import imaplib
import email
from email.header import decode_header
import webbrowser
import os


class MailFetcher:
    def __init__(self, user_name: str, user_password: str, imap4_server_name: str, port: int) -> None:
        self._user_name = user_name
        self._user_password = user_password
        self._imap4_server_name = imap4_server_name
        self._port = port

    def _clean(self, text: str) -> str:
        # чистый текст для создания папки
        return "".join(c if c.isalnum() else "_" for c in text)

    def _connect(self) -> None:
        self._imap4_server = imaplib.IMAP4_SSL(self._imap4_server_name, self._port)
        self._imap4_server.login(self._user_name, self._user_password)

    def _disconnect(self) -> None:
        self._imap4_server.close()
        self._imap4_server.logout()

    def get_messages(self, num_messages: int, dir_name: str = "INBOX") -> None:
        self._connect()
        status, messages = self._imap4_server.select(dir_name)
        # TODO: Удалить строчку ниже потом, возможно добавить исключение, если не удалось прочитать
        # print(f"Status: {status}")
        messages = int(messages[0])
        for i in range(messages, messages - num_messages, -1):
            # fetch the email message by ID
            print(f"I: {i}")
            res, msg = self._imap4_server.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    # TODO: Удалить то, что ниже
                    print(f"Type message: {type(msg)}")
                    print(f"Message: {msg}")
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    else:
                        pass
                        #raise RuntimeError("isinstance(subject, bytes) == False")
                    # decode email sender
                    from_email, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(from_email, bytes):
                        from_email = from_email.decode(encoding)
                    print("Subject: ", subject)
                    print("From:", from_email)
                    # if the email message is multipart
                    if msg.is_multipart():
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
                                # print text/plain emails and skip attachments
                                # TODO: Не распечатывать тело, а возвращать его или как-то иначе записывать в БД
                                print(body)
                            elif "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename()
                                if filename:
                                    folder_name = self._clean(subject)
                                    if not os.path.isdir(folder_name):
                                        # make a folder for this email (named after the subject)
                                        os.mkdir(folder_name)
                                    filepath = os.path.join(folder_name, filename)
                                    # download attachment and save it
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plaint":
                            # print only text email parts
                            # TODO: Изменить вывод в консоль, а return или запись в БД
                            print(body)
                    if content_type == "text/html":
                        # if it's HTML, create a new HTML file and open  it in browser
                        folder_name = self._clean(subject)
                        if not os.path.isdir(folder_name):
                            os.mkdir(folder_name)
                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)
                        with open(filepath, "w") as f:
                            f.write(body)
                        webbrowser.open(filepath)
                    print("=" * 100)
        self._disconnect()

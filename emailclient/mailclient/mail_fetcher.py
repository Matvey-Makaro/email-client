import imaplib


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

    def get_messages(self, first_id: int, dir_name: str = "INBOX") -> (list, int):
        self._connect()
        status, msg_num = self._imap4_server.select(dir_name)

        # TODO: Удалить строчку ниже потом, возможно добавить исключение, если не удалось прочитать
        if status != "OK":
            self._disconnect()
            raise Exception("get_messages, status != 'OK'")  # TODO: заменить на нормальный

        messages = []
        msg_num = int(msg_num[0])
        for i in range(msg_num, first_id, -1):
            try:
                # fetch the email message by ID
                res, msg = self._imap4_server.fetch(str(i), "(RFC822)")
                messages.append(msg)
            except Exception:
                pass

        self._disconnect()
        return messages, msg_num

    def is_valid_mailbox(self) -> bool:
        try:
            self._connect()
            self._imap4_server.select("INBOX")
            self._disconnect()
        except imaplib.IMAP4.error:
            return False
        return True


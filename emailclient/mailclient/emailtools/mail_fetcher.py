import poplib
import sys
import mail_config

from mail_tool import MailTool, SilentMailTool

class MailFetcher(MailTool):
    """
    fetch mail: connect, fetch headers+mails, delete mails
    """
    def __init__(self, pop_server: str, pop_user: str, pop_pswrd: str, has_top: bool = True) -> None:
        self._pop_server = pop_server
        self._pop_user = pop_user
        self._srvr_has_top = has_top
        self._pop_password = pop_pswrd
        self._save_server = None

    def connect(self):
        """
        establish POP server connection for mailbox operations
        :return:
        """

        if ':' not in self._pop_server:
            srvr, port = self._pop_server, None
        else:
            srvr, port = self._pop_server.split(':')

        timeout = mailconfig.popTimeout

        if getattr(mail_config, 'popusesSSL', False):
            # start ssl pop session, encrypted
            server = poplib.POP3_SSL(srvr, port or 995, timeout=timeout)    # default port=995
        elif getattr(mail_config, 'popusesTLS', False):
            # start tls pop session, encrypted
            server = poplib.POP3(srvr, port or 110, timeout=timeout)    # default port=110
            server.stls()   # разрешить шифрованную связь по уже установленному соединению
            server.ehlo()







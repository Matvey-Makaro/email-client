"""
################################################################################
PyMailGUI user configuration settings.

Email scripts get their server names and other email config options from
this module: change me to reflect your account names, info, and preferences.
This module also specifies some widget style preferences applied to the GUI,
as well as message Unicode encoding policy and more as of version 3.0.

This file defines the base set of available configurations, and assigns their
defaults.  All names here not starting with a "_" are configuration settings.
The term "book" here means _Programming Python, 4th Ed_, this code's origin.

See also:
1) The local textConfig.py here, for customizing PyEdit pop-ups made by
   PyMailGUI, and some settings shared by PyEdit popups and View/Write windows.

2) The account-specific examples in ../MailConfigs that extend, customize,
   and in some cases further document the base configuration settings here.

Warning: PyMailGUI won't run without most variables here: keep a backup copy!
Caveat: somewhere along the way this started using mixed case inconsistently...;
TBD: we could get some user settings from the command line too, and a configure
dialog GUI would be better, but this common module file suffices for now.

[4.0] the end of this file now has a hook for running other config files in
this module's scope, to support multiple accounts usage (e.g., GUI launcher).
################################################################################
"""
import sys  # check platform for host-dependent settings

# ===============================================================================
# (Required for load, delete) POP3 email server machine and user name.
# Always authenticates (logs in) with password in file (ahead) or GUI input.
# For SSL/TLS, the server name probably needs a ':NNN' port number appended
# to it; see the account-specific extension examples in ../MailConfigs.
# ===============================================================================

popservername = 'pop.secureserver.net'  # see ../MailConfigs for others
popusername = 'PP4E@learning-python.com'  # login name, name email fill

# ===============================================================================
# (Optional) PyMailGUI: Name of local one-line text file with your POP
# password; if empty or file cannot be read, pswd is requested when first
# connecting.  Pswd not encrypted: leave this empty on shared machines!
# PyMailCGI always asks for pswd (it runs on a possibly remote server).
# Dec2015: partly for tablets, this works in PyMailGUI again, after tweaking
# pswd input code: any absolute (r'c:\xxx') or CWD relative (r'..\xxx') path.
# ===============================================================================

poppasswdfile = r'c:\temp\pymailgui.txt'  # login: '' or invalid = ask

# ===============================================================================
# (Required for send) SMTP email server machine name.
# See Python smtpd module for a SMTP server class to run locally ('localhost').
# Note: your ISP may require that you be directly connected to their system
# (email once worked through Earthlink on dial up, but not via Comcast cable).
# ===============================================================================

smtpservername = 'smtpout.secureserver.net'  # default port 25, unless ':#'

# ===============================================================================
# (May be required for send) SMTP user/password if authenticated.
# Set user to None or '' if no authentication (login) is required, or a
# nonblank user name string to authenticate (login) with a password.
# Set pswd to either the path name of a local file holding your SMTP password,
# or an empty string (or nonexistent path) to force programs to ask for the
# password in a console or GUI.  See also related poppasswdfile's notes.
# ===============================================================================

smtpuser = None  # per your ISP, nonblank=authenticate
smtppasswdfile = ''  # login: '' or invalid = ask

# smtpuser       = popusername              # if the same for fetch/send
# smtppasswdfile = poppasswdfile            # if the same for fetch/send

# Dec2011 example: comcast network
smtpuser = 'veramark62'  # nonblank=authenticated
smtppasswdfile = ''  # '' = ask in GUI
smtpservername = 'smtp.comcast.net:587'  # explicit port# at end, else default

# ===============================================================================
# (Optional) Personal information used by PyMailGUI to fill in edit fields.
# If not set, does not fill in initial field/text values in compose windows.
# mysignature:
#    -can be a triple-quoted block, ignored if empty string
#    -auto-inserted at the end on new messages (and can be deleted manually)
# myaddress:
#    -used for initial value of "From" field if not empty
#    -use "..." for the name part if it's present and contains any
#     special characters other than 1 space
# Note that address here may differ from your POP/SMTP account user names above.
# Importers no longer try to guess From for replies (this had varying success).
# ===============================================================================

# myaddress   = 'The Book <PP4E@learning-python.com>'
# myaddress   = '"Z. Book!" <PP4E@learning-python.com>'

myaddress = 'PP4E@learning-python.com'

mysignature = ('Thanks,\n'
               '--Mark Lutz, http://learning-python.com')

# ===============================================================================
# (Required) Local file where sent messages are always saved.
# You can open and view this file with any list window's 'Open' button.
# Don't use '.' relative form if may be run from another dir (e.g., PP4E demos).
# None = disable auto-save of sent mails (the auto Bcc may suffice).
# The following gives example usages: uncomment and edit as desired.
# ===============================================================================

# In the current working dir...
# sentmailfile = r'./sentmail.txt'.replace('/', os.sep)   # portable

# In a hardcoded, platform-specific path you provide...
# if sys.platform.startwith('win'):
#     sentmailfile = r'C:\...path...\sentmail.txt'
# else:
#     sentmailfile = '/...path.../sentmail.txt'

# In a hardcoded path to this program's install folder...
# _mysourcedir = r'C:\PP4E\Internet\Email\PyMailGui\'
# sentmailfile = _mysourcedir + 'sentmail.txt'

# Or determine the install folder automatically from one of its
# source files (dirname(__file__) may suffice in some packages)...
# import mailclient.test_email_tools.wraplines, os
import os
#import mailclient.test_email_tools.wraplines
#_mysourcedir = os.path.dirname(os.path.abspath(wraplines.__file__))
#sentmailfile = os.path.join(_mysourcedir, 'sentmail.txt')

# ===============================================================================
# (Defunct) Local file where pymail once saved fetched POP mail (full text).
# PyMailGUI now instead asks for a save name in GUI with a pop-up dialog.
# Also asks for Split directory, and saves part buttons save in ./TempParts.
# ===============================================================================

# savemailfile = r'c:\temp\savemail.txt'       # not used in PyMailGUI: dialog


# ===============================================================================
# (Optional) Customize headers displayed in PyMailGUI list and view windows.
# listheaders replaces default, viewheaders extends it; both must be tuple of
# strings, or None to use default hdrs.  These should usually be unchanged.
# ===============================================================================

listheaders = ('Subject', 'From', 'Date', 'To', 'X-Mailer')
viewheaders = ('Bcc',)

# ===============================================================================
# (Optional) PyMailGUI fonts and colors for text server/file message list
# windows, message content view windows, and view-window attachment buttons.
# For fonts, use ('family', size, 'style'), where style is space-separated
# words including 'bold', 'normal', 'italic'.  For colors (bg=background and
# fg=foreground), use 'colorname' or hexstr '#RRGGBB'.  None means use defaults.
# View window font/color can also be set interactively in PyEdit's Tools menu.
# SEE ALSO:
# -The setcolor.py example in the GUI part (ch8) to select custom colors
#  (in the standalone PyMailGUI release, see pickcolor.py in ../docetc).
# -File textConfig.py: font/color/size settings here apply to PyMailGUI
#  windows only, and override those in textConfig.py (used for PyEdit popups).
# MORE FONT NOTES:
# -listfont => use a *fixed-width* (monospace) family for best column alignment
# -viewfont => any font works, but fixed-width retains original message spacing
# -fixed-width families include 'courier', 'consolas', and 'lucinda console'
# -see tkinter's font.families() for a list of Tk-supported font families
# -note: some fonts may not be fixed-width across all platforms (e.g., Linux)
# ===============================================================================

# list windows
listbg = '#f1fdfe'  # None, or 'sienna', 'indianred'...
listfg = 'black'  # Tk color name or '#RRGGBB'
listfont = ('courier', 10, 'bold')  # None, ('courier', 12, 'bold italic')

# view windows
viewbg = 'cornsilk'  # or 'wheat', 'light blue', '#dbbedc'...
viewfg = 'black'  # or 'white' for dark backgrounds
viewfont = ('courier', 10, 'normal')  # None, ('arial' 12, 'bold')
viewheight = 18  # max lines for height when opened (20?)
viewheightmin = 10  # [4.0] min lines for height when opened

# Oct14: larger/darker font
viewfont = ('courier', 12, 'bold')

# part buttons
partfg = None  # colors of view-window part row buttons
partbg = None

# example Tk color names: aquamarine paleturquoise powderblue goldenrod burgundy...
# listbg = listfg = listfont = None
# viewbg = viewfg = viewfont = viewheight = None      # None = use defaults
# partbg = partfg = None


# ===============================================================================
# (Optional) Column at which mail's original text should be wrapped for view,
# reply, and forward.  Wraps at first delimiter to left of this position.
# Composed text is not auto-wrapped: user or recipient's mail tool must wrap
# new text if desired.  To disable wrapping, set this to a high value (1024?).
# ===============================================================================

wrapsz = 90  # wrap at or before this column in view windows

# ===============================================================================
# (Optional) Control how PyMailGUI opens mail parts in the GUI.
# Applies to view window Split actions and attachment quick-access buttons.
# PyMailGUI auto-opens only mail parts of generally-safe and known types.
# If not okayToOpenParts, quick-access part buttons will not appear in
# the GUI, and Split saves parts in a directory but does not open them.
# verifyPartOpens is used by both Split action and quick-access buttons;
# if False, all known-type parts open automatically on Split and clicks.
# verifyHTMLTextOpen is used by web browser open of HTML main text part.
# [4.0] splitOpensAll can also be used to disable Split auto-opens
# after saves, subject to both okayToOpenParts and verifyPartOpens.
# ===============================================================================

okayToOpenParts = True  # open any parts/attachments at all?
verifyPartOpens = False  # ask permission before opening each part?
verifyHTMLTextOpen = False  # if main text part is HTML, ask before open?
splitOpensAll = True  # [4.0] Split opens parts after saving them?

# ===============================================================================
# (Optional) The maximum number of quick-access mail part buttons to show
# in the middle of view windows.  After this many, a "..." button will be
# displayed, which runs the "Split" action to extract additional parts.
# Caveat: the window can grow wide if part button names are long (TBD).
# ===============================================================================

maxPartButtons = 8  # how many part buttons in view windows

# *** PyMailGUI 3.0 ADDITIONS FOLLOW ***

# ===============================================================================
# (Required, for fetch) The Unicode encoding used to decode fetched full message
# bytes, and to encode and decode message text stored in text-mode save files.
# See the book's Chapter 13 for details: this is a limited and temporary approach
# to Unicode encodings until a new bytes-friendly email package parser is shipped
# which can handle Unicode encodings more accurately on a message-level basis.
# Note: 'latin1' (an 8-bit encoding which is a superset of 7-bit ascii) was
# required to decode messages in some old email save files I had, not 'utf8'.
# ===============================================================================

fetchEncoding = 'latin-1'  # how to decode and store full message text (ascii?)

# ===============================================================================
# (Optional, for send) Unicode encodings for composed mail's main text plus all
# text attachments.  Set these to None to be prompted for encodings on mail send;
# else uses values here across entire session.  Default='latin-1' if GUI Cancel.
# IN ALL CASE, falls back on UTF-8 if your encoding setting or input does not
# work for the text being sent (e.g., ascii chosen for reply to non-ascii text,
# or non-ascii attachments).  The email package is pickier than Python about
# names: latin-1 is known (uses qp MIME), but latin1 isn't (uses base64 MIME).
# Set these to sys.getdefaultencoding() result to choose the platform default.
# Encodings of text parts of _fetched_ email are automatic via message headers.
# ===============================================================================

mainTextEncoding = 'ascii'  # main mail body text part sent (None=ask)
attachmentTextEncoding = 'ascii'  # all text part attachments sent (utf-8, latin-1)

# ===============================================================================
# (Optional, for send) Set this to a Unicode encoding name to be applied to
# non-ASCII headers, as well as non-ASCII names in email addresses in headers,
# in composed messages when they are sent.  None means use the UTF-8 default,
# which should work for most use cases.  Email names that fail to decode are
# dropped (the address part is used).  Note that header decoding is performed
# automatically for _display_, according to header content, not user settings.
# ===============================================================================

headersEncodeTo = None  # how to encode non-ASCII headers sent (None=UTF-8)

# ===============================================================================
# (Optional) Select text, HTML, or both versions of the help documentation.
# Always shows one or the other: displays HTML if both of these are turned off.
# New: see also showStandaloneHelp below, to control standalone-release help.
# ===============================================================================

showHelpAsText = True  # scrolled text, with button for opening source files
showHelpAsHTML = True  # HTML in a web browser, without source file links

# ===============================================================================
# (Optional) If True, do NOT show a selected HTML text message part in a PyEdit
# popup too, if it is being displayed in a web browser.  If False show both, to
# see Unicode encoding name and effect in a  text widget (browser may not know).
# ===============================================================================

skipTextOnHtmlPart = False  # do not show html part in PyEdit popup too

# ===============================================================================
# (Optional) The maximum number of mail headers or messages that will be
# downloaded on each load request.  Given this setting N, PyMailGUI fetches at
# most N of the most-recently arrived mails.  Older mails outside this set are
# not fetched from the server, but are displayed as empty/dummy emails.  If this
# is assigned to None (or 0), loads will have no such limit.  Use this name if
# you have very many mails in your inbox, and your Internet or mail server
# speed makes full loads too slow to be practical.  PyMailGUI also loads only
# newly-arrived headers, but this setting is independent of that feature.
# ===============================================================================

fetchlimit = 50  # maximum number headers/emails to fetch on loads

# ===============================================================================
# (Optional) Initial width and height of mail index lists (chars x lines).
# Just a convenience, as the window can be resized/expanded freely once opened.
# ===============================================================================

listWidth = None  # None = use default 74
listHeight = None  # None = use default 15  (see also viewheight)

# ===============================================================================
# (Optional, for reply) If True, the Reply operation prefills the reply's Cc
# with all original mail recipients, after removing duplicates and the new sender.
# If False, no CC prefill occurs, and the reply is configured to reply to the
# original sender only.  The Cc line may always be edited later, in either case.
# ===============================================================================

repliesCopyToAll = True  # True=reply to sender + all recipients, else sender

# *** Dec2015+ ADDITIONS FOLLOW (not in PP4E book) ***

# ===============================================================================
# New settings for toggling SSL and TLS/SSL support in POP and SMTP servers.
# These are only "on" if they are both assigned and True, and "off" otherwise.
# The SSL setting takes priority over TLS if both are "on", and plain non-SSL
# mode is used if both are "off".  You may also need to add a port number to
# the end of your POP or SMTP server name string: 'pop.secureserver.net:995'.
# More details: http://learning-python.com/pymailgui/UserGuide.html#SSL,
# and see the config-file examples in the top-level launcher's MailConfigs.
# ===============================================================================

popusesSSL  = True           # secure with SSL?
popusesTLS  = False           # secure with TLS/SSL?

smtpusesSSL = True           # secure with SSL?
smtpusesTLS = False           # secure with TLS/SSL?


# ===============================================================================
# Assorted behavior configurations: new help display, more GUI color options.
# ===============================================================================

showStandaloneHelp = True  # help bar: standalone release html in browser?

helpfg = helpbg = None  # server list window's help bar colors, None=dflt

ctrlfg = ctrlbg = None  # view window's action button colors, None=dflt

# ===============================================================================
# May2016: As of Python 3.5, socket.sendall() used by smtplib now applies a
# timeout to total operations (e.g., a full email content send), not to each
# partial data transfer performed during an operation.  Both for this and
# general usage, PyMailGUI's smtp timeout was increased from 20 to 120 secs
# for large emails on slow smtp servers, and moved here for easy adjustment.
# poplib (for fetches) reads by lines and is not impacted by the Python 3.5
# change, but its timeout was increased too for robustness.  Without timeouts,
# PymailGUI cannot be closed in the GUI if any server transaction hangs.
# ===============================================================================

smtpTimeout = 120  # total seconds for send transactions
popTimeout = smtpTimeout  # total seconds for fetch transactions

# ===============================================================================
# [4.0] Allow header display/entry field fonts to be configured; defaults may
# be too small for some platforms and users.  Use ('family', size, 'style') for
# font, where style is space-separated words including 'bold', 'normal' (which
# is the non-bold default), and 'italic'.  None means use Tk/tkinter default.
# Unlike the mail's text (initialized to "viewfont" above), there is no way to
# set this font in the GUI itself (mail text has a menu option in its Tools).
# ===============================================================================

headerfont = ('arial', 14, 'bold')
headerfont = ('consolas', 15)
headerfont = None  # last setting wins, None=default

# ===============================================================================
# [4.0] Specify number of days to retain files in the temporary parts save
# folder, TempParts.  Email parts are saved there when selected for viewing,
# and auto-cleaned when PyMailGUI starts up.  If you prefer to retain all
# temporary parts, set this to None to disable auto-clean.  These files can
# accumulate and consume space, and are not used except for mail views.
# Note that this setting is not account-specific: there is just one TempParts.
# ===============================================================================

daysToRetainTempParts = 30  # 1=one day, 7=one week, None=turn off auto-clean

# ===============================================================================
# [4.0] Declare the file types, via their filename extensions, that PyMailGUI
# is allowed to open for email parts coded as "application".  These parts will
# be opened as if clicked in a file-explorer GUI, and rely on program/app
# associations on your computer.  A file will fail to open if no program/app is
# associated to open it, but others automatically open handler programs (e.g.,
# parts ending in ".xls" may open in Excel if it is installed on your device).
#
# Opening is still subject to the approval settings and prompts configured
# elsewhere in this file (okayToOpenParts, verifyPartOpens, and splitOpensAll).
# Use all-lowercase extensions in this list; message part names are mapped
# to lowercase before checking for matches to the list's items.  This setting
# applies to main MIME type "application" only; "text" types (including HTML),
# "image", "audio", and "video" are opened with more specialized techniques.
# This could use MIME subtype instead of extension, but the latter is absolute.
#
# CAUTION: do not add extensions of filetypes that may contain macros or pose
# other security concerns, unless you are willing to take the risk of opening
# their content.  Excel types with macros such as ".xlsm" and ".xlsb", for
# example, may contain macros run when opened; if you add their extensions
# here, be sure to click or Split+open such parts from trusted sources only.
# Even ".zip" files can be malicious in some unzip programs: open with care!
# ===============================================================================

clickablePartTypes = [  # app-part types to open, *all lowercase*
    '.doc', '.docx',  # 3.0: + word and excel 'x' types
    '.xls', '.xlsx',  # but not xlsb/xlsm unless trusted: macros
    '.ppt', '.pptx',  # [4.0]: + power point types
    '.pdf',  # pdf opens in adobe, web browser, etc.
    '.zip', '.tar',  # but open zips from trusted sources only
    '.wmv',  # [4.0]: allow uppercase in parts
    '.odt', '.ods', '.odp'  # [4.0]: + open office native types
]


# see also splitOpensAll and viewheightmin above, both added in 4.0

# ===============================================================================
# --END USER SETTINGS--
# ===============================================================================


################################################################################
# [4.0] Hook to run external per-account settings file - see GUI launcher
################################################################################

def runAcctFileHook():
    """
    If given in command-line arg, run account file's code to customize defaults.
    Coded as a function to avoid adding any of its local names to the mailconfig
    module's scope: globals() is the enclosing module scope.  The  alternative
    is using gross "_x" names or cleaning up sys.modules['mailconfig']._dict__.
    """
    import sys, os, traceback
    for (ix, arg) in enumerate(sys.argv):
        if arg.startswith('-mailconfig'):
            acctfilepath = arg.split('=')[1]
            acctfiledir = os.path.dirname(acctfilepath)

            savedir = os.getcwd()
            os.chdir(acctfiledir)  # cwd for other-file exec's, etc.
            sys.path.insert(0, acctfiledir)  # path for other-file imports?

            try:
                # run the account file in this module's scope: any name
                # assignments overwrite the default settings here/above;

                acctcode = open(acctfilepath).read()  # default Unicode encoding
                exec(acctcode, globals())  # in enclosing mod scope

            except Exception as Why:
                # popup error with exception details and exit now;
                # there is no GUI yet, so make and hide a dummy root

                from tkinter import Tk  # '*' not allowed in def
                from tkinter.messagebox import showerror
                from io import StringIO
                buffer = StringIO()
                print('Error in config file...\n', file=buffer)
                traceback.print_exc(file=buffer)  # or use limit=-1 in 3.5+?

                root = Tk()  # no GUI yet: dummy root
                root.iconify()
                showerror('PyMailGUI Launcher Error', buffer.getvalue())
                sys.exit(1)  # fatal errors: can't continue

            del sys.path[0]  # restore my cwd and import path
            os.chdir(savedir)
            del sys.argv[ix]  # remove from consideration elsewhere
            break  # end the import of this file


runAcctFileHook()

# though irrelevant in offline mode (imapfetch, save files)
print('servers: %s, %s' % (popservername, smtpservername))  # user: mailtools

# back to PyMailGui.py importer of this file...

# -*- coding: utf-8 -*-

# Erstellen komplexer Emails
# Senden und Empfangen nur in reinem ASCII-Code (keine Binaerdaten)
# Sonderzeichen ausserhalb 7Bit ASCII Standard auch problematisch
# Abhilfe:
    # MIME-Standard (Multipurpose Internet Mail Extension)
    # Kann Sonderzeichen und Binaerdaten kodieren
    # Groesse der Datenuebertragung steigt
    # MIME definiert verschiedene Dateitypen und legt Syntax fest,
    # mit der Dateianhaenge einem bestimmten Typ zugeordnet werden
    # Leichtere Verabeitung beim Empfaenger

# Die Klasse message FROM email.message == Basisklasse neue Email
"""
from email.message import Message
msg = Message()
msg.set_payload("Dies ist meine selbst erstellte E-Mail.")
msg["Subject"] = "Hallo Welt"
msg["From"] = "Me <Skadi76@hotmail.de>"
msg["To"] = "Me2 <Gyula.Orosz.DE@gmail.com>"
print(msg.as_string())
"""

#Subject: Hallo Welt
#From: Donald Duck <don@ld.de>
#To: Onkel Dagobert <d@gobert.de>
#Dies ist meine selbst erstellte E-Mail.

"""
# Mit Anhaengen
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

msg = MIMEMultipart()
msg["Subject"] = "Hallo Welt"
msg["From"] = "Me <Skadi76@hotmail.de>"
msg["To"] = "Me2 <Gyula.Orosz.DE@gmail.com>"

text = MIMEText("Dies ist meine selbst erstellte E-Mail.")
msg.attach(text)

f = open("hdr3.jpg", "rb")
bild = MIMEImage(f.read())
f.close()
msg.attach(bild)
print(msg.as_string())
"""
# email.mime.application.MIMEApplication für ausführbare Programme
# email.mime.audio.MIMEAudio für Sounddateien
# email.mime.image.MIMEImage für Grafikdateien
# email.mime.message.MIMEMessage für Message-Instanzen
# email.mime.image.MIMEText für reinen Text
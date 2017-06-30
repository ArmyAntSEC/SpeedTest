#!/usr/bin/python
import smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import time

msg = MIMEMultipart()

msg['Subject'] = "Hastighetsrapport [" + time.strftime("%Y-%m-%dT%H:%M:%S") + "]"
msg['From'] = "daniel@armyr.se"
msg['To'] = "postmaster@armyr.se"

text = MIMEText("Hastighetsrapport")
msg.attach( text )

img = open( "image.png", 'rb').read()
image = MIMEImage( img, name="image.png" )
msg.attach( image )

s = smtplib.SMTP('smtp.tre.se')
s.set_debuglevel(False)
s.sendmail( 'daniel@armyr.se', 'postmaster@armyr.se', msg.as_string() )
s.quit
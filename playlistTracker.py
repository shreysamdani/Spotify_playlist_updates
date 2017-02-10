
import os
import codecs
import sys
import time
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

























def log(str):
    #print('[{}] {}'.format(time.strftime('%I:%M:%S'), str).encode(sys.stdout.encoding, errors='replace'))
    sys.stdout.buffer.write('[{}] {}\n'.format(time.strftime('%I:%M:%S'), str).encode(sys.stdout.encoding, errors='replace'))
    sys.stdout.flush()

#remove old files and prep to check differences

if os.path.isfile('/Users/shreysamdani/Desktop/spotify/playlists0.txt'):
	os.remove('/Users/shreysamdani/Desktop/spotify/playlists0.txt')
	log('Removed file: playlists0.txt')

if os.path.isfile('/Users/shreysamdani/Desktop/spotify/differences.csv'):
	os.remove('/Users/shreysamdani/Desktop/spotify/differences.csv')
	log('Removed file: differences.csv')

if os.path.isfile('/Users/shreysamdani/Desktop/spotify/playlists.txt'):
	os.rename('/Users/shreysamdani/Desktop/spotify/playlists.txt','/Users/shreysamdani/Desktop/spotify/playlists0.txt')
	log('Renamed file: playlists.txt to playlists0.txt')
else:
	log('Error: No playlists.txt file to compare to.')	
	exit()

os.system('/Library/Frameworks/Python.framework/Versions/3.5/bin/python3 /Users/shreysamdani/Desktop/spotify/spotify-backup.py /Users/shreysamdani/Desktop/spotify/playlists.txt')

#open files and write the differences file

with codecs.open('/Users/shreysamdani/Desktop/spotify/playlists0.txt', "r", "utf-8") as old:
	old1 = set()
	for x in old:
		old1.add(x.strip())

with codecs.open('/Users/shreysamdani/Desktop/spotify/playlists.txt', "r", "utf-8") as new, open('/Users/shreysamdani/Desktop/spotify/differences.txt','w+') as differences:
    differences.writelines(x for x in new if x.strip() not in old1)

log('Wrote file: differences.txt')

os.rename('/Users/shreysamdani/Desktop/spotify/differences.txt','/Users/shreysamdani/Desktop/spotify/differences.csv')

log('Renamed file: differences.txt to differences.csv')

#email the differences file

emailfrom = ""
emailto = ""
fileToSend = ''
username = ""
password = ""

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "spotify updates"
msg.preamble = ""

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)
fp = open(fileToSend)

attachment = MIMEText(fp.read(), _subtype=subtype)
fp.close()

attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()

log('Sent email with ' + fileToSend + ' as attachment')    






















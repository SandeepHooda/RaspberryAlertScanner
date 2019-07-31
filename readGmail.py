#!/usr/bin/python
import poplib
import email
from base64 import b64decode
import requests
import time
pop3_server = 'pop.gmail.com'
pop3_port = '995'
username = 'foscamnotificationsandeep@gmail.com'
password = 'mkvzopwhygniskdj'



def decode_header(header):
    decoded_bytes, charset = email.header.decode_header(header)[0]
    if charset is None:
        return str(decoded_bytes)
    else:
        return decoded_bytes.decode(charset)

def readEmail():
 connection = poplib.POP3_SSL(pop3_server, pop3_port)
 connection.user(username)
 connection.pass_(password)
 pop3info = connection.stat() #access mailbox status
 numMessages = pop3info[0] #toral email
 
 humanDetected = False;
 for i in range(numMessages):
    raw_email  = b"\n".join(connection.retr(i+1)[1])
    parsed_email = email.message_from_bytes(raw_email)
    print('=========== email #%i ============' % i)
    print('From:', parsed_email['From'])
    print('To:', parsed_email['To'])
    print('Date:', parsed_email['Date'])
    print('Subject:', decode_header(parsed_email['Subject']))
    emailSubject = decode_header(parsed_email['Subject'])
    if ('D3D cam1' == emailSubject):
       #print("making a call")
       #requests.get("http://sanhoo-home-security.appspot.com/HumanDetected?deviceID=3")
       humanDetected  = True;
    for part in parsed_email.walk():
        if part.is_multipart():
            # maybe need also parse all subparts
            continue
        elif part.get_content_maintype() == 'text':
            text = part.get_payload(decode=True).decode(part.get_content_charset())
            print('Text:\n', text)
        elif part.get_content_maintype() == 'application' and part.get_content_disposition() == 'attachment':
            name = decode_header(part.get_filename())
            body = part.get_payload(decode=True)
            size = len(body)
            print('Attachment: "{}", size: {} bytes, starts with: "{}"'.format(name, size, body[:50]))
        else:
            print('Unknown part:', part.get_content_type())
    print('======== email #%i ended =========' % i)

 if (humanDetected):
    print("making a call")
    requests.get("http://sanhoo-home-security.appspot.com/HumanDetected?deviceID=3")
 connection.quit()

while(True):
    #try:
        print("read email")
        readEmail()
        time.sleep(10)
    #except:
        #print("error while reading email")

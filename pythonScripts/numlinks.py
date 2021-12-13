import email
import email.policy
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse


easy_ham_names = []
easy_ham_emails = []


for root, dirs, files in os.walk("C:\\Users\\jkaru\\Documents\\CSCE489\\FinalProject\\datasets", topdown=False):
    for name in files:
        f = open(os.path.join(root, name), 'r')
        easy_ham_names.append(name)
        b = email.message_from_string(f.read())


        if b.is_multipart():
            temp_str = ""
            for payload in b.get_payload():
                temp_str += str(payload)
            easy_ham_emails.append(temp_str)
        else:
            easy_ham_emails.append(str(b.get_payload()))
        f.close()

f = open("C:\\Users\\jkaru\\Documents\\CSCE489\\FinalProject\\numlinks.csv", 'w')
for i in range(len(easy_ham_emails)):
    soup = BeautifulSoup(easy_ham_emails[i])
    a_tags = soup.find_all("a", href=True) 
    f.write(easy_ham_names[i] + "," + str(len(a_tags)) + "\n")
f.close()
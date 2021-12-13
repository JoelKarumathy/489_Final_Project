import email
import email.policy
import os
from bs4 import BeautifulSoup


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


f = open("C:\\Users\\jkaru\\Documents\\CSCE489\\FinalProject\\urlImage.csv", 'w')
for i in range(len(easy_ham_emails)):
    soup = BeautifulSoup(easy_ham_emails[i])
    img_tags = soup.find_all("img", src=True)
    flag = False
    for image in img_tags:
        if "http://" in image['src'] or "https://" in image['src']:
            flag = True
    
    if flag:
        f.write(easy_ham_names[i] + ',' + "1\n")
    else:
        f.write(easy_ham_names[i] + ',' + "0\n")

f.close()
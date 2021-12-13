from urllib.parse import urlparse
import email
import email.policy
import os
import re
from tldextract import extract
from bs4 import BeautifulSoup

easy_ham_names = []
easy_ham_emails = []

regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

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

f = open("C:\\Users\\jkaru\\Documents\\CSCE489\\FinalProject\\nonModalDomain.csv", 'w')
for i in range(len(easy_ham_emails)):
    urls = re.findall(regex, easy_ham_emails[i])
    domains = dict()
    for url in urls:
        if "http://" in url or "https://" in url:
            inner_tag_url = url
            if url[:2] == "3D":
                inner_tag_url = (url[2:])[1:-1]

            tsd, td, tsu = extract(inner_tag_url) # prints abc, hostname, com

            domains[td] = domains.get(td, 0) + 1
    
    soup = BeautifulSoup(easy_ham_emails[i])
    a_tags = soup.find_all("a", href=True)
    flag = False 
    for tag in a_tags:
        if "link" in tag.text.strip() or "click" in tag.text.strip() or "here" in tag.text.strip() and tag["href"] != '':
            
            urls = re.findall(regex, tag["href"])

            for url in urls:
                if "http://" in url or "https://" in url:
                    inner_tag_url = url
                    if url[:2] == "3D":
                        inner_tag_url = (url[2:])[1:-1]

                    tsd, td, tsu = extract(inner_tag_url)

                    max_key = max(domains, key=domains.get)
                    if td != max_key:
                        flag = True

    if flag:
        f.write(easy_ham_names[i] + ',' + "1\n")
    else:
        f.write(easy_ham_names[i] + ',' + "0\n")

f.close()
                        

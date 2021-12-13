import email
import email.policy
import os
import magic


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

f = open("C:\\Users\\jkaru\\Documents\\CSCE489\\FinalProject\\htmlEmails.csv", 'w')
for i in range(len(easy_ham_emails)):
        if "</html>" in easy_ham_emails[i] or "</HTML>" in easy_ham_emails[i] or "<HTML>" in easy_ham_emails[i] or "<html>" in easy_ham_emails[i]:
            f.write(easy_ham_names[i] + "," + "1\n")
        else:
            f.write(easy_ham_names[i] + "," + "0\n")
f.close()

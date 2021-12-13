import email
import email.policy
import os
import re
import whois
from email import utils
import datetime
import pytz


import time
import concurrent.futures as futures


def timeout(timelimit):
    def decorator(func):
        def decorated(*args, **kwargs):
            with futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timelimit)
                except futures.TimeoutError:
                    print('Timedout!')
                    raise TimeoutError from None
                else:
                    pass
                executor._threads.clear()
                futures.thread._threads_queues.clear()
                return result
        return decorated
    return decorator


@timeout(1)
def test(url):
    flags = 0
    flags = flags | whois.NICClient.WHOIS_QUICK
    w = whois.whois(url, flags=flags)
    return w

easy_ham_names = []
easy_ham_emails = []
easy_ham_dates = []

regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

for root, dirs, files in os.walk("C:\\Users\\jkaru\\Documents\\CSCE489\\FinalProject\\datasets", topdown=False):
    for name in files:
        f = open(os.path.join(root, name), 'r')
        easy_ham_names.append(name)
        b = email.message_from_string(f.read())

        datestring = b['date']
        datetime_obj = utils.parsedate_to_datetime(datestring)
        easy_ham_dates.append(datetime_obj)

        if b.is_multipart():
            temp_str = ""
            for payload in b.get_payload():
                temp_str += str(payload)
            easy_ham_emails.append(temp_str)
        else:
            easy_ham_emails.append(str(b.get_payload()))
        f.close()

easy_ham_emails = easy_ham_emails[-250:]
easy_ham_names = easy_ham_names[-250:]
easy_ham_dates = easy_ham_dates[-250:]

f = open("C:\\Users\\jkaru\\Documents\\CSCE489\\FinalProject\\domainAge.csv", 'w')
for i in range(len(easy_ham_emails)):
    urls = re.findall(regex, easy_ham_emails[i])
    flag = False
    print(easy_ham_names[i])
    for url in urls:
        if "http://" in url or "https://" in url:
            try:
                try:
                    w = test(url)
                    if w["creation_date"] is not None:
                        if type(w["creation_date"]) is list:
                            creation_date = (w["creation_date"][0])
                        else:
                            creation_date = (w["creation_date"])

                        if isinstance(creation_date, datetime.date):
                            if abs((easy_ham_dates[i].replace(tzinfo=pytz.UTC) - creation_date.replace(tzinfo=pytz.UTC)).days) <= 60:
                                flag = True
                except TimeoutError:
                    continue
                                              
            except whois.parser.PywhoisError:
                continue
            except KeyError:
                continue

    if flag:
        f.write(easy_ham_names[i] + ',' + "1\n")
    else:
        f.write(easy_ham_names[i] + ',' + "0\n")
f.close()        



    
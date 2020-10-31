from collections import Counter
import random, numpy as np

class Error(Exception):
    """Base class for other exceptions"""
    pass
class BadLastPair(Error):
    """Retry, bad random generator (last combination happens to be the same person for giving and receiving"""
    pass


class SecretSanta:
    def __init__(self, emailDict):
        self.sender = emailDict
        self.receive = emailDict.copy()

        self.chosen_list = {}

    def grab_pair(self, name):        
        l = list(self.receive.items())
        while name not in self.chosen_list.keys():
            pop_num = int(random.random() * len(l))
            choice = l[pop_num]
            #
            same_name = name[0] == choice[0]
            already_given = choice in self.chosen_list.values()
            if not same_name and not already_given:
                self.chosen_list[name] = choice 
                l.pop(pop_num)
                
            elif len(self.receive) == 1 and same_name:
                raise BadLastPair

    def generate(self):
        try:
            for name in self.sender.items():
                self.grab_pair(name)
                
        except BadLastPair:
            print('Retry, bad random generation (last combination: same person for giving and receiving')



    def duplicated(self):
        key_count = Counter([name[0] for name in self.chosen_list.keys()]).values()
        val_count = Counter([name[0] for name in self.chosen_list.values()]).values()

        for (i1, i2) in zip(key_count, val_count):
            if i1 != 1 or i2 != 1:
                return True
        return False
        

    def send_email(self, send, to):
        import smtplib

        sender_email = "email"  # Enter your own address
        receiver_email = send[1]  # Enter receiver address
        # 
        password = "password"


        message = """\
        Subject: Secret Santa! 

        {}, you have gotten {} for the secret santa!

        Remember the 10 pound limit!
        """.format(send[0], to[0])

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(sender_email, password)
        s.sendmail(sender_email, receiver_email, message)
        s.quit()


names_and_emails = {'Name':'Email',
        'Name':'Email'}


santa = SecretSanta(names_and_emails)
santa.generate()
if not santa.duplicated():
    for item in santa.chosen_list.items():
        santa.send_email(item[0], item[1])
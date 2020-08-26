import smtplib
import login_webscrape



class Email_send:
    def __init__(self, emails):
        self.emails = emails
        self.server = self.init_server()

    def init_server(self):
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login('youremail@gmail.com', 'yourpassword') #email, password

        return smtpserver

#My purpose was to automate weekly projections for my job. Hence most of the naming convention
    def run(self):
        total = self.get_total()
        formatted_message = self.format_message(total)
        for email in self.emails:
            self.send_email(email, formatted_message)
        return

    def send_email(self, email, total,  frm=""):
        self.server.sendmail(frm, email, msg=total)

    def get_total(self):
        week_total = login_webscrape.string_income
        return week_total


    def format_message(self, total):
        return "This weeks total is " + total


if __name__ == '__main__':
    my_email = "yourotheremail@gmail.com"
    tolist = [my_email]

    sender = Email_send(tolist)
    sender.run()
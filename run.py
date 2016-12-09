import os
import csv
import base64
import logging
import requests
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content, Attachment, Personalization
from BeautifulSoup import BeautifulSoup

file_destination = "./inmates.csv"
url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'

def removeFile():
    try:
        os.remove(file_destination)
        logging.info("Past file {} removed".format(file_destination))
    except:
        logging.info("No past file {} to remove".format(file_destination))


def webCrawler():
    try:
        response = requests.get(url)
        html = response.content
    except:
        logging.critical("HTTP error. crawler is not able to connect to {}".format(url))
        return False
    try:
        # Core web parsing logic lives here.
        soup = BeautifulSoup(html)
        table = soup.find('tbody', attrs={'class': 'stripe'})

        list_of_rows = []
        for row in table.findAll('tr'):
            list_of_cells = []
            for cell in row.findAll('td'):
                text = cell.text.replace('&nbsp;', '')
                list_of_cells.append(text)
            list_of_rows.append(list_of_cells)
    except:
        logging.critical("Parsing error. The format of the url must have changed: {}".format(url))
        return False
    logging.info("Web crawler complete")
    return list_of_rows


def saveFile(list_of_rows):
    try:
        outfile = open(file_destination, "wb")
        writer = csv.writer(outfile)
        writer.writerows(list_of_rows)
        logging.info("File {} created".format(file_destination))
        return True
    except:
        logging.critical("Unable to write content to file {}".format(file_destination))
        return False


def sendEmail():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))
    mail = Mail()
    mail.set_from(Email(os.environ.get("EMAIL")))

    personalization = Personalization()
    personalization.add_to(Email(os.environ.get("EMAIL")))
    mail.add_personalization(personalization)

    mail.set_subject("Hello World from the SendGrid Python Library")
    mail.add_content(Content("text/plain", "Sample email text"))

    with open(file_destination, 'rb') as fd:
        b64data = base64.b64encode(fd.read())
    attachment = Attachment()
    attachment.set_content(b64data)
    attachment.set_type("text/csv") # change this if the content is xlsx or somehting else
    attachment.set_filename(file_destination)
    attachment.set_disposition("attachment")
    mail.add_attachment(attachment)

    # Decided not to wrap this part of the code in a try/except block, because if it fails, user should paste error stack and send it to me
    response = sg.client.mail.send.post(request_body=mail.get())
    logging.info(response.status_code)
    logging.info(response.headers)
    logging.info(response.body)

if __name__ == "__main__":
    removeFile()
    list_of_rows = webCrawler()
    if not list_of_rows:
        exit()
    result = saveFile(list_of_rows)
    if not result:
        exit()
    sendEmail()

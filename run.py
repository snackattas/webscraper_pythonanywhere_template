import os
import csv
import base64
import requests
from BeautifulSoup import BeautifulSoup

file_destination = "./inmates.csv"
url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'

def removeFile():
    try:
        os.remove(file_destination)
        print "Past file {} removed\n".format(file_destination)
    except:
        print "No past file {} to remove\n".format(file_destination)


def webCrawler():
    try:
        response = requests.get(url)
        html = response.content
    except:
        print "HTTP error. crawler is not able to connect to {}".format(url)
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
        print "Parsing error. The format of the url must have changed: {}".format(url)
        return False
    print "Web crawler complete\n"
    return list_of_rows


def saveFile(list_of_rows):
    try:
        outfile = open(file_destination, "wb")
        writer = csv.writer(outfile)
        writer.writerows(list_of_rows)
        print "File {} created\n".format(file_destination)
        return True
    except:
        print "Unable to write content to file {}".format(file_destination)
        return False


def sendEmail():
    sendgrid_mail_url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(os.environ.get("SENDGRID_API_KEY"))}

    email_subject = "Hello from SendGrid"
    email_message = "Hello.  This is your scheduled task.  Enjoy the content!"
    file_type = "text/csv"

    with open(file_destination, 'rb') as fd:
        base64data = base64.b64encode(fd.read())

    payload = {
      "content": [
        {
          "type": "text/plain",
          "value": email_message
        }],
      "personalizations": [
        {
          "to": [
            {
              "email": os.environ.get("EMAIL")
            }
          ],
          "subject": email_subject
        }
      ],
      "from": {
        "email": os.environ.get("EMAIL")
      },
      "attachments": [
        {
    	  "content": base64data,
          "type": file_type,
          "filename": file_destination
        }
      ]
    }

    response = requests.post(sendgrid_mail_url, json=payload, headers=headers)
    print "Status code: {}\n".format(response.status_code)
    print "Header: {}\n".format(response.headers)

if __name__ == "__main__":
    removeFile()
    list_of_rows = webCrawler()
    if not list_of_rows:
        exit()
    result = saveFile(list_of_rows)
    if not result:
        exit()
    sendEmail()

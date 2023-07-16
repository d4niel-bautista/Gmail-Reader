from build_service import get_service
import base64
import email
import pandas as pd
from bs4 import BeautifulSoup

# 1 - Read in 20 emails from your personal email and pull out any emails that are from "software@venturebnb.io"
# and include "Traveler Housing Request" in the subject line
def ReadInFurnishedFinderHousingRequestsEmails():
    # TODO: write the code for this function to return the emails that qualify
    service = get_service()
    if service is not False:
        results = service.users().messages().list(userId='me', maxResults=20, labelIds=['INBOX'], q="category:primary").execute()
        messages = results.get('messages', [])

        emails = []
        
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
            mime_msg = email.message_from_bytes(base64.urlsafe_b64decode(msg_data['raw']), policy=email.policy.default)
            if "software@venturebnb.io" in mime_msg['from'] and "Traveler Housing Request" in mime_msg['subject']:
                emails.append(mime_msg.get_body().get_payload(decode=True))
    return emails


# 2 - Loop through the emails and put the following information from EACH email into a new row of a pandas dataframe:
# Tenant, Email Address, Phone Number, Number of Travelers, and Dates
def PullInformationFromEmailsAndPutIntoDataframe(emails):
    # TODO: write the code for this function to return the full dateframe
    df_columns = ['tenant', 'email_address', 'phone_number', 'number_of_travelers', 'dates']
    dataframe = pd.DataFrame(columns=df_columns)
    df_tenant = []
    df_email = []
    df_phone_num = []
    df_num_travelers = []
    df_dates = []
    
    for content in emails:
        soup = BeautifulSoup(content, 'lxml')
        tables = soup.find_all('table', attrs={'align': 'center', "style":"border-collapse:collapse", "border": "0", "cellpadding":"0", 'width': '480'})
        for tbl in tables:
            data = [j.text for i in tbl.tbody.find_all('td') for j in i.find_all('p')]
            if data[0] == 'Tenant:':
                df_tenant.append(data[1])
            elif data[0] == 'Email:':
                df_email.append(data[1])
            elif data[0] == 'Phone #:':
                df_phone_num.append(data[1])
            elif data[0] == 'Travelers:':
                df_num_travelers.append(data[1])
            elif data[0] == 'Dates:':
                df_dates.append(data[1])
    
    dataframe['tenant'] = df_tenant
    dataframe['email_address'] = df_email
    dataframe['phone_number'] = df_phone_num
    dataframe['number_of_travelers'] = df_num_travelers
    dataframe['dates'] = df_dates

    return dataframe

if __name__ == '__main__':
    # 1 - Read in 20 emails from your personal email and pull out any emails that are from "john@venturebnb.io"
    # and include "Traveler Housing Request" in the subject line
    emails = ReadInFurnishedFinderHousingRequestsEmails()
    # 2 - Loop through the emails and put the following information from EACH email into a new row of a pandas dataframe:
    # Tenant, Email Address, Phone Number, Number of Travelers, and Dates
    dataframe = PullInformationFromEmailsAndPutIntoDataframe(emails)
    print(dataframe.to_string())

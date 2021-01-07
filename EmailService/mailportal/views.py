from django.shortcuts import render
import sendgrid
import os
from sendgrid.helpers.mail import *
from mailjet_rest import Client


#  when the request is made, request contain the following parameter.
#  emails_to list = list of email where we have to send mails 
#  content = content of the mail or body of the mail.
#  subject = subject of the mail.

def index(request):

    # here flag to check wheather mail is send successfully or not
    flag = 1

    # if the form is filled then it gets into the if condition
    if(request.method == "POST"):
        emails = request.POST['email']
        emails = emails.split(",")
        

        # We use first RESTAPI of Sendgrid
        #And second RESTAPI is of mailjet
        mailbody = request.POST["content"]
        sub = request.POST['subject']
        
        for email in emails:
        
            # SENDGRID_API_KEY is stored into the sendgrid.env 
            # which is being set as the environment variable

            sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
            # This is registered mail id at sandgrid - Email Web Service
            from_email = Email('tanujsharma19978@gmail.com')
            to_email = To(email)
            subject = sub
            content = Content("text/plain",mailbody)
            try:
                mail = Mail(from_email, to_email, subject, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                
                print(response.status_code)
                print(response.body)
                print(response.headers)
                # print("-----------------------using 1st API-----------------------")
                

                #if the first api produce an exception or get failed in sending mail,
                #we send your mail using second restapi i.e mailjet.
            except Exception as e:
                
                print(e)
                name = email.split("@")
                
                # API_KEY & API_SECRET of mailjet is stored stored under mailjet.env
                # which is later used to make it environment variable 
                api_key = os.environ.get('API_KEY')
                api_secret = os.environ.get('API_SECRET')
                try:
                    
                    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
                    data = {
                    'Messages': [
                        {
                        "From": {
                            #This is the registered mail id at mailjet.
                            "Email": "tanujsharma1412@gmail.com",
                            "Name": "Tanuj"
                        },
                        "To": [
                            {
                            "Email": email,
                            "Name": name[0]
                            }
                        ],
                        "Subject": sub,
                        "TextPart": "My first Mailjet email",
                        "HTMLPart": mailbody,
                        "CustomID": "AppGettingStartedTest"
                        }
                    ]
                    }
                    result = mailjet.send.create(data=data)
                    print (result.status_code)
                    print (result.json())
                    # print("-----------------------------using 2nd API----------------------------")
                except Exception as e2:
                    print(e2)
                    flag = 0                

        # if the mail is send successfully, then we pass the control to success.html
        if(flag == 1):
            return render(request, 'success.html',{'email':email})
        else:
            #if their an error occur, then the control is send to the error.html
            return render(request, 'error.html', {})
    else:
        # if the user didnot submittted the form now we will show index.html.
        return render(request, 'index.html', {})
    
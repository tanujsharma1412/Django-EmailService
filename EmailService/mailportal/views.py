from django.shortcuts import render
import sendgrid
import os
from sendgrid.helpers.mail import *
from mailjet_rest import Client


# Create your views here.

def index(request):

    flag = 1

    if(request.method == "POST"):
        emails = request.POST['email']
        emails = emails.split(",")
        # print(type(emails), "----------------------------------------------------")

        mailbody = request.POST["content"]
        
        for email in emails:
        
            sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
            # print(email)
            from_email = Email('tanujsharma19978@gmail.com')
            to_email = To(email)
            subject = "Mail From SendGrid(1st API)"
            content = Content("text/plain",mailbody)
            try:
                mail = Mail(from_email, to_email, subject, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                
                print(response.status_code)
                print(response.body)
                print(response.headers)
                print("-----------------------using 1st API-----------------------")
                
            except Exception as e:
                
                print(e)
                name = email.split("@")
                
                api_key = 'c5e2da64218aa7bd460723d8010148a4'
                api_secret = 'e53b5047529591a891e7f749cdca1090'
                try:
                    
                    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
                    data = {
                    'Messages': [
                        {
                        "From": {
                            "Email": "tanujsharma1412@gmail.com",
                            "Name": "Tanuj"
                        },
                        "To": [
                            {
                            "Email": email,
                            "Name": name[0]
                            }
                        ],
                        "Subject": "Mail From Mailjet (2nd API)",
                        "TextPart": "My first Mailjet email",
                        "HTMLPart": mailbody,
                        "CustomID": "AppGettingStartedTest"
                        }
                    ]
                    }
                    result = mailjet.send.create(data=data)
                    print (result.status_code)
                    print (result.json())
                    print("-----------------------------using 2nd API----------------------------")
                except Exception as e2:
                    print(e2)
                    flag = 0                

        if(flag == 1):
            return render(request, 'test.html',{'email':email})
        else:
            return render(request, 'error.html', {})
    else:
        return render(request, 'index.html', {})
    
    # if(request.method == "POST"):
    #     email = request.POST['email']
    #     content = request.POST['content']
    #     return render(request, 'test.html', {'email' : email, 'content' : content })
    # else:
    #     return render(request, 'index.html', {})
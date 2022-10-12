from django.core.mail import EmailMessage, send_mail


def mail_send(request):
    # send_mail('Test of body', 'Test of Subject', 'iliyagagarin1@yandex.com',
    #             ['trader177@gmail.com'],
    #             html_message='<h1>First Django email test</h1>')

    em = EmailMessage(subject='to you', body='s', to=['trader177@gmail.com'])
    em.send()

    print('='*9)
    print('EMAIL SENT')
    print('='*9)
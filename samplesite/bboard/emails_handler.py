from django.соre.mail import send_mail


def mail_send(request):
    send_mail('Test of body', 'Test of Subject', 'admin@classifieds.com',
                html_message='<h1>Fucking test</h1>')
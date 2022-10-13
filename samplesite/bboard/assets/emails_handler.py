from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string


def mail_send(request):
    # send_mail('Test of body', 'Test of Subject', 'trader177@gmail.com',
                # ['trader177@gmail.com'],
                # html_message='<h1>First Django email test</h1>')
    context = {'user': 'Some UserName'}
    s = render_to_string('email/letter.txt', context)
    em = EmailMessage(subject='to you', body=s, to=['trader177@gmail.com'])
    em.send()

    print('='*9)
    print('EMAIL SENT')
    print('='*9)
    return redirect('bboard:index') 
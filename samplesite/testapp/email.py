from django.соre.mail import EmailMessage
from django.template.loader import render_to_string


context = {'user': 'Just an example!'}
s = render_to_string('email/letter.txt', context)

em = EmailMessage(subject='reminder', body=s, to=['user@othersite.ru'])
em.send()
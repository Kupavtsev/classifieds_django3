from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse

from .models import Bb

# This is First version I
# def index(request):
#     s = 'Список объявлений\r\n\r\n\r\n'
#     for bb in Bb.objects.order_by('-published'):
#         s += bb.title + '\r\n' +  bb.content + '\r\n\r\n'
#     return HttpResponse(s, content_type='text/plain; charset=utf-8')

# This is Second version II
# def index(request):
#     template = loader.get_template('bboard/index.html')
#     bbs = Bb.objects.order_by('-published')
#     context = {'bbs': bbs}
#     return HttpResponse(template.render(context, request))

# This is Third version III
def index(request):
    bbs = Bb.objects.order_by('-published')
    return render(request, 'bboard/index.html', {'bbs': bbs})
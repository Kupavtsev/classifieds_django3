from multiprocessing import context
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from http.client import HTTPResponse
from django.shortcuts   import render
# from django.template    import loader
from django.urls        import reverse_lazy

# from django.http        import HttpResponse

from .models            import Bb, Rubric
from .forms             import BbForm

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
    # В зависимоти от контекста запрома, render ведет себя по разному
    if request.method == 'GET':     # не обязательно
        bbs             = Bb.objects.all()
        rubrics         = Rubric.objects.all()
        context         = {'bbs': bbs, 'rubrics': rubrics}
        return render(request, 'bboard/index.html', context)
    else:
        return HTTPResponse('Wrong method: 405')

# Func version by_rubric
def by_rubric(request, rubric_id):
    bbs             = Bb.objects.filter(rubric=rubric_id)
    rubrics         = Rubric.objects.all()
    current_rubric  = Rubric.objects.get(pk=rubric_id)
    context         = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)

# Class version by_rubric
class BbByRubricView(TemplateView):
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context

class BbByRubricViewListView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs' # будет сохранен извлеченный набор записей

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context



class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbCreateView(CreateView):
    template_name   = 'bboard/create.html'
    form_class      = BbForm
    success_url     = reverse_lazy('index')
    # success_url     = '/bboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # получаем контекст шаблона от метода базового класса
        print("bboard/views.py - context = super().get_context_data(**kwargs): \n", context)
        context['rubrics'] = Rubric.objects.all()
        print("bboard/views.py - context['rubrics'] = Rubric.objects.all(): \n", context)
        return context

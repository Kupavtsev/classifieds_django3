from django.db.models import Count, OuterRef, Exists
from django.http import HttpResponseRedirect
from http.client import HTTPResponse
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, YearArchiveView, DayArchiveView, DateDetailView

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator

# from django.http        import HttpResponse

from .models            import Bb, Rubric
from .forms             import BbForm


# SQL filters
subquery = Exists(Bb.objects.filter(rubric=OuterRef('pk'), price__gt=100000))
for r in Rubric.objects.annotate(is_expensive=subquery).filter(is_expensive=True): print(r.name)


RC = Rubric.objects.annotate(Count('bb'))

# MAIN PAGE
def index(request):
    # В зависимоти от контекста запроса, render ведет себя по разному

    if request.method == 'GET':     # не обязательно
        # rc = Rubric.objects.annotate(Count('bb'))
        bbs       = Bb.objects.all()
        paginator = Paginator(bbs, 3)
        if "page" in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        rubrics   = Rubric.objects.all()
        context   = {'bbs': page.object_list, 'rubrics': rubrics, 'rc': RC, 'page': page, 'bbstotal': bbs}
        return render(request, 'bboard/index.html', context)
    else:
        return HTTPResponse('Wrong method: 405')

class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period: str = 'year'
    template_name: str = 'bboard/index.html'
    context_object_name: str = 'bbs'
    # context_object_name: str = ''
    allow_empty: bool = True

    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context


# BY RUBRIC - FUNC
def by_rubric(request, rubric_id):
    bbs             = Bb.objects.filter(rubric=rubric_id)
    rubrics         = Rubric.objects.all()
    current_rubric  = Rubric.objects.get(pk=rubric_id)
    context         = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric, 'rc': RC}
    return render(request, 'bboard/by_rubric.html', context)

# BY RUBRIC - CLASS
# It mixdex class You Should avoid such a constructions!
class BbByRubricView(SingleObjectMixin, ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg: str = 'rubric_id'

    # Извлекаем рубкиру с заданным ключом
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        context['bbs'] = context['object_list']         # по умолчанию хранит записи из ListView
        # context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = self.object         # берем рубрику из get
        context['rc'] = RC
        return context

    def get_queryset(self):
        return self.object.bb_set.all()

class BbByRubricViewListView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs' # будет сохранен извлеченный набор записей

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        context['rc'] = RC
        return context


# DETAIL VIEW OF EACH PRODUCT
class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        context['rc'] = RC
        return context


# FORM
class BbCreateView(CreateView):
    template_name   = 'bboard/create.html'
    form_class      = BbForm
    success_url     = reverse_lazy('index')
    # success_url     = '/bboard/detail/{id}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # получаем контекст шаблона от метода базового класса
        # context['rubrics'] = Rubric.objects.all()
        context['rc'] = RC
        return context

class BbAddFormView(FormView):
    template_name   = 'bboard/create.html'
    form_class      = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # мы сохраняем полученную форму в object
    def get_form(self, form_class = None):
        self.object = super().get_form(form_class)
        return self.object

    # Получаем доступ к pk из object
    def get_success_url(self):
        return reverse('by_rubric',
                    kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})

# EDIT AD FORM - CLASS
class BbUpdateView(UpdateView):
    model = Bb
    form_class = BbForm
    # success_url = reverse_lazy('detail')
    success_url = '/bboard/detail/{id}'

    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context

# EDIT AD FORM - FUNC
# ITS DOESNT WORK!!!!!
# Срабатывает метод GET, и почему то перекидывает на create.html
def edit(request, pk):
    bb = Bb.objects.get(pk=pk)
    print('=' * 9)
    print(bb)
    print('=' * 9)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            # if bbf.has_changed():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric',
                                        kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        print('=' * 9)
        print('ELSE')
        print('=' * 9)
        # должен поределять конкретную сущность!!!
        # bbf = BbForm()
        bbf = BbForm(instance=bb)           # НЕ ПОЛУЧАЕТ СОДЕРЖИМОЕ В СКОБКАХ
        print('=' * 9)
        print(bbf)
        print('=' * 9)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/bboard/'

    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context


# DATES
class BbMonthArchiveView(MonthArchiveView):
    model = Bb
    date_field: str = 'published'
    month_format: str = '%m'            # порядковый номер месяца

    context_object_name: str = 'bbs'
    allow_empty: bool = True


    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context


class BbYearArchiveView(YearArchiveView):
    model = Bb
    date_field: str = 'published'
    year_format: str = '%Y'            # порядковый номер месяца

    context_object_name: str = 'bbs'
    allow_empty: bool = True


    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context


class BbDayArchiveView(DayArchiveView):
    context_object_name: str = 'bbs'
    allow_empty: bool = True


    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context

# this is does not work!!!
class BbDayDetailView(DateDetailView):
    model = Bb
    date_field: str = 'published'
    year_format: str = '%m'            # порядковый номер месяца

    # context_object_name: str = 'bbs'
    # allow_empty: bool = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context

    
from django.contrib import messages
from xml.dom import ValidationErr
from django.db.models import Count, OuterRef, Exists, Prefetch
# from django.db.transaction import atomic
from django.http import HttpResponseRedirect, HttpResponseForbidden
from http.client import HTTPResponse

from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, YearArchiveView, DayArchiveView, DateDetailView

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.forms import modelformset_factory, BaseModelFormSet, inlineformset_factory,formset_factory
from django.forms.widgets import TextInput
# from django.forms.formsets import ORDERING_FIELD_NAME

from django.contrib.auth.views import PasswordChangeView, redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# from django_filters.views import FilterView

# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter

# from django.http        import HttpResponse

from .models import Bb, Rubric
from .forms import BbForm, SearchForm

from .sessions import test_cookie
from .filters import BbFilter


# SQL filters
# f1
subquery = Exists(Bb.objects.filter(rubric=OuterRef('pk'), price__gt=100000))
# for r in Rubric.objects.annotate(is_expensive=subquery).filter(is_expensive=True): print(r.name)
# f2
pr1 = Prefetch('bb_set', queryset=Bb.objects.order_by('-title'))
r = Rubric.objects.prefetch_related(pr1).first()
# for bb in r.bb_set.all(): print(bb.price, end=' ')
# f3
pr2 = Prefetch('bb_set', queryset=Bb.objects.filter(price__gt=1000), to_attr='expensive')
r2 = Rubric.objects.prefetch_related(pr2).get(pk=2)
# for bb in r2.expensive: print(bb.price)

# GLOBALS
rubricsAll   = Rubric.objects.all()
RC = Rubric.objects.annotate(Count('bb'))


#           ========================================= 
#           ---===          1 MAIN PAGE        ===---
#           ========================================= 
# 1.1 main
def index(request):
    test_cookie(request)
    # В зависимоти от контекста запроса, render ведет себя по разному

    if request.method == 'GET':     # не обязательно
        # rc = Rubric.objects.annotate(Count('bb'))
        bbs       = Bb.objects.all()
        bbFilter = BbFilter(request.GET,  queryset=bbs)
        bbs = bbFilter.qs
        paginator = Paginator(bbs, 3)
        if "page" in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        # rubrics   = Rubric.objects.all()
        context   = {'bbs': page.object_list,  'rc': RC, 'page': page, 'bbstotal': bbs, 'bbFilter': bbFilter}
        return render(request, 'bboard/index.html', context)
    else:
        return HTTPResponse('Wrong method: 405')
# 1.2
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


#           ========================================= 
#           ---===      2 BY RUBRIC - FUNC     ===---
#           ========================================= 
# 2.1
def by_rubric(request, rubric_id):
    bbs             = Bb.objects.filter(rubric=rubric_id)
    # rubrics         = Rubric.objects.all()
    current_rubric  = Rubric.objects.get(pk=rubric_id)
    context         = {'bbs': bbs, 'rubrics': rubricsAll, 'current_rubric': current_rubric, 'rc': RC}
    return render(request, 'bboard/by_rubric.html', context)

#           ---===      BY RUBRIC - CLASS      ===---
# It mixdex class You Should avoid such a constructions!
# 2.2
class BbByRubricView(SingleObjectMixin, ListView):
# class BbByRubricView(SingleObjectMixin, ListView, FilterView):
    # model = Bb
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg: str = 'rubric_id'
    # I'm not sure about it
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = BbFilter
    # queryset = Bb.objects.all()

    # Извлекаем рубкиру с заданным ключом
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        context['bbs'] = context['object_list']         # по умолчанию хранит записи из ListView
        context['current_rubric'] = self.object         # берем рубрику из get
        context['rc'] = RC
        context['gt1000'] = r2.expensive
        return context

    def get_queryset(self):
        return self.object.bb_set.all()
# 2.3
class BbByRubricViewListView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs' # будет сохранен извлеченный набор записей

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        context['rc'] = RC
        return context


#           ========================================= 
#           ---===3 DETAIL VIEW OF EACH PRODUCT===---
#           ========================================= 
# 3.1
class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        context['rc'] = RC
        return context


#           ========================================= 
#           ---===   4 Add new Advertisment    ===---
#           ========================================= 
# 4.1
class BbCreateView(CreateView):
    template_name   = 'bboard/create.html'
    form_class      = BbForm
    # success_url     = reverse_lazy('index')
    # success_url     = '/bboard/detail/{id}'
    success_url     = '/{rubric_id}'
    success_message = 'created!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # получаем контекст шаблона от метода базового класса
        context['rc'] = RC
        return context
# 4.2
class BbAddFormView(LoginRequiredMixin, FormView):
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
        return reverse('bboard:by_rubric',
                    kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


#           ========================================= 
#           ---===    5 EDIT AD FORM - CLASS   ===---
#           ========================================= 
# 5.1
class BbUpdateView(UserPassesTestMixin, UpdateView):
    model = Bb
    form_class = BbForm
    # success_url = reverse_lazy('detail')
    success_url = '/bboard/detail/{id}'

    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context

    def test_func(self):
        return self.request.user.is_staff

#           ---===    EDIT AD FORM - FUNC   ===---
# 5.2
# @atomic                 # В этом контроллере будет действовать режим атомарных запросов
def edit(request, pk):
    bb = Bb.objects.get(pk=pk)

    bbFilter = BbFilter(request.GET,  queryset=Bb.objects.all())
    bbs = bbFilter.qs

    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление исправлено', extra_tags='first second')
                return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)      
        context = {'form': bbf, 'bbs': bbs, 'bbFilter': bbFilter}
        return render(request, 'bboard/bb_form.html', context)

# 5.3
class BbDeleteView(LoginRequiredMixin, DeleteView):
    model = Bb
    success_url = '/bboard/'

    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context


#           ========================================= 
#           ---===            6 DATES          ===---
#           ========================================= 
# 6.1
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

# 6.2
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

# 6.3
class BbDayArchiveView(DayArchiveView):
    context_object_name: str = 'bbs'
    allow_empty: bool = True


    def get_context_data(self, *args, **kwargs: any):
        context = super().get_context_data(*args, **kwargs)
        context['rc'] = RC
        return context

# this is does not work!!!
# 6.4
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

#           ========================================= 
#           ---=== 7 Edit/Validation in forms  ===---
#           ========================================= 
# 7.1
class RubricBaseFormSet(BaseModelFormSet):
    ordering_widget = TextInput
    def clean(self) -> None:
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms if 'name' in form.cleaned_data]
        if ('Недвижимость' not in names) or ('Транспорт' not in names):
            raise ValidationErr(' Добавьте Недвижимость и Транспорт')
# 7.1
def rubrics(request):
    if request.user.has_perm('bboard.add_rubric'):
        RubricFormSet = modelformset_factory(Rubric, fields=('name',), 
                                            can_delete=True, formset=RubricBaseFormSet)
        # RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_order=True, can_delete=True)

        if request.method == 'POST':
            formset = RubricFormSet(request.POST)
            if formset.is_valid():

                # IT CAN NOT DELETE Rubrics! and reorder!!
                # for form in formset:
                #     if form.cleaned_data:
                #         rubric = form.save(commit=False)
                #         rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                #         rubric.save()
                # return redirect('index')
                
                # That is can to delete and rename, but cant reorder (no such Model column)...
                formset.save()
                return redirect('bboard:index')

                
        else:
            formset = RubricFormSet()
        
        context = {'formset': formset}
        return render(request, 'bboard/rubrics.html', context)
    else:
        return HttpResponseForbidden('Вы не имеете допуска к списку рубрик')


#           ========================================= 
#           ---===  Редактировать объявления   ===---
#           =========================================
# 7.2
def bbs(request, rubric_id):
    if request.user.is_authenticated:
        BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
        rubric = Rubric.objects.get(pk=rubric_id)
        if request.method == 'POST':
            formset = BbsFormSet(request.POST, instance=rubric)
            if formset.is_valid():
                formset.save()
                return redirect('bboard:index')
        else:
            formset = BbsFormSet(instance=rubric)
        
        context = {'formset': formset, 'current_rubric': rubric}
        return render(request, 'bboard/bbs.html', context)
    else:
        return HttpResponseForbidden('Вы не имеете допуска к списку редактирования объявлений')
        # redirect_to_login(reverse('bbs', rubric_id))


#           ========================================= 
#           ---===  8 Password operations      ===---
#           ========================================= 
# 8.1
class PassChg(PasswordChangeView):
    template_name: str = 'registration/password_change_my.html'


#           ========================================= 
#           ---===         9 Search Froms      ===---
#           =========================================
# 9.1
def search(request):
    if request.nethod == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            bbs = Bb.objects.filter(title__icontains=keyword, rubric=rubric_id)
            context = {'bbs': bbs}
            return render(request, 'bboard/search_results.html', context)
    else:
        sf = SearchForm()
    context = {'form': sf}
    return render(request, 'bboard/search.html', context)

# 9.2 Надо Сделать саму форму
def formset_processing(request):
    FS = formset_factory(SearchForm, extra=3, can_order=True, can_delete=True)

    if request.method == 'POST':
        formset = FS(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    keyword = form.cleaned_data['keyword']
                    rubric_id = form.cleaned_data['ORDER']
                    # Выполняем какие-либо действия над полученными данными
            return render(request, 'bboard/process_result.html')
    else:
        formset = FS()
        context = {'formset': formset}
        return render(request, 'bboard/formset.html', context)
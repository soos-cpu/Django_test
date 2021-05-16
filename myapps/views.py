# Create your views here.


from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, HaijuHouseInfo
from django.template import loader
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import time
import datetime


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapps/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myapps/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapps:results', args=(question.id,)))


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    # 1
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # 2
    # template = loader.get_template('myapps/index.html')
    # return HttpResponse(template.render(context, request))

    # 3
    return render(request, 'myapps/index.html', context)


# def details(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'myapps/details.html', {'question': question})

def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    error_message = 'hello1'
    return render(request, 'myapps/details.html', {'question': question, 'error_message': error_message})


class IndexView(generic.ListView):
    template_name = 'myapps/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'myapps/details.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'myapps/results.html'


def homepage(request):
    return render(request, 'myapps/homepage.html', )


def note(request):
    return render(request, 'myapps/note.html', )


def odoo(request):
    start_time = datetime.datetime(2020, 5, 20)
    now_time = datetime.datetime.now()
    days = (now_time - start_time).days
    return render(request, 'myapps/odoo.html', {'days': days})


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage


def ggl_house(request):
    if str(request.user) == 'soos':
        update_flag = True
    search = request.GET.get('q', False)
    if search:
        haiju1 = HaijuHouseInfo.objects.filter(title__icontains=search)
        haiju2 = HaijuHouseInfo.objects.filter(gui_ge__icontains="6室")
        try:
            price = float(search)
            haiju3 = HaijuHouseInfo.objects.filter(price__lte=price).order_by('-price')
            # haiju = haiju1 | haiju2 | haiju3
            haiju = haiju3
        except:
            haiju = haiju1 | haiju2
    else:
        haiju = HaijuHouseInfo.objects.all()
    paginator = Paginator(haiju, 25)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            haiju = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            haiju = paginator.page(1)
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            haiju = paginator.page(paginator.num_pages)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
    return render(request, 'myapps/haiju_info.html', locals())


def update_ggl_house_info(request):
    from .haiju_spider import main
    if str(request.user) == 'soos':
        main()
    return ggl_house(request)


def ggl_house_search(request):
    return ggl_house(request)

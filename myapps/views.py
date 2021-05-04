# Create your views here.


from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
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

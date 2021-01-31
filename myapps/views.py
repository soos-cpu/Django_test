from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


from .models import Question
from django.template import loader


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


from django.http import Http404
from django.shortcuts import render, get_object_or_404


# def details(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'myapps/details.html', {'question': question})

def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    error_message = 'hello'
    return render(request, 'myapps/details.html', {'question': question, 'error_message': error_message})
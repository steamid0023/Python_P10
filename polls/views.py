from logging import ERROR
from operator import index
from sre_constants import SUCCESS

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages

from .forms import QuestionForm
from .models import Question, Choice


def homepage(request):
    return render(request, 'home.html')


def test(request):
    print(request)
    return HttpResponse("Это проверка айпи адреса, можно ли зайти через другой сервис")


def questions_list(request):
    # without templates
    # questions = Question.objects.all()
    # response = ''
    # for index, question in enumerate(questions):
    #     response += f"{index + 1}. {question.text}<br>"
    # return HttpResponse(f"Questions list here.<br>{response}")

    questions = Question.objects.all()

    context = {
        "questions": questions
    }

    return render(request, 'polls/questions.html', context=context)


def question_detail(request, question_id):
    # without template
    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404
    # else:
    #     return HttpResponse(f"Question text: {question.text}<br>pub_date: {question.pub_date}")
    # question = get_object_or_404(Question, id=question_id)
    # return HttpResponse(f"Question text: {question.text}<br>pub_date: {question.pub_date}")

    question = get_object_or_404(Question, id=question_id)
    # choices = Choice.objects.filter(question=question)

    context = {
        "question": question,
        # "choices": choices
    }

    return render(request, 'polls/question_detail.html', context=context)


def question_vote(request, question_id):
    choice = request.POST['choice']
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choices.get(pk=choice)
    except Choice.DoesNotExist:
        raise Http404("Choice doesn't exist.")
    else:
        selected_choice.votes += 1
        selected_choice.save()
        if selected_choice.is_true:
            messages.add_message(request, SUCCESS, 'Your choice is correct.')
            return HttpResponse('Your choice is correct.')
        else:
            messages.add_message(request, ERROR, 'Your choice is incorrect.')
            return HttpResponse('Your choice is incorrect.')
    # return redirect("polls:questions_list")


def question_add(request):
    form = QuestionForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("polls:questions_list")
    return render(request, 'polls/add_question.html', {"form": form})

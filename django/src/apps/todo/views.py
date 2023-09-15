from django.shortcuts import render

from apps.core.models import (
    Source,
    Language,
)

from .models import Todo

from .services import TodoService


# Create your views here.
def index(request):
    todos = Todo.objects.all()
    return render(request, "todo/index.html", {"todos": todos})


def create_todo(request):
    title = request.POST.get("title")
    # todo = Todo.objects.create(title=title)
    # todo.save()
    service = TodoService()
    service.get_or_create_todo(title)
    todos = Todo.objects.all().order_by("-id")
    return render(request, "todo/todos.html", {"todos": todos})


def mark_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.completed = True
    todo.save()
    todos = Todo.objects.all().order_by("-id")
    return render(request, "todo/todos.html", {"todos": todos})


def delete_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.delete()
    todos = Todo.objects.all().order_by("-id")
    return render(request, "todo/todos.html", {"todos": todos})

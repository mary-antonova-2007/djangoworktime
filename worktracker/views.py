from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required


@login_required
def add_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('taskName')
        # Допустим, у модели Task есть поля name и user, а start_time автоматически устанавливается при создании задачи
        new_task = Task(name=task_name, user=request.user)
        new_task.save()
        messages.success(request, 'Задача успешно добавлена!')
        return redirect('home')  # предполагается, что 'home' - это имя URL вашей главной страницы
    else:
        messages.error(request, 'Ошибка при добавлении задачи!')
        return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    # Получение списка активных задач для текущего пользователя
    active_tasks = Task.objects.filter(user=request.user, status='active').order_by('-id')

    # Подготовка контекста для передачи данных в шаблон
    context = {
        'active_tasks': active_tasks,
    }

    # Отображение шаблона с переданным контекстом
    return render(request, 'worktracker/home.html', context)

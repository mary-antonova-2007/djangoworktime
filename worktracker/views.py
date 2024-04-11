from django.contrib.auth.decorators import login_required
from .models import Task
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages


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

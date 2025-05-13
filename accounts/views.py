from django.shortcuts import render, redirect
from .models import User, Transaction
from .forms import UserForm, LoginForm
from decimal import Decimal


def index(request):
    users = User.objects.order_by('-money')
    return render(request, "accounts/index.html", {'title': 'Приветствие', 'users': users})


def profile(request):
    name = request.session.get('user_name')
    user = User.objects.filter(name=name).first()

    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        print(amount_str)
        try:
            amount = Decimal(amount_str)
            user.money += amount
            user.save()
        except:
            pass
    return render(request, "accounts/profile.html", {'user': user})


def signup(request):
    error = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_name'] = user.name
            return redirect('profile')
        else:
            error = 'Неверные данные'

    form = UserForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    error = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = User.objects.filter(name=name, password=password).first()

        if user:
            request.session['user_name'] = user.name
            return redirect('profile')
        else:
            error = 'Неверное имя или пароль'

    form = LoginForm()
    context = {
        'form': form,
        'error': error
    }

    return render(request, 'accounts/login.html', context)


def logout(request):
    request.session['user_name'] = None
    return redirect('home')


def transaction(request):
    error = ''
    success = ''
    sender_name = request.session.get('user_name')
    sender = User.objects.filter(name=sender_name).first()

    if request.method == 'POST':
        receiver_name = request.POST.get('receiver')
        amount_str = request.POST.get('amount')

        try:
            amount = Decimal(amount_str)
            receiver = User.objects.filter(name=receiver_name).first()

            if not receiver:
                error = 'Пользователь не найден.'
            elif receiver.name == sender.name:
                error = 'Нельзя перевести себе.'
            elif amount <= 0:
                error = 'Введите положительную сумму.'
            elif sender.money < amount:
                error = 'Недостаточно средств.'
            else:
                sender.money -= amount
                receiver.money += amount
                sender.save()
                receiver.save()
                Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
                success = f'Перевод выполнен: {amount} -> {receiver.name}'
        except:
            error = 'Неверная сумма.'

    return render(request, 'accounts/transaction.html', {
        'user': sender,
        'error': error,
        'success': success
    })


def history(request):
    name = request.session.get('user_name')
    user = User.objects.filter(name=name).first()
    sent = user.sent_transactions.all().order_by('-timestamp')
    received = user.received_transactions.all().order_by('-timestamp')

    return render(request, 'accounts/history.html', {
        'user': user,
        'sent': sent,
        'received': received
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from recipes.models import CustomRecipe


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='/login')
def profile(request):
    user = request.user
    custom_recipes = CustomRecipe.objects.filter(author=request.user)
    context = {'user': user, 'custom_recipes': custom_recipes}
    return render(request, 'accounts/profile.html', context)

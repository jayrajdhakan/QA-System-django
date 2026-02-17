from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django .contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'qa_app/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'qa_app/register.html', {'form': form})

@staff_member_required
def admin_panel(request):
    return render(request, 'qa_app/admin_panel.html')


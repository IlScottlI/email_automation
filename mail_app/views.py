from django.shortcuts import render
from . import mail_server
# Create your views here.


def index(request):
    arr = mail_server.email_save_attachment()
    context = {
        'inventory': arr
    }
    return render(request, 'index.html', context)

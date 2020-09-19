from django.shortcuts import render, get_list_or_404
from .models import Comment

# Create your views here.
def comment_thread(request,pk):
    obj = get_list_or_404(Comment, pk=pk)
    context = {
        "object":obj
    }
    return render(request,"comment_thread.html",{context})
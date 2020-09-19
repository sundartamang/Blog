from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.http import HttpResponse
from .models import Post,Category
from comments.models import Comment
from django.views.generic import ListView,DetailView,View
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

#for newsletter
from .forms import NewsUserForm
from comments.forms import CommentForm
from marketing.forms import EmailSignupForm
from .models import NewsUsers
from django.core.mail import send_mail
from .utils import get_read_time
from marketing.models import Signup

# Create your views here.
# class HomeView(ListView):
#     model = Post
#     template_name = 'index.html'
# this count total blog under category
def count():
    category = Category.objects.annotate(count_post = Count('post'))
    return category


def homeView(request):
    post = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comments = Comment.objects.all()
    form = EmailSignupForm()

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'categories' : count(),
        'object' : post,
        'page_obj' : page_obj,
        'comments' : comments,
        'form': form
    }
    return render(request,'index.html',context)


    
def archive(request):
    post = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comments = Comment.objects.all()
    context = {
        'categories' : count(),
        'object' : post,
        'page_obj' : page_obj,
        'comments' : comments
    }
    return render(request,'archive.html',context)

def contact(request):
    return render(request,'contact.html')

def category(request,slug):
    blogCategory = get_object_or_404(Category, slug=slug)
    print(blogCategory)
    order_qs = Post.objects.all().filter(category=blogCategory)
    comments = Comment.objects.all()
    context = {
        'categories' : count(),
        'cate' : order_qs,
        'blogCategory' : blogCategory,
        'comments' : comments
    }
    return render(request, 'category.html',context)


def blogDetail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    comments = instance.comments  # Comment.objects.filter_by_instance(instance)
    initial_data = {
        "content_type" : instance.get_content_type,
        "object_id" : instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content= content_data,
            parent = parent_obj
        )
        return redirect(new_comment.content_object.get_absoulate_url())
    else:
        print("**invlaid form**")

    context = {
        'object' : instance,
        'categories' : count(),
        'comments' : comments,
        'comment_form':form,
    }
    return render(request,'blog-details.html',context)
        
#for comment
# def postComment(request,slug):
#     template_name = 'blog-details.html'
#     post = get_object_or_404(Post, slug=slug)
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.save()
#             return redirect('core:details',slug=slug)
#     else:
#         comment_form = CommentForm()
#     return render(request, template_name, {'post': post,
#                                         'comments': comments,
#                                         'new_comment': new_comment,
#                                         'comment_form': comment_form})

    
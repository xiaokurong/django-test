from django.shortcuts import render,get_object_or_404
from .models import Post
# Create your views here.
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_list(request):
    posts=Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                           status='published',
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})

def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    cd = None
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject='{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'test@dealeasy.com',[cd['to']])
            sent = True
    else:
        form= EmailPostForm()
    return render(request,'blog/post/share.html',
                  {'post':post,
                  'form':form,
                    'cd':cd})


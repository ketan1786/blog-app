from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from Blog_App.forms import Updateuser, Createform, CommentForm
from .models import Post, Comment


def index_view(request):
    return render(request, 'index.html')


def post_list_view(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'Blog_App/post_list.html', {'post': post_list})


class BlogDetailView(DetailView):
    model = Post
    template_name = 'Blog_App/detail.html'

    def get_context_data(self, **kwargs):
        print("ok")
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        context['comments'] = Comment.objects.filter(post=self.get_object())
        return context

    def post(self, request, *args, **kwarg):
        print("ok")
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = self.get_object()
            instance.user = request.user
            instance.save()
            redirect_url = "blog/detail/{}".format(self.get_object().id)
            return redirect(redirect_url)


def dashboard_view(request):
    login_user = request.user
    posts = Post.objects.filter(author=login_user)
    return render(request, 'Blog_App/dashboard.html', {'posts': posts})


def update_view(request, pk):
    update = Post.objects.get(id=pk)
    if request.method == 'POST':
        print('ok')
        form = Updateuser(request.POST, instance=update)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request, 'Blog_App/update.html', {'update': update})


def delete_view(request, pk):
    d = Post.objects.get(id=pk).delete()
    return redirect('/')


def createview(request):
    form=Createform()
    if request.method == 'POST':
        form = Createform(request.POST)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.author=request.user
            blog.save()
            return redirect('/blog/post/')
    return render(request ,'Blog_App/create.html',{'form':form})

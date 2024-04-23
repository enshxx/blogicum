from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .constants import POSTS_ON_PAGE
from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post
from .utils import formation_pagination

User = get_user_model()


def filter_posts(post_list):
    return post_list.filter(is_published=True,
                            category__is_published=True,
                            pub_date__lte=timezone.now()
                            )


class PostMixin():
    model = Post
    success_url = reverse_lazy('blog:profile')


class PostDispatchMixin(PostMixin):
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PostFormMixin(LoginRequiredMixin):
    form_class = PostForm
    template_name = 'blog/create.html'


class Index(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = filter_posts(Post.objects).select_related('author')
    paginate_by = POSTS_ON_PAGE


def profile_view(request, username=None):
    if username is None:
        return redirect('blog:profile', username=request.user)
    else:
        user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).select_related('author')
    page_obj = formation_pagination(request, posts)
    context = {
        'profile': user,
        'page_obj': page_obj,
    }

    return render(request, 'blog/profile.html', context)


class PostDeleteView(PostDispatchMixin, DeleteView):
    template_name = 'blog/create.html'


class PostCreateView(PostMixin, PostFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostDispatchMixin, PostFormMixin, UpdateView):
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        post.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, pk, comment_id):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    form = CommentForm(instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    if request.method == 'POST':
        comment.text = request.POST['text']
        comment.save()
        return redirect('blog:post_detail', pk=pk)

    return render(request, 'blog/comment.html', {
        'post': post,
        'comment': comment,
        'form': form
    })


@login_required
def delete_comment(request, pk, comment_id):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=pk)

    return render(request, 'blog/comment.html', {
        'post': post,
        'comment': comment,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'blog/user.html', {'form': form})


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.objects, pk=pk)
    if not post.is_published and post.author != request.user:
        return render(request, 'pages/404.html', status=404)
    comments = Comment.objects.filter(post_id=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, template, context)


def category_posts(request, category_slug):
    tempalte = 'blog/category.html'
    category = get_object_or_404(Category,
                                 is_published=True,
                                 slug=category_slug)
    post_list = filter_posts(category.posts)
    page_obj = formation_pagination(request, post_list)
    context = {'page_obj': page_obj, 'category': category}
    return render(request, tempalte, context)

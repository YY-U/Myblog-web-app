from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Create your views here.
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

#extension2 #8/12
from django.contrib.auth.decorators import login_required

def post_list(request):
    #posts=Post.object
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request,pk):
    #posts=Post.object
    post = get_object_or_404(Post, pk=pk)#与えられたpkのPostがない場合、前よりもっとよい Page Not Found 404 ページが表示
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required#extension2 #8/12
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():#フォームの値が正しいかどうかをチェック
            post = form.save(commit=False)#フォーム保存#commit=False は Post モデルをまだ保存しないという意味。保存前にauthor追加したいから
            post.author = request.user#フォームにauthorを追加
            #post.published_date = timezone.now() #8/11#extension#コメントアウト
            post.save()
            return redirect('post_detail', pk=post.pk)#新しく作成された記事の post_detail ページを表示したいため
            #pk=post.pk ここのpostは新しく作られたブログポスト

    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required#extension2 #8/12
def post_edit(request, pk):#まず urls から追加の pk パラメータ取得
    post = get_object_or_404(Post, pk=pk)#編集したいPostモデルをpk使って取得
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)#フォームを保存する時
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now() #8/11#extension#コメントアウト
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)#編集のためただフォームを開く時
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required#extension2 #8/12
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required#extension2 #8/12
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required#extension2 #8/12
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

#extension post comment
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
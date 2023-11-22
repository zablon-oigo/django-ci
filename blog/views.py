from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment
from .forms import CommentForm,SearchForm,CreatePostForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank

def post_list(request,tag_slug=None):
    posts=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        posts=posts.filter(tags__in=[tag])
    context={"posts":posts,"tag":tag}
    return render(request,"blog/post_list.html",context)

def post_detail(request, post,year,month,day):
    post=get_object_or_404(Post, status=Post.Status.PUBLISHED,
                           slug=post,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
    comments=post.comments.filter(active=True)
    form=CommentForm()
    post_tags_ids=post.tags.values_list('id', flat=True)
    similar_post=Post.objects.filter(status=Post.Status.PUBLISHED,tags__in=post_tags_ids).exclude(id=post.id)
    similar_post=similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    context={"post":post,"form":form,"comments":comments,"similar_post":similar_post}
    return render(request,'blog/post_detail.html',context)




@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(data=request.POST)

    if form.is_valid():
        parent_id = request.POST.get('parent_id')
        parent_obj = Comment.objects.get(id=parent_id) if parent_id else None

        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.parent = parent_obj
        comment.save()
        messages.success(request, "Your comment has been added successfully")
        return redirect(post.get_absolute_url())

    context = {"post": post, "form": form, "comment": comment}
    return render(request, 'post/comment.html', context)


def post_search(request):
    form=SearchForm()
    query=None
    results=[]

    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            search_vector=SearchVector('title', weight='A')+ SearchVector('content', weight='B')
            search_query=SearchQuery(query)
            results=Post.published.annotate(
                search=SearchVector('title', 'content'),
            ).filter(search=query)

    return render(request, 'blog/search.html', {'form':form,'query':query,'results':results})


def create_post(request):
    if request.method =="POST":
        form=CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form=CreatePostForm()
    return render(request,"blog/create_post.html",{"form":form})

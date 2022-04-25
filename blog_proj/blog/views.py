from django.shortcuts import render, get_object_or_404, redirect ,HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post, Comment 
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy ,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView , ListView, 
                                    DetailView, CreateView,
                                    UpdateView, DeleteView)


from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
# Create your views here.


def home(request):
    return render(request, "index.html")


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') 
        # try:
        #     posts = Post.objects.filter(published_date__lte=timezone.now).order_by(-published_date) 
        # except:
        #     print("somthing wrong")
        # else:
        #     return posts


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# class CreatePostView(LoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#     form_class = PostForm
#     model=Post


@login_required
def create_post_view(request):

    if request.method =='POST':
        form = PostForm(request.POST)
        # import pdb;pdb.set_trace()
        if form.is_valid():
            # form = form.save(commit = False)
            # form.author = request.user
            form.save()
            # import pdb; pdb.set_trace()
            return HttpResponseRedirect(reverse("blog:post_list"))
            # return redirect('blog:post_detail', pk=form.pk)


    else:
        # form = JournalForm(initial={'tank': 123})
        user = get_object_or_404(User, pk=request.user.pk)
        form = PostForm(initial={'author': user})

        return render(request, 'blog/post_form.html',{'form':form})
    


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model=Post



class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


#############################################
#############################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)







def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # return HttpResponseRedirect(reverse("blog:post_detail", kwargs={'pk':post.pk}))
            # return reverse('blog:post_detail', pk=post.pk)
            return redirect('blog:post_detail', pk=post.pk)

    else:
        form=CommentForm()

    return render(request, 'blog/comment_form.html',{'form':form}) 


#login
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk= comment.post.pk)



@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)





# ###--------------------API views------------------####


@api_view(['GET', 'POST'])
def post_list(request):
    """
    List all code posts, or create a new post.
    """
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
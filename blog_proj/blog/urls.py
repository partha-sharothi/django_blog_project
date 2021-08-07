
from django.urls import path
from .import views

urlpatterns = [
    # path('',views.home, name='home'),
    path('',views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(),name='about'),
    path('post/<pk=int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new/',views.CreatePostView.as_view(), name='post_new'),
    path('post/<pk=int:pk>/edit/',views,PostUpdateView.as_view(),name='post_edit'),
    path('post/<pk=int:pk>/remove/', views.PostDeleteView.as_view(),name='Post_remove'),
    path('drafts/',views.DraftListView.as_view(),name='post_draft_list'),
]


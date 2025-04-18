from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

app_name = 'myblog'

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('blog:profile')
    
urlpatterns = [
    path('posts/', views.all_posts, name='all_posts'),
    path('posts/<slug:tag_slug>', views.all_posts, name='post_list_tags'),
    
    path('post/<int:id>',views.post_detail, name="post"),
    path('post/<int:id>/comment/',views.set_comment, name="comment"),
    path('search/', views.search, name='search_post'),
    path('profile/',views.profile,name="profile"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/create-post/',views.create_post,name="create_post"),
    path('profile/edit-post/<int:post_id>',views.edit_post,name="edit_post"),
    path('post/<int:id>/toggle_active/', views.activat_post, name='toggle_active'),
    path('post/<int:id>/',views.delete_post,name="delete_post"),
    path('signup',views.sign_up,name="sign_up"),
    path('user/edit-profile/',views.edit_profile,name="edit_profile"),
    path('contact/',views.resume_view,name="contact")
]

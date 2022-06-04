from django.urls import path
from . import views

urlpatterns = [
    path('manga/', views.MangaListView.as_view()),
    path('new_chapters/', views.NewChaptersListView.as_view()),
    path('manga/<int:pk>/', views.MangaDetailView.as_view(), name='manga-detail'),
    path('chapter/<int:pk>/', views.ChapterDetailView.as_view(), name='chapter-detail'),
    path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('profile/', views.UserURLView.as_view()),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('notifications/', views.UserNoticeListView.as_view()),
    path('team/create/', views.TeamCreateView.as_view(), name='team-create'),
    path('manga/<int:pk>/set_rating/', views.RatingSetView.as_view(), name='rating-create'),
    path('manga/<int:pk>/set_section/', views.SectionSetView.as_view(), name='section-create'),
    path('manga/<int:pk>/manga_update/', views.MangaUpdateView.as_view(), name='manga-update'),
    path('manga/<int:pk>/manga_delete/', views.MangaDeleteView.as_view(), name='manga-delete'),
    path('manga/<int:pk>/manga_pass/', views.MangaPassView.as_view(), name='manga-pass'),
    path('manga/<int:pk>/chapter_add/', views.ChapterAddView.as_view(), name='chapter-add'),

]

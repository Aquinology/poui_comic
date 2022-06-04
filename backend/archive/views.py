from abc import ABC

from .models import Manga, Chapter, Team, Member, Profile, Role

from django.db import models
from rest_framework import permissions, generics
from . import serializers
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied


class Round(models.Func, ABC):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s::numeric, 2)'


class AdminMangaPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        role = Role.objects.filter(name__in=['Админ', 'Модератор'])
        manga = Manga.objects.filter(id=obj.id, owner__members__user__id=request.user.id,
                                     owner__members__role__in=role)
        if manga.exists():
            return True
        raise PermissionDenied('Данный тйтл не принадлежит вашей группе или у вас нет прав администратора.')


# --------------------ХЕДЕР--------------------

class UserURLView(generics.ListAPIView):
    """Пользователь"""

    serializer_class = serializers.UserURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user.id)


class UserNoticeListView(generics.ListAPIView):
    """Новые главы манг, которые читает пользователь"""

    serializer_class = serializers.NoticeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        notifications = Chapter.objects.filter(manga__user_section__user__id=self.request.user.id,
                                               add_date__gt=models.F('manga__user_section__add_data'))\
            .exclude(profile__id=self.request.user.id)
        return notifications.order_by('-add_date')


# --------------------ГЛАВНАЯ--------------------

class MangaListView(generics.ListAPIView):
    """Все тайтлы"""

    serializer_class = serializers.MangaListSerializer
    queryset = Manga.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        manga = Manga.objects.annotate(
            average_rating=Round(models.Avg('ratings__rating')),
        ).order_by('-average_rating')
        return manga


class NewChaptersListView(generics.ListAPIView):
    """Недавно вышедшие главы"""

    serializer_class = serializers.NewChapterListSerializer
    queryset = Chapter.objects.all().order_by('-add_date')


# -------------------СТРАНИЦА МАНГИ-------------------

class MangaDetailView(generics.RetrieveAPIView):
    """Страница какой-то манги"""

    serializer_class = serializers.MangaDetailSerializer

    def get_queryset(self):
        manga = Manga.objects.annotate(
            average_rating=Round(models.Avg('ratings__rating')),
        )
        return manga


# --------------------СТРАНИЦА ГЛАВЫ--------------------

class ChapterDetailView(generics.RetrieveAPIView):
    """Страница какой-то главы"""

    serializer_class = serializers.ChapterDetailSerializer
    queryset = Chapter.objects.all()


class MangaUpdateView(generics.RetrieveUpdateAPIView):
    """Редактировать тайтл"""

    serializer_class = serializers.MangaUpdateSerializer
    queryset = Manga.objects.all()
    permission_classes = [permissions.IsAuthenticated & AdminMangaPermission]

    def perform_update(self, serializer):
        serializer.save()


class MangaDeleteView(generics.DestroyAPIView):
    """Удалить тайтл"""

    queryset = Manga.objects.all()
    permission_classes = [permissions.IsAuthenticated & AdminMangaPermission]


class MangaPassView(generics.RetrieveUpdateAPIView):
    """Передать тайтл"""

    serializer_class = serializers.MangaPassSerializer
    queryset = Manga.objects.all()
    permission_classes = [permissions.IsAuthenticated & AdminMangaPermission]

    def perform_update(self, serializer):
        serializer.save()


class RatingSetView(generics.CreateAPIView):
    """Обновить оценку"""

    serializer_class = serializers.RatingSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id, manga_id=self.kwargs.get('pk'))


class SectionSetView(generics.CreateAPIView):
    """Обновить секцию"""

    serializer_class = serializers.SectionSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id, manga_id=self.kwargs.get('pk'))


class ChapterAddView(generics.ListCreateAPIView):
    """Добавить главу"""

    serializer_class = serializers.ChapterAddSerializer
    queryset = Chapter.objects.all()
    permission_classes = [permissions.IsAuthenticated & AdminMangaPermission]

    def perform_create(self, serializer):
        team = Team.objects.filter(pk__in=self.request.data['team'],
                                   members__user_id=self.request.user.id)
        if team.exists():
            serializer.save(manga_id=self.kwargs.get('pk'))
        else:
            raise ValidationError('Вы не состоите в данной группе.')


class ChapterDelete(generics.DestroyAPIView):
    """Удалить главу"""

    queryset = Chapter.objects.all()
    permission_classes = [permissions.IsAuthenticated & AdminMangaPermission]


# -------------СТРАНИЦА ГРУППЫ ПЕРЕВОДЧИКОВ-------------

class TeamDetailView(generics.RetrieveAPIView):
    """Страница какой-то команды переводчиков"""

    serializer_class = serializers.TeamDetailSerializer
    queryset = Team.objects.all()


# -----------------ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ-----------------

class UserDetailView(generics.RetrieveAPIView):
    """Страница какого-то пользователя"""

    serializer_class = serializers.UserDetailSerializer
    queryset = Profile.objects.all()


class TeamCreateView(generics.CreateAPIView):
    """Создать команду переводчиков"""

    serializer_class = serializers.TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        team = get_object_or_404(Team, title=serializer.data['title'])
        role = Role.objects.filter(name__in=['Участник', 'Админ'])
        member = Member.objects.create(user_id=self.request.user.id, team_id=team)
        member.role.set(role)
        member.save()

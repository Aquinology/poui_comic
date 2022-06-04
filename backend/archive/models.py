from django.db import models
from auth_system.models import User


class Team(models.Model):
    title = models.CharField(max_length=256, unique=True)
    team_pic = models.ImageField(upload_to='team_pics/', default='team_pics/no-image.jpg', blank=True)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Manga(models.Model):
    STATUS = [
        (0, 'Продолжается'),
        (1, 'Завершён'),
        (2, 'Заморожен'),
        (3, 'Заброшен'),
    ]
    title = models.CharField(max_length=256, unique=True)
    manga_pic = models.ImageField(upload_to='manga_pics/', default='manga_pics/no-image.jpg', blank=True)
    desc = models.TextField()
    status = models.PositiveIntegerField(choices=STATUS, default=0)
    genre = models.ManyToManyField(Genre)
    owner = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}  | {self.get_status_display()}'


class Chapter(models.Model):
    vol = models.PositiveIntegerField()
    chap = models.PositiveIntegerField()
    title = models.CharField(max_length=256, blank=True, null=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='chapters')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='chapters')
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.manga.title} - Том {self.vol} Глава {self.chap} | {self.team.title}'

    class Meta:
        ordering = ['-vol', '-chap']
        unique_together = ('vol', 'chap', 'manga', 'team')


class Profile(User):
    read_chapters = models.ManyToManyField(Chapter, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Member(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='member_of')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    role = models.ManyToManyField(Role)

    def __str__(self):
        return f'{self.user.username} | {self.team.title}'

    class Meta:
        unique_together = ('user', 'team')


class Section(models.Model):
    SECTION = [
        (0, 'Читаю'),
        (1, 'В планах'),
        (2, 'Отложенные'),
        (3, 'Любимые'),
        (4, 'Прочитано'),
        (5, 'Брошено'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='manga_of_user')
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='user_section')
    section = models.PositiveIntegerField(choices=SECTION, default=0)
    add_data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ---> {self.manga.title} | {self.get_section_display()}'

    class Meta:
        unique_together = ('user', 'manga')


class Rating(models.Model):
    RATING = [
        (5, 'Супер'),
        (4, 'Хорошо'),
        (3, 'Нормально'),
        (2, 'Плохо'),
        (1, 'Ужасно'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(choices=RATING, default=5)

    def __str__(self):
        return f'{self.user.username} ---> {self.manga.title} | {self.get_rating_display()}'

    class Meta:
        unique_together = ('user', 'manga')


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
    page = models.ImageField(upload_to='pages/')
    queue = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.chapter} ({self.queue})'

    class Meta:
        ordering = ['queue']
        unique_together = ('chapter', 'page')

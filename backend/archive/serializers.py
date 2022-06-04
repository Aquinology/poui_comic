from rest_framework import serializers
from .models import Manga, Section, Chapter, Page, Genre, Team, Member, Role, Profile, Rating
from auth_system.models import User


# *********** Минимальные элементы ************

class UserURLSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', read_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'url')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name',)


class TeamURLSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='team-detail', read_only=True)

    class Meta:
        model = Team
        fields = ('title', 'url')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class MangaURLSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='manga-detail', read_only=True)

    class Meta:
        model = Manga
        fields = ('title', 'url')


class MangaURLPicSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='manga-detail', read_only=True)

    class Meta:
        model = Manga
        fields = ('title', 'manga_pic', 'url')


class SectionSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='get_section_display')

    class Meta:
        model = Section
        fields = ('section',)


class ChapterURLSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='chapter-detail', read_only=True)

    class Meta:
        model = Chapter
        fields = ('vol', 'chap', 'title', 'url')


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('page',)


# ************ Элементы хедера ****************


class NoticeListSerializer(serializers.HyperlinkedModelSerializer):
    manga = MangaURLPicSerializer()
    team = TeamURLSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='chapter-detail', read_only=True)

    class Meta:
        model = Chapter
        fields = ('vol', 'chap', 'title', 'manga', 'team', 'add_date', 'url')


# ********* Элементы главной страницы *************

class MangaListSerializer(serializers.HyperlinkedModelSerializer):
    average_rating = serializers.FloatField()
    user_section = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='manga-detail', read_only=True)

    def get_user_section(self, manga):
        if self.context.get('request').user.is_authenticated:
            qs = Section.objects.filter(manga_id=manga, user_id=self.context.get('request').user.id)
        else:
            qs = None
        serializer = SectionSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Manga
        fields = ('title', 'manga_pic', 'average_rating', 'user_section', 'url')


class NewChapterListSerializer(serializers.HyperlinkedModelSerializer):
    manga = MangaURLPicSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='chapter-detail', read_only=True)

    class Meta:
        model = Chapter
        fields = ('vol', 'chap', 'title', 'manga', 'url')


# ************ Элементы страницы манги *************

class ChapterMangaDetailSerializer(serializers.HyperlinkedModelSerializer):
    read_status = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='chapter-detail', read_only=True)

    def get_read_status(self, chapter):
        status = False
        if self.context.get('request').user.is_authenticated:
            qs = Profile.objects.filter(id=self.context.get('request').user.id,
                                        read_chapters__id=chapter.id).values('read_chapters')
            if qs.exists():
                status = True
        return status

    class Meta:
        model = Chapter
        fields = ('vol', 'chap', 'title', 'add_date', 'read_status', 'url')


class MangaDetailSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.CharField(source='get_status_display')
    genre = GenreSerializer(many=True)
    average_rating = serializers.FloatField(read_only=True)
    owner = TeamURLSerializer()
    translations = serializers.SerializerMethodField()
    set_rating = serializers.HyperlinkedIdentityField(view_name='rating-create', read_only=True)
    set_section = serializers.HyperlinkedIdentityField(view_name='section-create', read_only=True)
    manga_update = serializers.HyperlinkedIdentityField(view_name='manga-update', read_only=True)
    manga_delete = serializers.HyperlinkedIdentityField(view_name='manga-delete', read_only=True)
    manga_pass = serializers.HyperlinkedIdentityField(view_name='manga-pass', read_only=True)
    chapter_add = serializers.HyperlinkedIdentityField(view_name='chapter-add', read_only=True)

    def get_translations(self, manga):
        teams = Team.objects.filter(chapters__manga=manga).distinct()
        result = []
        if teams.exists():
            for team in teams:
                chapters = Chapter.objects.filter(manga_id=manga, team_id=team)
                result.append({
                    'title': team.title,
                    'chapters': ChapterMangaDetailSerializer(instance=chapters, many=True,
                                                             context=self.context).data
                })
        return result

    class Meta:
        model = Manga
        fields = ('title', 'manga_pic', 'desc', 'genre', 'average_rating', 'owner', 'status',
                  'translations', 'set_rating', 'set_section', 'manga_update', 'manga_delete',
                  'manga_pass', 'chapter_add')


class MangaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ('title', 'manga_pic', 'desc', 'genre', 'status')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.manga_pic = validated_data.get('manga_pic', instance.manga_pic)
        print(instance.manga_pic)
        print(validated_data.get('manga_pic', instance.manga_pic))
        instance.desc = validated_data.get('desc', instance.desc)
        instance.status = validated_data.get('status', instance.status)
        genre = Genre.objects.filter(manga_id=instance.id)
        instance.genre.set(validated_data.get('genre', genre))
        instance.save()
        return instance


class MangaPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ('owner',)

    def update(self, instance, validated_data):
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance


class RatingSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating',)

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            user_id=validated_data.get('user_id'),
            manga_id=validated_data.get('manga_id'),
            defaults={'rating': validated_data.get('rating')}
        )
        return rating


class SectionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('section',)

    def create(self, validated_data):
        section, _ = Section.objects.update_or_create(
            user_id=validated_data.get('user_id'),
            manga_id=validated_data.get('manga_id'),
            defaults={'section': validated_data.get('section')}
        )
        return section


class ChapterAddSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ('vol', 'chap', 'title', 'team', 'pages')


# ************ Элементы страницы главы *************

class ChapterDetailSerializer(serializers.ModelSerializer):
    manga = MangaURLSerializer()
    pages = PageSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ('vol', 'chap', 'title', 'manga', 'pages')


# ******** Элементы страницы команды переводчиков *********

class MemberTeamSerializer(serializers.ModelSerializer):
    user = UserURLSerializer()
    role = RoleSerializer(many=True)

    class Meta:
        model = Member
        fields = ('user', 'role')


class TeamDetailSerializer(serializers.ModelSerializer):
    members = MemberTeamSerializer(many=True, read_only=True)
    manga = serializers.SerializerMethodField()

    def get_manga(self, team):
        manga = Manga.objects.filter(chapters__team_id=team) | Manga.objects.filter(owner_id=team)
        manga = manga.distinct()
        if manga.exists():
            qs = manga
        else:
            qs = None
        serializer = MangaURLPicSerializer(instance=qs, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Team
        fields = ('title', 'team_pic', 'desc', 'members', 'manga')


# ******** Элементы страницы профиля *********

class MangaSectionUserSerializer(serializers.HyperlinkedModelSerializer):
    last_chapter = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='manga-detail', read_only=True)

    def get_last_chapter(self, manga):
        if self.context.get('request').user.is_authenticated:
            qs = Chapter.objects.filter(manga_id=manga, profile__id=self.context.get('request').user.id).first()
        else:
            qs = None
        serializer = ChapterURLSerializer(instance=qs, context=self.context)
        return serializer.data

    class Meta:
        model = Manga
        fields = ('title', 'manga_pic', 'last_chapter', 'url')


class SectionUserDetailSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='get_section_display')
    manga = MangaSectionUserSerializer()

    class Meta:
        model = Section
        fields = ('section', 'manga')


class MemberUserDetailSerializer(serializers.HyperlinkedModelSerializer):
    team = TeamURLSerializer()

    class Meta:
        model = Member
        fields = ('team',)


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    member_of = MemberUserDetailSerializer(many=True)
    manga_of_user = serializers.SerializerMethodField()
    new_team = serializers.URLField(default='http://localhost:8000/api/v1/archive/team/create/')  # del

    def get_manga_of_user(self, user):
        qs = Section.objects.filter(user_id=user)
        serializer = SectionUserDetailSerializer(instance=qs, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Profile
        fields = ('username', 'avatar', 'member_of', 'manga_of_user', 'new_team')


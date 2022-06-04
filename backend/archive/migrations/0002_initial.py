# Generated by Django 4.0.4 on 2022-05-26 03:34

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('archive', '0001_initial'),
        ('auth_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('read_chapters', models.ManyToManyField(blank=True, to='archive.chapter')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth_system.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('team_pic', models.ImageField(blank=True, default='team_pics/no-image.jpg', upload_to='team_pics/')),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='archive.chapter'),
        ),
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.ManyToManyField(to='archive.role'),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='archive.team'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_of', to='archive.profile'),
        ),
        migrations.AddField(
            model_name='manga',
            name='genre',
            field=models.ManyToManyField(to='archive.genre'),
        ),
        migrations.AddField(
            model_name='manga',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.team'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='archive.manga'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='archive.team'),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.PositiveIntegerField(choices=[(0, 'Читаю'), (1, 'В планах'), (2, 'Отложенные'), (3, 'Любимые'), (4, 'Прочитано'), (5, 'Брошено')], default=0)),
                ('add_data', models.DateField(auto_now_add=True)),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_section', to='archive.manga')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manga_of_user', to='archive.profile')),
            ],
            options={
                'unique_together': {('user', 'manga')},
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(5, 'Супер'), (4, 'Хорошо'), (3, 'Нормально'), (2, 'Плохо'), (1, 'Ужасно')], default=5)),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='archive.manga')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.profile')),
            ],
            options={
                'unique_together': {('user', 'manga')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together={('chapter', 'page')},
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('user', 'team')},
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together={('vol', 'chap', 'manga')},
        ),
    ]
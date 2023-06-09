# Generated by Django 4.1.5 on 2023-05-30 13:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citizenship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True, verbose_name='Название страны')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(default='', verbose_name='Адрес отделения')),
                ('post_index', models.CharField(default='', max_length=6, verbose_name='Почтвый индекс')),
            ],
        ),
        migrations.CreateModel(
            name='Doc_migr_pers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(default='', max_length=20, unique=True, verbose_name='Серия и номер документа')),
                ('issued_by', models.TextField(default='', verbose_name='Кем выдан документ')),
                ('issued_when', models.DateField(default='', verbose_name='Дата выдачи документа')),
                ('expires_when', models.DateField(default='', null=True, verbose_name='Дата окончания срока действия документа')),
            ],
        ),
        migrations.CreateModel(
            name='Migrant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', verbose_name='ФИО')),
                ('address', models.TextField(verbose_name='Адрес проживания')),
                ('birthday', models.DateField(default='', verbose_name='Дата рождения')),
                ('birthday_place', models.TextField(verbose_name='Место рождения')),
                ('profession', models.CharField(default='Безработный', max_length=150, verbose_name='Профессия')),
                ('citizenship', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.citizenship', verbose_name='Гражданство')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=11, verbose_name='Номер телефона')),
            ],
        ),
        migrations.CreateModel(
            name='Unregistration_Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='', verbose_name='Дата заполнения документа')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.department')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.migrant')),
            ],
        ),
        migrations.CreateModel(
            name='Registration_Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='', verbose_name='Дата заполнения документа')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.department')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.migrant')),
            ],
        ),
        migrations.AddField(
            model_name='migrant',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.phone'),
        ),
        migrations.AddField(
            model_name='migrant',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.doc_migr_pers'),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expirience', models.IntegerField(verbose_name='Стаж работы')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Оклад')),
                ('rank', models.CharField(default='', max_length=30, null=True, verbose_name='Звание')),
                ('information', models.TextField(verbose_name='Информация о сотруднике')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.phone')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.phone'),
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail пользователя')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'employee'), (2, 'analyst'), (3, 'department_dir'), (4, 'admin')])),
                ('department', models.ManyToManyField(to='api.department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]

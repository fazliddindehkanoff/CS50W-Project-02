# Generated by Django 4.0.5 on 2022-07-02 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_comment_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listingid',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='title',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.listing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

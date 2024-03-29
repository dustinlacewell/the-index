from __future__ import unicode_literals

from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('pages.HomePage')

    # Delete the default homepage
    Page.objects.get(id=2).delete()

    # # Create content type for homepage model
    # homepage_content_type, created = ContentType.objects.get_or_create(
    #     model='homepage', app_label='pages')

    # # Create a new homepage
    # homepage = HomePage.objects.create(
    #     title="Welcome to The Index",
    #     slug='index',
    #     content_type=homepage_content_type,
    #     path='00010001',
    #     depth=2,
    #     numchild=0,
    #     url_path='/index',
    # )

    # Create a site with the new homepage set as the root
    # Site.objects.create(
    #     hostname='localhost', is_default_site=True)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_homepage),
    ]

from django.db import migrations


def sync_moved_content_revisions(apps, schema_editor):
    from about_company.models import AboutPage
    from home.models import HomePage

    pages = [*HomePage.objects.all(), *AboutPage.objects.all()]
    for page in pages:
        revision = page.save_revision(log_action=False)
        if page.live:
            revision.publish(log_action=False)


class Migration(migrations.Migration):

    dependencies = [
        ("about_company", "0006_alter_aboutpage_indicators"),
        ("home", "0010_remove_homepage_achievements"),
    ]

    operations = [
        migrations.RunPython(
            sync_moved_content_revisions,
            migrations.RunPython.noop,
        ),
    ]

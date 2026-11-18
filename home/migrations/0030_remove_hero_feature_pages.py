from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0029_citypage_buttons_alter_citypage_content"),
        ("content_pages", "0002_move_content_pages"),
    ]

    operations = [
        migrations.DeleteModel(name="HeroFeatureIndexPage"),
        migrations.DeleteModel(name="HeroFeaturePage"),
    ]

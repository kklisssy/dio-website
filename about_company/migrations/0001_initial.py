# Generated manually on 2026-05-26

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models

from about_company.models import AchievementsBlock, CertificatesBlock
from base.page_blocks import FeaturesBlock, RichTextSectionBlock
from home.models import PartnershipBlock, WorkWithBlock


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0096_referenceindex_referenceindex_source_object_and_more"),
        ("wagtailimages", "0027_image_description"),
        ("home", "0004_homepage_hero_features_alter_homepage_hero"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "hero_label",
                    models.CharField(
                        blank=True,
                        default="О компании",
                        max_length=120,
                        verbose_name="Лейбл hero",
                    ),
                ),
                (
                    "headline",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "intro",
                    models.TextField(
                        blank=True,
                        verbose_name="Описание",
                    ),
                ),
                (
                    "content",
                    wagtail.fields.StreamField(
                        [
                            ("achievements", AchievementsBlock()),
                            ("features", FeaturesBlock()),
                            ("rich_text", RichTextSectionBlock()),
                            ("work_with", WorkWithBlock()),
                            ("partners", PartnershipBlock()),
                            ("certificates", CertificatesBlock()),
                        ],
                        blank=True,
                        use_json_field=True,
                        verbose_name="Содержимое страницы",
                    ),
                ),
                (
                    "hero_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Фоновое изображение hero",
                    ),
                ),
            ],
            options={
                "verbose_name": "О компании",
                "verbose_name_plural": "Страницы о компании",
            },
            bases=("wagtailcore.page",),
        ),
    ]

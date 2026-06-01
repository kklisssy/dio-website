# Generated manually on 2026-05-29

import wagtail.fields
from django.db import migrations

from about_company.models import AchievementsBlock, CertificatesBlock, WorkStagesBlock
from base.page_blocks import FeaturesBlock, RichTextSectionBlock
from home.models import PartnershipBlock, WorkWithBlock


class Migration(migrations.Migration):

    dependencies = [
        ("about_company", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutpage",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    ("achievements", AchievementsBlock()),
                    ("features", FeaturesBlock()),
                    ("rich_text", RichTextSectionBlock()),
                    ("work_with", WorkWithBlock()),
                    ("work_stages", WorkStagesBlock()),
                    ("partners", PartnershipBlock()),
                    ("certificates", CertificatesBlock()),
                ],
                blank=True,
                use_json_field=True,
                verbose_name="Содержимое страницы",
            ),
        ),
    ]

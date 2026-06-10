import uuid

from django.db import migrations


def move_content(apps, schema_editor):
    AboutPage = apps.get_model("about_company", "AboutPage")
    HomePage = apps.get_model("home", "HomePage")

    for home_page in HomePage.objects.all():
        about_page = (
            AboutPage.objects.filter(
                path__startswith=home_page.path,
                depth__gt=home_page.depth,
            )
            .order_by("path")
            .first()
        )
        if about_page is None:
            continue

        home_achievements = list(home_page.achievements.raw_data)
        about_content = list(about_page.content.raw_data)

        work_stages = next(
            (block for block in about_content if block["type"] == "work_stages"),
            None,
        )
        if work_stages and not home_page.work_stages:
            home_page.work_stages = [work_stages]

        if home_achievements:
            items = [
                {
                    "id": block.get("id", str(uuid.uuid4())),
                    "type": "item",
                    "value": block["value"],
                }
                for block in home_achievements
            ]
            about_page.indicators = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "indicators",
                    "value": {
                        "title": "Наши достижения в цифрах",
                        "intro": (
                            "Результаты многолетней работы в сфере автоматизации "
                            "бизнеса и внедрения информационных систем."
                        ),
                        "items": items,
                    },
                }
            ]

        about_page.content = [
            block
            for block in about_content
            if block["type"] not in {"achievements", "work_stages"}
        ]

        home_page.save(update_fields=["work_stages"])
        about_page.save(update_fields=["indicators", "content"])


def restore_content(apps, schema_editor):
    AboutPage = apps.get_model("about_company", "AboutPage")
    HomePage = apps.get_model("home", "HomePage")

    for home_page in HomePage.objects.all():
        about_page = (
            AboutPage.objects.filter(
                path__startswith=home_page.path,
                depth__gt=home_page.depth,
            )
            .order_by("path")
            .first()
        )
        if about_page is None:
            continue

        about_content = list(about_page.content.raw_data)
        work_stages = list(home_page.work_stages.raw_data)
        indicators = list(about_page.indicators.raw_data)

        if work_stages:
            about_content.extend(work_stages)

        if indicators:
            indicator_value = indicators[0]["value"]
            about_content.insert(
                0,
                {
                    "id": str(uuid.uuid4()),
                    "type": "achievements",
                    "value": indicator_value,
                },
            )

        about_page.content = about_content
        about_page.save(update_fields=["content"])


class Migration(migrations.Migration):

    dependencies = [
        ("about_company", "0003_aboutpage_indicators"),
        ("home", "0009_homepage_work_stages"),
    ]

    operations = [
        migrations.RunPython(move_content, restore_content),
    ]

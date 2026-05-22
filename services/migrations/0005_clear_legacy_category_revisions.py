from typing import ClassVar

from django.db import migrations


def clear_legacy_category_revisions(apps, _schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Revision = apps.get_model("wagtailcore", "Revision")

    try:
        content_type = ContentType.objects.get(
            app_label="services",
            model="singleservicepage",
        )
    except ContentType.DoesNotExist:
        return

    for revision in Revision.objects.filter(content_type=content_type):
        if revision.content.get("category") is not None:
            revision.content["category"] = None
            revision.save(update_fields=["content"])


class Migration(migrations.Migration):

    dependencies: ClassVar[list[tuple[str, str]]] = [
        ("services", "0004_servicecategory_alter_singleservicepage_content_and_more"),
    ]

    operations: ClassVar[list[object]] = [
        migrations.RunPython(clear_legacy_category_revisions, migrations.RunPython.noop),
    ]

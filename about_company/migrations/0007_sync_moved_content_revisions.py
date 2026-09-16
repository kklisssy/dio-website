from django.db import migrations
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.models import get_serializable_data_for_fields


def serialize_page(instance, db_alias):
    """Serialize historical fields and clustered children without live models."""
    content = get_serializable_data_for_fields(instance)
    for relation in instance._meta.related_objects:
        if isinstance(relation.field, ParentalKey):
            name = relation.get_accessor_name()
            content[name] = [
                serialize_page(child, db_alias)
                for child in getattr(instance, name).using(db_alias).all()
            ]
    return content


def sync_moved_content_revisions(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Page = apps.get_model("wagtailcore", "Page")
    Revision = apps.get_model("wagtailcore", "Revision")
    ContentType = apps.get_model("contenttypes", "ContentType")
    base_content_type, _ = ContentType.objects.using(db_alias).get_or_create(
        app_label="wagtailcore", model="page"
    )

    for app_label, model_name in [("home", "HomePage"), ("about_company", "AboutPage")]:
        model = apps.get_model(app_label, model_name)
        for page in model.objects.using(db_alias).iterator():
            if page.alias_of_id:
                continue
            # 0004 already updated the page tables. Record their historical state;
            # calling current save_revision/publish would query future columns.
            revision = Revision.objects.using(db_alias).create(
                content_type_id=page.content_type_id,
                base_content_type_id=base_content_type.pk,
                object_id=str(page.pk),
                object_str=page.title,
                created_at=timezone.now(),
                content=serialize_page(page, db_alias),
            )
            updates = {
                "latest_revision_id": revision.pk,
                "latest_revision_created_at": revision.created_at,
                "draft_title": page.title,
                "has_unpublished_changes": not page.live,
            }
            if page.live:
                updates["live_revision_id"] = revision.pk
            Page.objects.using(db_alias).filter(pk=page.pk).update(**updates)


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

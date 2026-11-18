from django.db import migrations


def move_content_pages(apps, schema_editor):
    from wagtail.models import Page

    database = schema_editor.connection.alias
    old_page = apps.get_model("home", "HeroFeaturePage")
    old_index = apps.get_model("home", "HeroFeatureIndexPage")
    new_page = apps.get_model("content_pages", "ContentPage")
    content_types = apps.get_model("contenttypes", "ContentType").objects.using(database)
    pages = Page.objects.using(database)
    quote = schema_editor.quote_name

    columns = ", ".join(quote(column) for column in (
        "page_ptr_id", "headline", "intro", "content", "image_id",
    ))
    schema_editor.execute(
        f"INSERT INTO {quote(new_page._meta.db_table)} ({columns}) "
        f"SELECT {columns} FROM {quote(old_page._meta.db_table)}"
    )
    # Keep the content type ID as well as page IDs, including for revisions.
    content_types.filter(app_label="home", model="herofeaturepage").update(
        app_label="content_pages", model="contentpage",
    )

    index_ids = list(old_index.objects.using(database).values_list("pk", flat=True))
    base_type, _ = content_types.get_or_create(app_label="wagtailcore", model="page")
    for index_id in index_ids:
        index = pages.get(pk=index_id)
        parent = index.get_parent()
        for child in list(index.get_children()):
            # A previous move can change the paths of the remaining siblings.
            child.refresh_from_db()
            slugs = set(parent.get_children().values_list("slug", flat=True))
            if child.slug in slugs:
                suffix = 2
                while f"{child.slug[: 254 - len(str(suffix))]}-{suffix}" in slugs:
                    suffix += 1
                slug = f"{child.slug[: 254 - len(str(suffix))]}-{suffix}"
                pages.filter(pk=child.pk).update(slug=slug)
                child.slug = slug
            child.move(parent, pos="last-child")

        # Drop the obsolete subtype row before deleting its base page.
        schema_editor.execute(
            f"DELETE FROM {quote(old_index._meta.db_table)} WHERE page_ptr_id = %s",
            [index_id],
        )
        pages.filter(pk=index_id).update(content_type_id=base_type.pk)
        pages.get(pk=index_id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("content_pages", "0001_initial"),
        ("home", "0029_citypage_buttons_alter_citypage_content"),
        ("wagtailredirects", "0008_add_verbose_name_plural"),
    ]

    operations = [migrations.RunPython(move_content_pages)]

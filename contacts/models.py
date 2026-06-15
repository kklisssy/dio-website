from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from base.page_blocks import RichTextSectionBlock


class ContactPage(Page):
    template = "contacts/contact_page.html"

    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Контакты",
    )
    city = models.CharField(
        "Город",
        max_length=100,
        default="Тюмень",
    )
    phone = models.CharField(
        "Телефон",
        max_length=50,
        blank=True,
    )
    email = models.EmailField(
        "Email",
        blank=True,
    )
    address = models.TextField(
        "Адрес",
        blank=True,
    )
    map_embed_url = models.URLField(
        "Ссылка iframe-карты",
        blank=True,
        help_text="Например src из iframe Яндекс.Карт",
    )

    social_links = StreamField(
        [
            ("social", blocks.StructBlock([
                ("name", blocks.CharBlock(label="Название")),
                ("url", blocks.URLBlock(label="Ссылка")),
                ("icon", ImageChooserBlock(required=False, label="Иконка")),
            ], label="Соцсеть")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Соцсети",
    )

    content = StreamField(
        [
            ("rich_text", RichTextSectionBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Содержимое страницы",
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("headline"),
        MultiFieldPanel(
            [
                FieldPanel("city"),
                FieldPanel("map_embed_url"),
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("address"),
            ],
            heading="Контактная информация",
        ),
        FieldPanel("social_links"),
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

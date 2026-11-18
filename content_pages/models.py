from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from base.page_blocks import ButtonBlock, FeaturesBlock, RichTextSectionBlock, TableSectionBlock


class ContentPage(Page):
    """Универсальная контентная страница."""

    template = "content_pages/content_page.html"

    headline = models.CharField(
        "Заголовок",
        max_length=255,
        blank=True,
        help_text="Если оставить пустым, будет использовано название страницы.",
    )
    intro = models.TextField(
        "Краткое описание",
        blank=True,
        help_text="Вводный текст для первого экрана.",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение",
    )
    buttons = StreamField(
        [("button", ButtonBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Кнопки",
    )
    content = StreamField(
        [
            ("text_section", RichTextSectionBlock()),
            ("table", TableSectionBlock()),
            ("features", FeaturesBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Содержимое страницы",
    )

    content_panels = [
        *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel("headline"),
                FieldPanel("intro"),
                FieldPanel("image"),
                FieldPanel("buttons"),
            ],
            heading="Основная информация",
        ),
        FieldPanel("content"),
    ]

    parent_page_types = [
        "home.HomePage",
        "cases.CaseIndexPage",
        "services.ServiceIndexPage",
        "services_1C.Service1CIndexPage",
        "products.ProductIndexPage",
        "practice.PracticeIndexPage",
    ]
    subpage_types = []

    class Meta:
        verbose_name = "Контентная страница"
        verbose_name_plural = "Контентные страницы"

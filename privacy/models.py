from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField
from wagtail.models import Page


class PrivacyPolicyPage(Page):
    """Страница политики конфиденциальности."""

    template = "privacy/privacy_page.html"

    content = StreamField(
        [
            (
                "text",
                blocks.RichTextBlock(
                    features=["h2", "h3", "h4", "bold", "italic", "link", "ol", "ul"],
                    label="Текст",
                ),
            ),
            ("table", TableBlock(label="Таблица")),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Содержимое страницы",
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"

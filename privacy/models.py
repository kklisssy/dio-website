from typing import ClassVar

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from base.page_blocks import RichTextSectionBlock, TableSectionBlock


class LegalDocumentPage(Page):
    """Страница политики конфиденциальности."""

    template = "privacy/document_page.html"

    content = StreamField(
        [
            ("text_section", RichTextSectionBlock()),
            ("table", TableSectionBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Содержимое страницы",
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("content"),
    ]

    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]
    subpage_types: ClassVar[list[str]] = []

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

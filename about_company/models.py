from typing import ClassVar

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from base.page_blocks import FeaturesBlock, RichTextSectionBlock
from home.models import MainAchievementBlock, PartnershipBlock, WorkWithBlock


class AchievementsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Наши достижения в цифрах",
        label="Заголовок",
    )
    intro = blocks.RichTextBlock(
        required=False,
        features=["bold", "italic", "link"],
        label="Описание",
    )
    items = blocks.ListBlock(
        MainAchievementBlock(),
        min_num=1,
        label="Достижения",
    )

    class Meta:
        icon = "pick"
        label = "Достижения"


# Секция этапов работы
class WorkStageItemBlock(blocks.StructBlock):
    """Блок для одного этапа работы"""

    title = blocks.CharBlock(max_length=120, label="Название этапа")
    text = blocks.TextBlock(label="Описание этапа")

    class Meta:
        icon = "list-ol"
        label = "Этап работы"


class WorkStagesBlock(blocks.StructBlock):
    """Блок для секции этапов работы"""

    title = blocks.CharBlock(
        required=True,
        default="Как мы работаем",
        label="Заголовок",
    )
    intro = blocks.TextBlock(
        required=False,
        label="Описание",
    )
    stages = blocks.ListBlock(
        WorkStageItemBlock(),
        min_num=1,
        label="Этапы",
    )

    class Meta:
        icon = "list-ol"
        label = "Этапы работы"


class CertificateItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, label="Изображение сертификата")
    title = blocks.CharBlock(required=False, label="Название")
    description = blocks.TextBlock(required=False, label="Описание")
    file = DocumentChooserBlock(required=False, label="Файл")

    class Meta:
        icon = "doc-full"
        label = "Сертификат"


class CertificatesBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Сертификаты",
        label="Заголовок",
    )
    intro = blocks.RichTextBlock(
        required=False,
        features=["bold", "italic", "link"],
        label="Описание",
    )
    items = blocks.ListBlock(
        CertificateItemBlock(),
        min_num=1,
        label="Сертификаты",
    )

    class Meta:
        icon = "doc-full"
        label = "Сертификаты"



class AboutPage(Page):
    hero_label = models.CharField(
        "Лейбл hero",
        max_length=120,
        default="О компании",
        blank=True,
    )
    headline = models.CharField("Заголовок", max_length=255, blank=True)
    intro = models.TextField("Описание", blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Фоновое изображение hero",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
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
    )

    content_panels: ClassVar[list[object]] = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_label"),
                FieldPanel("headline"),
                FieldPanel("intro"),
                FieldPanel("hero_image"),
            ],
            heading="Hero",
        ),
        FieldPanel("content"),
    ]

    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]
    subpage_types: ClassVar[list[str]] = []

    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "Страницы о компании"

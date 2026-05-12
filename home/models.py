from wagtail.models import Page
from django.db import models
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField, RichTextField

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField


# Hero блок
class HeroButtonBlock(blocks.StructBlock):
    """Блок для отображения кнопок слайда hero"""

    text = blocks.CharBlock(max_length=50, required=True, label="Текст кнопки")
    url = blocks.URLBlock(required=True, label="Ссылка")
    is_secondary = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Вторичная кнопка",
    )


class HeroBlock(blocks.StructBlock):
    """Блок для hero"""

    title = blocks.TextBlock(
        required=True,
        label="Заголовок",
    )
    text = blocks.RichTextBlock(
        required=False,
        features=["bold", "italic", "link"],
        label="Описание",
    )
    buttons = blocks.ListBlock(
        HeroButtonBlock(),
        required=True,
        max_num=2,
        label="Кнопки",
    )
    image = ImageChooserBlock(required=True, label="Большое изображение")

    class Meta:
        icon = "image"
        label = "Hero секция"


#Секция достижений
class MainAchievementBlock(blocks.StructBlock):
    """Блок для основного достижения"""

    icon = ImageChooserBlock(
        required=False,
        label="Иконка",
        help_text="Выберите изображение для иконки (рекомендуемый размер: 50x50px)",
    )
    value = blocks.IntegerBlock(default=0, label="Числовое значение")
    suffix = blocks.CharBlock(
        max_length=10, blank=True, default="+", label="Суффикс (например, '+' или '%')"
    )
    label = blocks.CharBlock(max_length=100, label="Краткое название")
    description = blocks.RichTextBlock(blank=True, label="Описание достижения")

    class Meta:
        icon = "tick"
        label = "Достижение"


#Секция "С кем мы работаем"
class WorkWithCardBlock(blocks.StructBlock):
    """Блок для карточки отрасли работы"""

    image = ImageChooserBlock(label="Изображение")
    title = blocks.CharBlock(label="Название")
    text = blocks.RichTextBlock(label="Описание", features=["bold", "italic", "link"])

class WorkWithBlock(blocks.StructBlock):
    """Блок для отраслей работы"""

    title = blocks.CharBlock(
        label="Заголовок",
        default="С кем мы работаем",
    )
    intro = blocks.RichTextBlock(
        label="Описание",
        required=False,
        features=["bold", "italic", "link"],
    )
    cards = blocks.ListBlock(
        WorkWithCardBlock(),
        label="Карточки",
        min_num=1
    )

    class Meta:
        icon = "group"
        label = "С кем мы работаем"

#Секция клиентов
class PartnerLogoBlock(blocks.StructBlock):
    """Блок для логотипа партнёра"""

    logo = ImageChooserBlock(
        required=True,
        label="Логотип партнёра",
        help_text="Рекомендуемый размер: 54x16px",
    )
    link = blocks.URLBlock(required=False, label="Ссылка на партнёра")

    class Meta:
        icon = "image"
        label = "Логотип партнёра"


class PartnershipBlock(blocks.StructBlock):
    """Блок для секции с партнёрствами"""

    headline = blocks.CharBlock(required=True, label="Заголовок секции")
    subheadline = blocks.CharBlock(required=True, label="Подзаголовок секции")
    logos = blocks.ListBlock(
        PartnerLogoBlock(),
        min_num=1,
        label="Логотипы партнёров",
    )

    class Meta:
        icon = "group"
        label = "Секция партнёрств"


#Глобальное присутсвие
class GlobalPresenceBlock(blocks.StructBlock):
    """Блок для секции глобальное присутсвие"""

    title = blocks.CharBlock(
        required=True,
        default="Глобальное присутствие",
        label="Заголовок"
    )
    description = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "link", "superscript"],
        required=False,
        label="Описание"
    )
    image = ImageChooserBlock(
        required=True,
        label="Изображение для локации",
        help_text="Рекомендуемый размер: квадратное или 1x1"
    )


class HomePage(Page):
    """Главная страница"""

    hero = StreamField([
        ("hero", HeroBlock())],
        blank=True,
        max_num=1,
        use_json_field=True,
        verbose_name="Hero секция",
    )

    achievements = StreamField(
        [("achievement", MainAchievementBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Достижения",
    )

    work = StreamField(
        [("work_with", WorkWithBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Секция с кем мы работаем",
    )

    partners = StreamField(
        [("partner", PartnershipBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Секция партнёрств",
    )

    global_presence = StreamField(
        [('presence', GlobalPresenceBlock())],
        use_json_field=True,
        blank=True,
        max_num=1,
        verbose_name="Глобальное присутствие"
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero'),
        FieldPanel('achievements'),
        FieldPanel('work'),
        FieldPanel('partners'),
        FieldPanel('global_presence'),
    ]

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"

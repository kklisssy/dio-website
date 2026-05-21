from typing import ClassVar

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index

SERVICE_CATEGORY_CHOICES = [
    ("consulting", "Консультации"),
    ("development", "Разработка"),
    ("support", "Поддержка"),
    ("training", "Обучение"),
    ("1_c", "1С"),
]

RICH_TEXT_FEATURES = [
    "h2",
    "h3",
    "bold",
    "italic",
    "link",
    "ol",
    "ul",
    "blockquote",
]


class RichTextSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label="Заголовок")
    text = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Текст")

    class Meta:
        icon = "doc-full"
        label = "Текстовая секция"


class ListItemBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, label="Текст пункта")

    class Meta:
        icon = "list-ul"
        label = "Пункт списка"


class SimpleListBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        label="Заголовок блока",
    )
    items = blocks.ListBlock(ListItemBlock(), label="Пункты")

    class Meta:
        icon = "list-ul"
        label = "Обычный список"


class FeatureItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Заголовок")
    text = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul"],
        required=False,
        label="Описание",
    )
    icon = ImageChooserBlock(required=False, label="Иконка")

    class Meta:
        icon = "tick"
        label = "Пункт"


class FeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Преимущества",
        label="Заголовок блока",
    )
    items = blocks.ListBlock(FeatureItemBlock(), label="Список пунктов")

    class Meta:
        icon = "tasks"
        label = "Преимущества"


class StepItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Название этапа")
    text = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul"],
        required=False,
        label="Описание этапа",
    )

    class Meta:
        icon = "order"
        label = "Этап"


class StepsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Как мы работаем",
        label="Заголовок блока",
    )
    items = blocks.ListBlock(StepItemBlock(), label="Этапы")

    class Meta:
        icon = "cog"
        label = "Этапы работы"


class ImageTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Заголовок")
    text = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Текст")
    image = ImageChooserBlock(required=False, label="Изображение")
    image_position = blocks.ChoiceBlock(
        choices=[
            ("left", "Слева"),
            ("right", "Справа"),
        ],
        default="left",
        label="Позиция изображения",
    )

    class Meta:
        icon = "image"
        label = "Текст с изображением"


class FaqItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, label="Вопрос")
    answer = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Ответ")

    class Meta:
        icon = "help"
        label = "Вопрос"


class FaqBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Вопросы и ответы",
        label="Заголовок блока",
    )
    items = blocks.ListBlock(FaqItemBlock(), label="Вопросы")

    class Meta:
        icon = "help"
        label = "FAQ"


class SingleServicePage(Page):
    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.CharField(
        max_length=100,
        choices=SERVICE_CATEGORY_CHOICES,
        default="consulting",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Заголовок услуги",
    )
    intro = models.TextField(
        "Краткое описание",
        blank=True,
        help_text="1-3 предложения для анонса и первого экрана",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение",
    )
    content = StreamField(
        [
            ("text_section", RichTextSectionBlock()),
            ("simple_list", SimpleListBlock()),
            ("features", FeaturesBlock()),
            ("steps", StepsBlock()),
            ("image_text", ImageTextBlock()),
            ("faq", FaqBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Содержимое страницы",
    )

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("category"),
                FieldPanel("headline"),
                FieldPanel("intro"),
                FieldPanel("image"),
            ],
            heading="Основная информация",
        ),
        FieldPanel("content"),
    ]

    search_fields: ClassVar[list[object]] = [
        *Page.search_fields,
        index.SearchField("headline"),
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    parent_page_types: ClassVar[list[str]] = ["services.ServiceIndexPage"]
    subpage_types: ClassVar[list[str]] = []

    def get_context(self, request):
        context = super().get_context(request)
        context["other_services"] = (
            SingleServicePage.objects.live().exclude(id=self.id).order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class ServiceIndexPage(Page):
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Услуги",
    )
    intro = RichTextField(
        "Введение",
        features=["bold", "italic", "link"],
        blank=True,
    )
    items_per_page = models.PositiveIntegerField("Услуг на странице", default=9)

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        FieldPanel("headline"),
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types: ClassVar[list[str]] = ["services.SingleServicePage"]
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        services = SingleServicePage.objects.live().order_by("-date")

        category = request.GET.get("category")
        categories = dict(SERVICE_CATEGORY_CHOICES)

        if category and category in categories:
            services = services.filter(category=category)
            context["current_category"] = category
        else:
            context["current_category"] = None

        paginator = Paginator(services, self.items_per_page)
        page = request.GET.get("page")

        try:
            services_page = paginator.page(page)
        except PageNotAnInteger:
            services_page = paginator.page(1)
        except EmptyPage:
            services_page = paginator.page(paginator.num_pages)

        context["services"] = services_page
        context["service_categories"] = SERVICE_CATEGORY_CHOICES
        return context

    class Meta:
        verbose_name = "Лента услуг"
        verbose_name_plural = "Ленты услуг"


class ServiceBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Заголовок секции услуг",
    )
    show_count = blocks.IntegerBlock(
        default=3,
        min_value=1,
        max_value=12,
        label="Количество услуг для показа",
    )

    class Meta:
        icon = "doc-full"
        label = "Блок услуг"

from typing import ClassVar

from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from base.page_blocks import FeaturesBlock, RichTextSectionBlock, TableSectionBlock


@register_snippet
class Service1CCategory(models.Model):
    name = models.CharField("Название", max_length=100)
    value = models.SlugField("Значение для URL", max_length=100, unique=True)

    panels: ClassVar[list[object]] = [
        FieldPanel("name"),
        FieldPanel("value"),
    ]

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория 1С"
        verbose_name_plural = "Категории 1С"

    def __str__(self):
        return self.name


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="Оставить заявку на подключение сервиса",
        label="Заголовок",
    )
    text = blocks.TextBlock(
        required=False,
        label="Описание",
    )
    button_text = blocks.CharBlock(
        required=True,
        default="Отправить",
        max_length=100,
        label="Текст кнопки",
    )
    button_url = blocks.CharBlock(
        required=False,
        default="#contacts",
        max_length=200,
        label="Ссылка кнопки",
        help_text="Например: #contacts или /contacts/",
    )

    class Meta:
        icon = "mail"
        label = "Заявка на подключение"


class SingleService1CPage(Page):
    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.ForeignKey(
        "services_1C.Service1CCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="services_1c",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Заголовок продукта 1C",
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
            ("table", TableSectionBlock()),
            ("features", FeaturesBlock()),
            ("cta", CallToActionBlock()),
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

    parent_page_types: ClassVar[list[str]] = ["services_1C.Service1CIndexPage"]
    subpage_types: ClassVar[list[str]] = []

    template = "services_1C/single_service_1C_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["other_services_1c"] = (
            SingleService1CPage.objects.live()
            .child_of(self.get_parent())
            .select_related("category")
            .exclude(id=self.id)
            .order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Решение 1С"
        verbose_name_plural = "Решения 1С"


class Service1CIndexPage(Page):
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Сервисы 1С",
    )
    intro = RichTextField(
        "Введение",
        features=["bold", "italic", "link"],
        blank=True,
    )
    items_per_page = models.PositiveIntegerField("Сервисов на странице", default=9)

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        FieldPanel("headline"),
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types: ClassVar[list[str]] = ["services_1C.SingleService1CPage"]
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]

    template = "services_1C/service_1C_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        services_1c = (
            SingleService1CPage.objects.live()
            .child_of(self)
            .select_related("category")
            .order_by("-date")
        )
        category = request.GET.get("category")
        categories = Service1CCategory.objects.filter(
            services_1c__in=services_1c
        ).distinct()

        if category and categories.filter(value=category).exists():
            services_1c = services_1c.filter(category__value=category)
            context["current_category"] = category
        else:
            context["current_category"] = None

        context["services_1c"] = Paginator(services_1c, self.items_per_page).get_page(
            request.GET.get("page")
        )
        context["service_1c_categories"] = categories
        return context

    class Meta:
        verbose_name = "Лента решений 1С"
        verbose_name_plural = "Ленты решений 1С"

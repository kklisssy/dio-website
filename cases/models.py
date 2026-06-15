from typing import ClassVar

from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

INDUSTRY_CHOICES = [
    ("oil-gas", "Нефтегаз"),
    ("service_business", "Сервисный бизнес"),
    ("trading", "Торговля"),
    ("production", "Производство"),
]

RICH_TEXT_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "link",
    "ol",
    "ul",
    "blockquote",
]


class CaseTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label="Заголовок")
    text = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Текст")

    class Meta:
        icon = "doc-full"
        label = "Текстовая секция"


class MetricItemBlock(blocks.StructBlock):
    value = blocks.CharBlock(required=True, label="Значение")
    label = blocks.CharBlock(required=True, label="Описание")

    class Meta:
        icon = "pick"
        label = "Метрика"


class MetricsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Ключевые показатели",
        label="Заголовок блока",
    )
    items = blocks.ListBlock(MetricItemBlock(), label="Метрики")

    class Meta:
        icon = "date"
        label = "Ключевые показатели"


class ResultItemBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
        required=True,
        label="Текст результата",
    )

    class Meta:
        icon = "success"
        label = "Результат"


class ResultsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Результаты",
        label="Заголовок блока",
    )
    items = blocks.ListBlock(ResultItemBlock(), label="Список результатов")

    class Meta:
        icon = "tick"
        label = "Результаты"


class TechnologiesBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        default="Технологии",
        label="Заголовок блока",
    )
    items = blocks.ListBlock(blocks.CharBlock(label="Технология"), label="Список технологий")

    class Meta:
        icon = "code"
        label = "Технологии"


class SingleCasePage(Page):
    customer_name = models.CharField("Название компании-клиента", max_length=255)
    industry = models.CharField("Отрасль", max_length=100, choices=INDUSTRY_CHOICES)
    project_date = models.DateField("Дата реализации проекта", default=timezone.now)
    duration = models.CharField("Длительность проекта", max_length=50, blank=True)
    location = models.CharField("Местоположение", max_length=100, blank=True)
    customer_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Логотип клиента",
    )
    intro = RichTextField(
        "Краткое описание",
        features=["bold", "italic", "link"],
        blank=True,
        help_text="1-3 предложения для анонса",
    )
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Основное изображение",
    )
    content = StreamField(
        [
            ("text_section", CaseTextBlock()),
            ("metrics", MetricsBlock()),
            ("results", ResultsBlock()),
            ("technologies", TechnologiesBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Содержание кейса",
    )

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel("customer_name"),
                FieldPanel("industry"),
                FieldPanel("project_date"),
                FieldPanel("duration"),
                FieldPanel("location"),
                FieldPanel("customer_logo"),
                FieldPanel("main_image"),
            ],
            heading="Основная информация",
        ),
        FieldPanel("intro"),
        FieldPanel("content"),
    ]

    search_fields: ClassVar[list[object]] = [
        *Page.search_fields,
        index.SearchField("customer_name"),
        index.SearchField("intro"),
        index.SearchField("content"),
    ]

    parent_page_types: ClassVar[list[str]] = ["cases.CaseIndexPage"]
    subpage_types: ClassVar[list[str]] = []

    template = "cases/single_case_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["other_cases"] = (
            SingleCasePage.objects.live().exclude(id=self.id).order_by("-project_date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"


class CaseIndexPage(Page):
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Кейсы",
    )
    intro = RichTextField(
        "Введение",
        features=["bold", "italic", "link"],
        blank=True,
    )
    items_per_page = models.PositiveIntegerField("Кейсов на странице", default=9)

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        FieldPanel("headline"),
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types: ClassVar[list[str]] = ["cases.SingleCasePage"]
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]

    template = "cases/case_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        cases = SingleCasePage.objects.live().order_by("-project_date")

        industry = request.GET.get("industry")
        industries = dict(INDUSTRY_CHOICES)

        if industry and industry in industries:
            cases = cases.filter(industry=industry)
            context["current_industry"] = industry
        else:
            context["current_industry"] = None

        context["cases"] = Paginator(cases, self.items_per_page).get_page(
            request.GET.get("page")
        )
        context["industry_choices"] = INDUSTRY_CHOICES
        return context

    class Meta:
        verbose_name = "Лента кейсов"
        verbose_name_plural = "Ленты кейсов"

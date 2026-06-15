from typing import ClassVar

from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from base.page_blocks import FeaturesBlock, RichTextSectionBlock, TableSectionBlock


@register_snippet
class PracticeCategory(models.Model):
    name = models.CharField("Название", max_length=100)
    value = models.SlugField("Значение для URL", max_length=100, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    panels: ClassVar[list[object]] = [
        FieldPanel("name"),
        FieldPanel("value"),
        FieldPanel("order"),
    ]

    class Meta:
        ordering = ("order", "name")
        verbose_name = "Категория практики"
        verbose_name_plural = "Категории практики"

    def __str__(self):
        return self.name


class PracticeSinglePage(Page):
    template = "practice/practice_single_page.html"

    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.ForeignKey(
        "practice.PracticeCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Заголовок материала",
    )
    intro = models.TextField(
        "Короткое описание",
        blank=True,
        help_text="1-3 предложения для анонса и первого экрана",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Обложка",
    )
    document = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Документ",
        help_text="Можно прикрепить файл для чек-листа или методички",
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

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("category"),
                FieldPanel("headline"),
                FieldPanel("intro"),
                FieldPanel("image"),
                FieldPanel("document"),
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

    parent_page_types: ClassVar[list[str]] = ["practice.PracticeIndexPage"]
    subpage_types: ClassVar[list[str]] = []

    def get_context(self, request):
        context = super().get_context(request)
        context["other_articles"] = (
            PracticeSinglePage.objects.live()
            .select_related("category")
            .exclude(id=self.id)
            .order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Материал практики"
        verbose_name_plural = "Материалы практики"


class PracticeIndexPage(Page):
    template = "practice/practice_index_page.html"

    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Практика 1С",
    )
    intro = RichTextField(
        "Введение",
        features=["bold", "italic", "link"],
        blank=True,
    )
    items_per_page = models.PositiveIntegerField("Материалов на странице", default=9)

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        FieldPanel("headline"),
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types: ClassVar[list[str]] = ["practice.PracticeSinglePage"]
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        articles = (
            PracticeSinglePage.objects.live()
            .descendant_of(self)
            .select_related("category")
            .order_by("-date")
        )

        category = request.GET.get("category")
        categories = PracticeCategory.objects.all()

        if category and categories.filter(value=category).exists():
            articles = articles.filter(category__value=category)
            context["current_category"] = category
        else:
            context["current_category"] = None

        context["practice_articles"] = Paginator(articles, self.items_per_page).get_page(
            request.GET.get("page")
        )
        context["practice_categories"] = categories
        return context

    class Meta:
        verbose_name = "Лента практики 1С"
        verbose_name_plural = "Ленты практики 1С"

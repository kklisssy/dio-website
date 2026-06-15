from typing import ClassVar

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from base.page_blocks import FeaturesBlock, RichTextSectionBlock, TableSectionBlock


@register_snippet
class ProductCategory(models.Model):
    name = models.CharField("Название", max_length=100)
    value = models.SlugField("Значение для URL", max_length=100, unique=True)

    panels: ClassVar[list[object]] = [
        FieldPanel("name"),
        FieldPanel("value"),
    ]

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория продукта"
        verbose_name_plural = "Категории продуктов"

    def __str__(self):
        return self.name


class SingleProductPage(Page):
    date = models.DateField("Дата публикации", default=timezone.now)
    category = models.ForeignKey(
        "products.ProductCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
        verbose_name="Категория",
    )
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Заголовок продукта",
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
    price = models.CharField(
        "Цена",
        max_length=100,
        blank=True,
        help_text="Например: 94 700 руб.",
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
                FieldPanel("price"),
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
        index.SearchField("price"),
        index.SearchField("content"),
    ]

    parent_page_types: ClassVar[list[str]] = ["products.ProductIndexPage"]
    subpage_types: ClassVar[list[str]] = []

    template = "products/single_product_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["other_products"] = (
            SingleProductPage.objects.live()
            .child_of(self.get_parent())
            .select_related("category")
            .exclude(id=self.id)
            .order_by("-date")[:3]
        )
        return context

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductIndexPage(Page):
    headline = models.CharField(
        "Заголовок",
        max_length=255,
        default="Продукты",
    )
    intro = RichTextField(
        "Введение",
        features=["bold", "italic", "link"],
        blank=True,
    )
    items_per_page = models.PositiveIntegerField("Продуктов на странице", default=9)

    content_panels: ClassVar[list[object]] = [
        *Page.content_panels,
        FieldPanel("headline"),
        FieldPanel("intro"),
        FieldPanel("items_per_page"),
    ]

    subpage_types: ClassVar[list[str]] = ["products.SingleProductPage"]
    parent_page_types: ClassVar[list[str]] = ["home.HomePage"]

    template = "products/product_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        products = (
            SingleProductPage.objects.live()
            .child_of(self)
            .select_related("category")
            .order_by("-date")
        )

        category = request.GET.get("category")
        categories = ProductCategory.objects.filter(products__in=products).distinct()

        if category and categories.filter(value=category).exists():
            products = products.filter(category__value=category)
            context["current_category"] = category
        else:
            context["current_category"] = None

        paginator = Paginator(products, self.items_per_page)
        page = request.GET.get("page")

        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        context["products"] = products_page
        context["product_categories"] = categories
        return context

    class Meta:
        verbose_name = "Лента продуктов"
        verbose_name_plural = "Ленты продуктов"

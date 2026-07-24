from django.db import models
from django.shortcuts import redirect
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from base.page_blocks import FeaturesBlock, RichTextSectionBlock, TableSectionBlock, LinkedCardBlock


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

class HeroFeaturesBlock(blocks.StructBlock):
    """Блок для отображения свойств hero"""

    icon = ImageChooserBlock(required=False, label="Иконка")
    title = blocks.TextBlock(max_length=50, required=True, label="Заголовок свойства")
    description = blocks.TextBlock(max_length=200, required=False, label="Короткое описание")
    page = blocks.PageChooserBlock(
        required=False,
        page_type=["home.HeroFeaturePage"],
        label="Страница",
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


class DirectionCardBlock(LinkedCardBlock):
    """Карточка направления работ"""
    class Meta:
        label = "Карточка направления аудита"
        icon = "link"

class DirectionsBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        max_length=150,
        label="Заголовок",
    )

    description = blocks.TextBlock(
        required=False,
        max_length=300,
        label="Описание",
    )

    main_card = DirectionCardBlock(
        label="Главная карточка",
    )

    cards = blocks.ListBlock(DirectionCardBlock(), min_num=1, label="Дополнительные карточки")

    class Meta:
        icon = "tick"
        label = "Направления аудита"


class Service1CActionCardBlock(LinkedCardBlock):
    """Карточка подключения сервисов 1С"""
    class Meta:
        label = "Карточка подключения сервисов 1С"
        icon = "link"

class Service1CActionsBlock(blocks.StructBlock):
    """Блок для секции подключения сервисов 1С."""

    title = blocks.CharBlock(
        required=False,
        max_length=150,
        label="Заголовок",
    )

    description = blocks.TextBlock(
        required=False,
        max_length=300,
        label="Описание",
    )

    cards = blocks.ListBlock(Service1CActionCardBlock(), min_num=1, label="Карточки подключения")

    class Meta:
        icon = "tick"
        label = "Подключение сервисов 1С"


class WorkStageItemBlock(blocks.StructBlock):
    """Блок для одного этапа работы."""

    title = blocks.CharBlock(max_length=120, label="Название этапа")
    text = blocks.TextBlock(label="Описание этапа")
    page = blocks.PageChooserBlock(
        required=False,
        page_type=["home.WorkStagePage"],
        label="Страница этапа",
    )

    class Meta:
        icon = "list-ol"
        label = "Этап работы"


class WorkStagesBlock(blocks.StructBlock):
    """Блок для секции этапов работы."""

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


class HeroFeatureIndexPage(Page):
    """Служебный раздел для группировки страниц свойств."""

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.HeroFeaturePage"]
    max_count_per_parent = 1

    def serve(self, request, *args, **kwargs):
        return redirect(self.get_parent().url)

    class Meta:
        verbose_name = "Раздел свойств"
        verbose_name_plural = "Разделы свойств"


class HeroFeaturePage(Page):
    """Страница с подробным описанием свойства."""

    template = "home/content_detail_page.html"

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
            ],
            heading="Основная информация",
        ),
        FieldPanel("content"),
    ]

    parent_page_types = ["home.HeroFeatureIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Описание свойства"
        verbose_name_plural = "Описания свойств"


class WorkStageIndexPage(Page):
    """Служебный раздел для группировки страниц этапов работы."""

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.WorkStagePage"]
    max_count_per_parent = 1

    def serve(self, request, *args, **kwargs):
        return redirect(self.get_parent().url)

    class Meta:
        verbose_name = "Раздел этапов работы"
        verbose_name_plural = "Разделы этапов работы"


class WorkStagePage(Page):
    """Страница с подробным описанием этапа работы."""

    template = "home/content_detail_page.html"

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
            ],
            heading="Основная информация",
        ),
        FieldPanel("content"),
    ]

    parent_page_types = ["home.WorkStageIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Описание этапа работы"
        verbose_name_plural = "Описания этапов работы"


class HomePage(Page):
    """Главная страница"""

    hero = StreamField([
        ("hero", HeroBlock())],
        blank=True,
        max_num=1,
        use_json_field=True,
        verbose_name="Hero секция",
    )

    hero_features = StreamField(
        [("feature", HeroFeaturesBlock())],
        blank=False,
        default=list,
        use_json_field=True,
        verbose_name="Карточки под hero"
    )

    directions = StreamField(
        [("directions", DirectionsBlock())],
        blank=True,
        max_num=1,
        use_json_field=True,
        verbose_name="Направления аудита",
    )

    products_description = RichTextField(
        "Дополнительный текст секции решений",
        blank=True,
        features=["bold", "italic", "link", "ol", "ul"],
        help_text="Текст отображается только в секции решений.",
    )

    service_1c_actions = StreamField(
        [("actions", Service1CActionsBlock())],
        blank=True,
        max_num=1,
        use_json_field=True,
        verbose_name="Действия с сервисами 1С",
    )

    work_stages = StreamField(
        [("work_stages", WorkStagesBlock())],
        blank=True,
        max_num=1,
        use_json_field=True,
        verbose_name="Этапы работы",
    )

    work_with = StreamField(
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

    content_panels = [
        *Page.content_panels,
        FieldPanel('hero'),
        FieldPanel("hero_features"),
        FieldPanel('work_with'),
        FieldPanel("directions"),
        FieldPanel("products_description"),
        FieldPanel("service_1c_actions"),
        FieldPanel("work_stages"),
        FieldPanel('partners'),
        FieldPanel('global_presence'),
    ]

    def get_cases(self, count=6):
        from cases.models import SingleCasePage
        return SingleCasePage.objects.live().order_by("-project_date")[:count]

    def get_case_index(self):
        from cases.models import CaseIndexPage

        return CaseIndexPage.objects.live().child_of(self).first()

    def get_services(self):
        from services.models import SingleServicePage
        return SingleServicePage.objects.live().order_by("-date")

    def get_service_index(self):
        from services.models import ServiceIndexPage

        return ServiceIndexPage.objects.live().child_of(self).first()

    def get_service_1c_index(self):
        from services_1C.models import Service1CIndexPage

        return Service1CIndexPage.objects.live().child_of(self).first()

    def get_product_index(self):
        from products.models import ProductIndexPage

        return (
            ProductIndexPage.objects.live()
            .child_of(self)
            .filter(slug="products")
            .first()
        )

    def get_own_product_index(self):
        from products.models import ProductIndexPage

        return (
            ProductIndexPage.objects.live()
            .child_of(self)
            .filter(slug="own-products")
            .first()
        )

    def get_product_categories(self):
        from products.models import ProductCategory

        return ProductCategory.objects.all()

    def get_about_indicators(self):
        from about_company.models import AboutPage

        about_page = (
            AboutPage.objects.live()
            .descendant_of(self)
            .first()
        )
        if not about_page:
            return []

        return about_page.indicators

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"

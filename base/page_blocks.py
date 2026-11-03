from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock

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

class ButtonBlock(blocks.StructBlock):
    """Блок для отображения кнопок"""

    text = blocks.CharBlock(max_length=50, required=True, label="Текст кнопки")
    url = blocks.CharBlock(
        required=True,
        max_length=255,
        default="#contacts",
        label="Ссылка или якорь",
        help_text="Например: #contacts, /contacts/, https://example.com",
    )
    is_secondary = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Вторичная кнопка",
    )


class RichTextSectionBlock(blocks.StructBlock):
    """Блок для отображения рич текста"""

    title = blocks.CharBlock(required=False, label="Заголовок")
    text = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Текст")

    class Meta:
        icon = "doc-full"
        label = "Текстовая секция"


class TableSectionBlock(blocks.StructBlock):
    """Блок для отображения таблиц"""

    title = blocks.CharBlock(required=False, label="Заголовок")
    table = TableBlock(label="Таблица")

    class Meta:
        icon = "table"
        label = "Табличный блок"


class FeatureItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Заголовок")
    text = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES,
        required=False,
        label="Описание",
    )
    icon = ImageChooserBlock(required=False, label="Иконка")

    class Meta:
        icon = "tick"
        label = "Пункт"


class FeaturesBlock(blocks.StructBlock):
    """Блок для отображения преимуществ"""

    title = blocks.CharBlock(
        required=False,
        default="Преимущества",
        label="Заголовок блока",
    )
    description = blocks.TextBlock(required=False, label="Описание под заголовком")
    items = blocks.ListBlock(FeatureItemBlock(), label="Список пунктов")

    class Meta:
        icon = "tasks"
        label = "Преимущества"


class ImageGalleryItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=250, label="Заголовок")
    image = ImageChooserBlock(required=True, label="Изображение")

    class Meta:
        icon = "image"
        label = "Изображение"

class ImageGalleryBlock(blocks.StructBlock):
    """Блок для отображения галереи изображений"""

    title = blocks.CharBlock(required=False, max_length=250, label="Заголовок")
    description = blocks.TextBlock(required=False, label="Описание под заголовком")
    images = blocks.ListBlock(ImageGalleryItemBlock(), label="Карточки")

    class Meta:
        icon = "media"
        label = "Галерея изображений"

class RateItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Название тарифа")
    price = blocks.CharBlock(
        required=True,
        label="Цена",
        help_text="Например: от 5 000 ₽",
    )
    period = blocks.CharBlock(
        required=False,
        label="Период",
        help_text="Например: месяц. Знак / добавляется в шаблоне.",
    )
    description = blocks.RichTextBlock(
        required=False,
        features=RICH_TEXT_FEATURES,
        label="Описание",
    )

    class Meta:
        icon = "tick"
        label = "Тариф"


class RateBlock(blocks.StructBlock):
    """Блок для отображения тарифов"""

    title = blocks.CharBlock(required=False, label="Заголовок")
    description = blocks.TextBlock(required=False, label="Описание под заголовком")
    rates = blocks.ListBlock(RateItemBlock(),label="Список тарифов")

    class Meta:
        icon = "tick"
        label = "Тарифы"


class FaqItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, label="Вопрос")
    answer = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Ответ")

    class Meta:
        icon = "help"
        label = "Вопрос"


class FaqBlock(blocks.StructBlock):
    """Блок для отображения вопросов FAQ"""

    title = blocks.CharBlock(
        required=False,
        default="Вопросы и ответы",
        label="Заголовок блока",
    )
    description = blocks.TextBlock(required=False, label="Описание под заголовком")
    items = blocks.ListBlock(FaqItemBlock(), label="Вопросы")

    class Meta:
        icon = "help"
        label = "FAQ"

class ChecklistBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        label="Заголовок",
    )
    description = blocks.TextBlock(
        required=False,
        label="Описание под заголовком",
    )
    items = blocks.ListBlock(
        blocks.CharBlock(label="Текст пункта"),
        min_num=1,
        label="Пункты",
    )

    class Meta:
        icon = "list-ul"
        label = "Список с галочками"

class LinkedCardBlock(blocks.StructBlock):
    """Блок для типовой структуры карточек"""

    page = blocks.PageChooserBlock(
        required=True,
        label="Страница",
    )
    category = blocks.CharBlock(
        required=False,
        max_length=80,
        label="Категория",
    )
    title = blocks.CharBlock(
        required=True,
        max_length=150,
        label="Заголовок",
    )
    description = blocks.TextBlock(
        required=False,
        max_length=300,
        label="Описание",
    )
    image = ImageChooserBlock(
        required=False,
        label="Изображение",
    )
    link_text = blocks.CharBlock(
        required=False,
        max_length=80,
        default="Подробнее",
        label="Текст ссылки",
    )

    class Meta:
        icon = "link"
        label = "Карточка со ссылкой"

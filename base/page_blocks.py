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

class RichTextSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label="Заголовок")
    text = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, label="Текст")

    class Meta:
        icon = "doc-full"
        label = "Текстовая секция"


class TableSectionBlock(blocks.StructBlock):
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
    title = blocks.CharBlock(
        required=False,
        default="Преимущества",
        label="Заголовок блока",
    )
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
    title = blocks.CharBlock(required=False, max_length=250, label="Заголовок")
    images = blocks.ListBlock(ImageGalleryItemBlock(), label="Карточки")

    class Meta:
        icon = "media"
        label = "Галерея изображений"

class RateItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Заголовок")
    period = blocks.CharBlock(required=False, label="Период тарифа")

    price_title = blocks.CharBlock(required=False, label="Заголовок цены", default="Цена продления")
    price = blocks.CharBlock(required=True, label="Цена тарифа")
    button = ButtonBlock()

    rec_price_title = blocks.CharBlock(required=False, label="Заголовок рекомендованной цены", default="Рекомендованная цена")
    rec_price = blocks.TextBlock(required=False, label="Рекомендованная цена")

    class Meta:
        icon = "tick"
        label = "Тариф"


class RateBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label="Заголовок")
    rates = blocks.ListBlock(RateItemBlock(),label="Список тарифов")

    class Meta:
        icon = "tick"
        label = "Тарифы"

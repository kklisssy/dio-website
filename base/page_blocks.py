from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock

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


class TableSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label="Заголовок")
    table = TableBlock(label="Таблица")

    class Meta:
        icon = "table"
        label = "Табличный блок"


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

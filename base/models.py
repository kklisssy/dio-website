from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    PageChooserBlock,
    StructBlock,
    URLBlock,
)
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField


@register_setting
class HeaderSettings(BaseGenericSetting):
    """Настройки хедера сайта."""

    class Meta:
        verbose_name = "Хедер"
        verbose_name_plural = "Хедер"

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Логотип сайта (рекомендуемый размер: 40x40px)",
    )
    site_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Название сайта, отображаемое рядом с логотипом",
    )
    consultation_button_text = models.CharField(
        max_length=255,
        default="Оставить заявку",
        help_text="Текст кнопки консультации",
    )
    nav_items = StreamField(
        [
            (
                "nav_item",
                StructBlock(
                    [
                        (
                            "name",
                            CharBlock(
                                max_length=255,
                                required=True,
                                label="Название пункта*",
                                help_text="Название пункта меню",
                            ),
                        ),
                        (
                            "page",
                            PageChooserBlock(
                                required=False,
                                label="Страница",
                                help_text="Выберите страницу для ссылки",
                            ),
                        ),
                        (
                            "external_url",
                            URLBlock(
                                required=False,
                                label="Внешняя ссылка",
                                help_text="Укажите внешний URL, если страница не выбрана",
                            ),
                        ),
                        (
                            "menu_type",
                            ChoiceBlock(
                                choices=[
                                    ("none", "Без подменю"),
                                    ("simple", "Простое подменю"),
                                ],
                                default="none",
                                label="Тип меню*",
                                help_text="Выберите тип подменю",
                            ),
                        ),
                        (
                            "simple_dropdown_items",
                            ListBlock(
                                StructBlock(
                                    [
                                        (
                                            "name",
                                            CharBlock(
                                                max_length=255,
                                                required=True,
                                                label="Название подпункта*",
                                                help_text="Название подпункта",
                                            ),
                                        ),
                                        (
                                            "page",
                                            PageChooserBlock(
                                                required=False,
                                                label="Страница",
                                                help_text="Выберите страницу для ссылки",
                                            ),
                                        ),
                                        (
                                            "external_url",
                                            URLBlock(
                                                required=False,
                                                label="Внешняя ссылка",
                                                help_text="Укажите внешний URL, если страница не выбрана",
                                            ),
                                        ),
                                    ]
                                ),
                                required=False,
                                label="Элементы подменю",
                                help_text="Используется для типа 'Простое подменю'",
                            ),
                        ),
                    ],
                    icon="list-ul",
                    label="Пункт меню",
                ),
            )
        ],
        use_json_field=True,
        blank=True,
        default=list,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("site_title"),
                FieldPanel("consultation_button_text"),
                FieldPanel("nav_items"),
            ],
            heading="Основные настройки хедера",
        ),
    ]

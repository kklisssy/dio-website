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

@register_setting
class ContactSettings(BaseGenericSetting):

    title = models.CharField(
        max_length=255,
        default="Обсудим ваш проект на базе 1С",
        verbose_name="Заголовок",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Телефон",
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Адрес",
    )
    working_hours = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Режим работы",
    )

    form_title = models.CharField(
        max_length=255,
        default="Получить консультацию",
        verbose_name="Заголовок формы",
    )

    submit_button_text = models.CharField(
        max_length=100,
        default="Отправить заявку",
        verbose_name="Текст кнопки",
    )

    form_note = models.CharField(
        max_length=255,
        default="Ответим и предложим следующий шаг по проекту.",
        verbose_name="Текст рядом с кнопкой",
    )

    privacy_policy_text = models.TextField(
        default="Нажимая кнопку, вы соглашаетесь с <a href='/privacy-policy/'>политикой обработки персональных данных</a>",
        verbose_name="Текст политики конфиденциальности"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("description"),
            ],
            heading="Основной текст",
        ),
        MultiFieldPanel(
            [
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("address"),
                FieldPanel("working_hours"),
            ],
            heading="Контакты",
        ),
        MultiFieldPanel(
            [
                FieldPanel("form_title"),
                FieldPanel("submit_button_text"),
                FieldPanel("form_note"),
                FieldPanel("privacy_policy_text"),
            ],
            heading="Форма консультации",
        ),
    ]

    class Meta:
        verbose_name = "Контакты"


class ConsultationRequest(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    company = models.CharField(max_length=255, blank=True, verbose_name="Компания")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    message = models.TextField(verbose_name="Краткое описание задачи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультацию"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.phone}"


from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from wagtail.models import Page, Site

from base.models import ContactSettings, FooterSettings, HeaderSettings
from home.models import HomePage


class Command(BaseCommand):
    help = "Create the initial Wagtail home page and baseline global settings."

    def handle(self, *args, **options):
        Page.fix_tree(destructive=False)
        root_page = Page.get_first_root_node()
        home_page, created = self._get_or_create_home_page(root_page)
        self._remove_default_welcome_page(root_page, home_page)
        self._set_default_site_root(home_page)
        self._bootstrap_header_settings()
        self._bootstrap_contact_settings()
        self._bootstrap_footer_settings()

        if created:
            self.stdout.write(self.style.SUCCESS("Home page created and set as site root."))
        else:
            self.stdout.write("Home page already exists; site root checked.")

    def _get_or_create_home_page(self, root_page):
        home_page = self._find_existing_home_page(root_page)
        if home_page:
            self._normalize_home_page(home_page)
            self._move_home_to_root(root_page, home_page)
            return home_page, False

        existing_home = root_page.get_children().filter(slug="home").first()
        if existing_home:
            specific_home = existing_home.specific
            if isinstance(specific_home, HomePage):
                return specific_home, False

            if self._is_disposable_default_page(existing_home):
                existing_home.delete()
                root_page.refresh_from_db()
                Page.fix_tree(destructive=False)
                root_page.refresh_from_db()
                self.stdout.write("Default Wagtail home slug removed.")
            else:
                raise CommandError(
                    "Slug 'home' is already used by a non-empty root page. "
                    "Move or remove that page before bootstrapping the site."
                )

        return self._create_home_page(root_page, slug="home"), True

    def _find_existing_home_page(self, root_page):
        root_home_page = HomePage.objects.child_of(root_page).order_by("path").first()
        if root_home_page:
            return root_home_page

        default_site = Site.objects.filter(is_default_site=True).first()
        if default_site and isinstance(default_site.root_page.specific, HomePage):
            return default_site.root_page.specific

        return HomePage.objects.order_by("path").first()

    def _normalize_home_page(self, home_page):
        changed = False
        if home_page.title in {
            "Главная страница",
            "Р“Р»Р°РІРЅР°СЏ СЃС‚СЂР°РЅРёС†Р°",
        }:
            home_page.title = "Главная"
            changed = True

        if not home_page.live:
            home_page.live = True
            changed = True

        if changed:
            home_page.save_revision().publish()

    def _move_home_to_root(self, root_page, home_page):
        if home_page.get_parent().id == root_page.id:
            return

        existing_home = root_page.get_children().filter(slug=home_page.slug).first()
        if existing_home and existing_home.id != home_page.id:
            if self._is_default_welcome_page(existing_home):
                existing_home.slug = "wagtail-welcome"
                existing_home.save()
            else:
                raise CommandError(
                    "Cannot move HomePage to root because another non-empty root page "
                    f"already uses slug '{home_page.slug}'."
                )

        home_page.move(root_page, pos="last-child")
        home_page.refresh_from_db()

    def _create_home_page(self, root_page, slug):
        root_page.refresh_from_db()
        home_page = HomePage(
            title="Главная",
            slug=slug,
            show_in_menus=True,
        )
        root_page.add_child(instance=home_page)
        home_page.save_revision().publish()
        return home_page

    def _is_disposable_default_page(self, page):
        return self._is_default_welcome_page(page) and not page.get_children().exists()

    def _is_default_welcome_page(self, page):
        return page.title == "Welcome to your new Wagtail site!"

    def _remove_default_welcome_page(self, root_page, home_page):
        root_page.refresh_from_db()
        welcome_pages = root_page.get_children().filter(
            title="Welcome to your new Wagtail site!"
        )
        for page in welcome_pages.exclude(id=home_page.id):
            if page.get_children().exists():
                raise CommandError(
                    "Default Wagtail welcome page still has child pages. "
                    "Move those pages under HomePage before bootstrapping the site."
                )
            page.delete()
            self.stdout.write("Default Wagtail welcome page removed.")

        Page.fix_tree(destructive=False)
        root_page.refresh_from_db()

    def _set_default_site_root(self, home_page):
        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if not site:
            Site.objects.create(
                hostname="localhost",
                port=80,
                root_page=home_page,
                is_default_site=True,
                site_name="DIO Website",
            )
            return

        changed = False
        if site.root_page_id != home_page.id:
            site.root_page = home_page
            changed = True
        if not site.is_default_site:
            site.is_default_site = True
            changed = True
        if changed:
            site.save()

    def _bootstrap_header_settings(self):
        settings = self._get_or_create_setting(HeaderSettings)
        changed = False

        if not settings.site_title:
            settings.site_title = "ДИО-Консалт"
            changed = True
        if not settings.consultation_button_text:
            settings.consultation_button_text = "Оставить заявку"
            changed = True

        if changed:
            settings.save()

    def _bootstrap_contact_settings(self):
        settings = self._get_or_create_setting(ContactSettings)
        values = {
            "title": "Обсудим ваш проект на базе 1С",
            "description": (
                "Расскажите какую задачу нужно решить: внедрение сопровождение, "
                "развитие, интеграция или обучение."
            ),
            "phone": "+7(345)250-06-90",
            "email": "info@diocon.ru",
            "address": "г. Тюмень, ул. Салтыкова-Щедрина, д. 58/1",
            "working_hours": "Пн-Пт: 9:00 - 18:00, Сб-Вс: по договоренности",
            "form_title": "Получить консультацию",
            "submit_button_text": "Отправить заявку",
        }

        changed = False
        for field, value in values.items():
            if not getattr(settings, field):
                setattr(settings, field, value)
                changed = True

        if settings.form_note:
            settings.form_note = ""
            changed = True

        if changed:
            settings.save()

    def _bootstrap_footer_settings(self):
        settings = self._get_or_create_setting(FooterSettings)
        changed = False

        if not settings.footer_button:
            settings.footer_button = "Связаться с нами"
            changed = True
        if not settings.footer_button_href:
            settings.footer_button_href = "#contacts"
            changed = True
        if not settings.bottom_links:
            settings.bottom_links = [
                (
                    "link",
                    {
                        "text": "Политика конфиденциальности",
                        "url": "/privacy-policy/",
                        "page": None,
                    },
                )
            ]
            changed = True

        if changed:
            settings.save()

    def _get_or_create_setting(self, model):
        return model.objects.first() or model.objects.create()

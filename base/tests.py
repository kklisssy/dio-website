from django.test import SimpleTestCase, TestCase

from base.templatetags.mega_menu import build_mega_menu
from cases.models import CaseIndexPage, CaseIndustry
from practice.models import PracticeCategory, PracticeIndexPage
from products.models import ProductCategory, ProductIndexPage
from services.models import ServiceCategory, ServiceIndexPage
from services_1C.models import Service1CCategory, Service1CIndexPage


class MegaMenuHelperTests(TestCase):
    class PageStub:
        def __init__(self, specific_class, url):
            self.specific_class = specific_class
            self.url = url

    class ContactSettingsStub:
        phone = "+7 000 000-00-00"
        email = "info@example.com"
        address = "Test address"

    def test_builds_service_category_panel(self):
        ServiceCategory.objects.create(name="Audit", value="audit")
        nav_item = {
            "mega_menu_items": [
                {
                    "name": "Services",
                    "description": "",
                    "page": self.PageStub(ServiceIndexPage, "/services/"),
                    "external_url": "",
                }
            ]
        }

        menu = build_mega_menu(nav_item)

        self.assertEqual(menu["panels"][0]["title"], "Направления услуг")
        self.assertEqual(menu["panels"][0]["items"][0]["url"], "/services/?category=audit")

    def test_builds_all_supported_category_panels(self):
        Service1CCategory.objects.create(name="ERP", value="erp")
        ProductCategory.objects.create(name="Custom", value="custom")
        PracticeCategory.objects.create(name="Guides", value="guides")
        CaseIndustry.objects.create(name="Retail", value="retail")

        nav_item = {
            "mega_menu_items": [
                {
                    "name": "1C",
                    "page": self.PageStub(Service1CIndexPage, "/1c/"),
                    "external_url": "",
                },
                {
                    "name": "Products",
                    "page": self.PageStub(ProductIndexPage, "/products/"),
                    "external_url": "",
                },
                {
                    "name": "Practice",
                    "page": self.PageStub(PracticeIndexPage, "/practice/"),
                    "external_url": "",
                },
                {
                    "name": "Cases",
                    "page": self.PageStub(CaseIndexPage, "/cases/"),
                    "external_url": "",
                },
            ]
        }

        menu = build_mega_menu(nav_item)

        self.assertEqual(
            [panel["items"][0]["url"] for panel in menu["panels"]],
            [
                "/1c/?category=erp",
                "/products/?category=custom",
                "/practice/?category=guides",
                "/cases/?industry=retail",
            ],
        )


class MegaMenuHelperSimpleTests(SimpleTestCase):
    class PageStub:
        def __init__(self, specific_class, url):
            self.specific_class = specific_class
            self.url = url

    class ContactSettingsStub:
        phone = "+7 000 000-00-00"
        email = "info@example.com"
        address = "Test address"

    def test_builds_contact_panel_without_title(self):
        from about_company.models import AboutPage

        nav_item = {
            "mega_menu_items": [
                {
                    "name": "Company",
                    "page": self.PageStub(AboutPage, "/company/"),
                    "external_url": "",
                }
            ]
        }

        menu = build_mega_menu(nav_item, self.ContactSettingsStub())

        self.assertEqual(menu["panels"][0]["type"], "contacts")
        self.assertTrue(menu["has_fixed_panel"])
        self.assertEqual(menu["fixed_panel_index"], 0)
        self.assertNotIn("title", menu["panels"][0])

    def test_unknown_page_keeps_left_item_without_panel(self):
        nav_item = {
            "mega_menu_items": [
                {
                    "name": "External",
                    "page": None,
                    "external_url": "https://example.com",
                }
            ]
        }

        menu = build_mega_menu(nav_item)

        self.assertEqual(menu["items"][0]["url"], "https://example.com")
        self.assertFalse(menu["has_panels"])

# Create your tests here.

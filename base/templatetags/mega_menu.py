from django import template

from about_company.models import AboutPage
from cases.models import CaseIndexPage, CaseIndustry
from practice.models import PracticeCategory, PracticeIndexPage
from products.models import ProductCategory, ProductIndexPage
from services.models import ServiceCategory, ServiceIndexPage
from services_1C.models import Service1CCategory, Service1CIndexPage


register = template.Library()


PANEL_CONFIGS = (
    (ServiceIndexPage, "categories", "Категории услуг", ServiceCategory, "category"),
    (Service1CIndexPage, "categories", "Категории сервисов 1С", Service1CCategory, "category"),
    (ProductIndexPage, "categories", "Категории решений", ProductCategory, "category"),
    (PracticeIndexPage, "categories", "Материалы практики", PracticeCategory, "category"),
    (CaseIndexPage, "categories", "Отрасли", CaseIndustry, "industry"),
)


def _value_get(value, key, default=None):
    if hasattr(value, "get"):
        return value.get(key, default)
    return getattr(value, key, default)


def _page_type(page):
    if not page:
        return None
    return getattr(page, "specific_class", None) or page.specific.__class__


def _page_url(page):
    return getattr(page, "url", "") or "#"


def _build_category_panel(page):
    page_type = _page_type(page)
    if not page_type:
        return None

    for index_class, panel_type, title, category_model, query_param in PANEL_CONFIGS:
        if issubclass(page_type, index_class):
            items = [
                {
                    "name": category.name,
                    "url": f"{_page_url(page)}?{query_param}={category.value}",
                }
                for category in category_model.objects.all()
            ]
            if not items:
                return None
            return {
                "type": panel_type,
                "title": title,
                "items": items,
            }

    return None


def _build_contact_panel(page, contact_settings):
    page_type = _page_type(page)
    if not page_type or not issubclass(page_type, AboutPage) or not contact_settings:
        return None

    return {
        "type": "contacts",
        "is_fixed": True,
        "phone": getattr(contact_settings, "phone", ""),
        "email": getattr(contact_settings, "email", ""),
        "address": getattr(contact_settings, "address", ""),
    }


def _build_panel(page, contact_settings):
    return _build_contact_panel(page, contact_settings) or _build_category_panel(page)


@register.simple_tag
def build_mega_menu(nav_item, contact_settings=None):
    items = []
    panels = []
    active_panel_index = None
    fixed_panel_index = None

    for index, subitem in enumerate(_value_get(nav_item, "mega_menu_items", []) or []):
        page = _value_get(subitem, "page")
        external_url = _value_get(subitem, "external_url", "")
        url = _page_url(page) if page else external_url
        panel = _build_panel(page, contact_settings)

        if panel:
            panel["index"] = index
            panels.append(panel)
            if panel.get("is_fixed"):
                fixed_panel_index = index
            if active_panel_index is None:
                active_panel_index = index

        items.append(
            {
                "index": index,
                "name": _value_get(subitem, "name", ""),
                "description": _value_get(subitem, "description", ""),
                "url": url,
                "has_link": bool(page or external_url),
                "has_panel": bool(panel),
                "is_active": active_panel_index == index,
            }
        )

    return {
        "items": items,
        "panels": panels,
        "active_panel_index": active_panel_index,
        "fixed_panel_index": fixed_panel_index,
        "has_panels": bool(panels),
        "has_fixed_panel": fixed_panel_index is not None,
    }

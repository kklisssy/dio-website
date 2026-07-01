from django.contrib import admin

from base.models import ConsultationRequest


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "phone", "email", "company")
    search_fields = ("name", "phone", "email", "company", "message")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "name", "company", "phone", "email", "message")

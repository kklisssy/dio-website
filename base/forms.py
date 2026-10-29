from django import forms
import re

from base.models import ConsultationRequest


class ConsultationRequestForm(forms.ModelForm):
    personal_data_agreement = forms.BooleanField(required=True)
    website = forms.CharField(required=False)

    class Meta:
        model = ConsultationRequest
        fields = [
            "name",
            "company",
            "email",
            "phone",
            "message",
        ]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 2 or not re.fullmatch(
            r"[A-Za-zА-Яа-яЁё -]+", name
        ) or not re.search(
            r"[A-Za-zА-Яа-яЁё]", name
        ):
            raise forms.ValidationError(
                "Введите имя буквами, минимум 2 символа."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not re.fullmatch(
            r"\+7 \([0-9]{3}\) [0-9]{3}-[0-9]{2}-[0-9]{2}", phone
        ):
            raise forms.ValidationError(
                "Введите телефон в формате +7 (999) 999-99-99."
            )

        return phone

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Spam detected.")
        return website


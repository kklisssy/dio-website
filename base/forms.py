from django import forms

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

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Spam detected.")
        return website


import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from base.forms import ConsultationRequestForm

logger = logging.getLogger(__name__)

@require_POST
def consultation_request(request):
    form = ConsultationRequestForm(request.POST)
    redirect_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    if "#contacts" not in redirect_url:
        redirect_url = f"{redirect_url}#contacts"

    if not form.is_valid():
        messages.error(request, "Проверьте заполнение полей и попробуйте ещё раз.")
        return redirect(redirect_url)

    consultation = form.save()
    try:
        send_consultation_email(consultation)
    except Exception:
        logger.exception("Failed to send consultation request email")


    messages.success(request, "Спасибо, заявка отправлена. Мы скоро свяжемся с Вами.")
    return redirect(redirect_url)

def send_consultation_email(consultation):
    recipients = getattr(settings, "CONSULTATION_REQUEST_RECIPIENTS", None)

    if not recipients:
        recipients = [settings.SERVER_EMAIL] if settings.SERVER_EMAIL else []

    if isinstance(recipients, str):
        recipients = [email.strip() for email in recipients.split(",") if email.strip()]

    if not recipients:
        logger.warning("Consultation request email recipients are not configured.")
        return

    subject = f"Новая заявка с сайта: {consultation.name}"

    message = "\n".join(
        [
           f"Имя: {consultation.name}",
           f"Компания: {consultation.company or 'Не указана'}",
           f"Телефон: {consultation.phone}",
           f"Email: {consultation.email}",
           "",
           "Описание задачи:",
           consultation.message,
        ]
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL or settings.SERVER_EMAIL,
        recipient_list=recipients,
        fail_silently=False,
    )

import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from base.forms import ConsultationRequestForm
from base.models import Subscriber

logger = logging.getLogger(__name__)


@require_POST
def consultation_request(request):
    form = ConsultationRequestForm(request.POST)
    redirect_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    if "#contacts" not in redirect_url:
        redirect_url = f"{redirect_url}#contacts"

    if not form.is_valid():
        messages.error(
            request,
            "Проверьте заполнение полей и попробуйте ещё раз.",
            extra_tags="contact",
        )
        return redirect(redirect_url)

    consultation = form.save()
    try:
        send_consultation_email(consultation)
    except Exception:
        logger.exception("Failed to send consultation request email")

    messages.success(
        request,
        "Спасибо, заявка отправлена. Мы скоро свяжемся с вами.",
        extra_tags="contact",
    )
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


@require_POST
def new_subscribe(request):
    redirect_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    email = request.POST.get("email", "").strip().lower()

    if not email:
        return redirect(redirect_url)

    subscriber, _ = Subscriber.objects.get_or_create(
        email=email,
        defaults={"is_active": False},
    )

    if subscriber.is_active:
        message_text = "Вы уже подтвердили подписку."
    else:
        confirm_url = request.build_absolute_uri(
            reverse("newsletter_confirm", args=[subscriber.confirm_token])
        )

        send_mail(
            subject="Подтвердите подписку на рассылку",
            message=(
                "Здравствуйте!\n\n"
                "Чтобы подтвердить подписку на рассылку, перейдите по ссылке:\n"
                f"{confirm_url}\n\n"
                "Если вы не подписывались, просто проигнорируйте это письмо."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber.email],
            fail_silently=False,
            html_message=f"""
                <div style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.5; color: #111;">
                    <p>Здравствуйте!</p>
                    <p>Чтобы подтвердить подписку на рассылку, нажмите на кнопку:</p>

                    <p style="margin: 28px 0;">
                        <a href="{confirm_url}"
                           style="
                               display: inline-block;
                               padding: 14px 24px;
                               background: #9f3030;
                               color: #ffffff;
                               text-decoration: none;
                               border-radius: 6px;
                               font-weight: bold;
                           ">
                            Подтвердить подписку
                        </a>
                    </p>

                    <p>Если вы не подписывались, просто проигнорируйте это письмо.</p>
                </div>
            """,
        )
        message_text = "На вашу почту отправлено письмо для подтверждения подписки."

    messages.success(
        request,
        message_text,
        extra_tags="newsletter",
    )
    return redirect(redirect_url)


def confirm_subscribe(request, token):
    subscriber = get_object_or_404(Subscriber, confirm_token=token)
    subscriber.is_active = True
    subscriber.confirmed_at = timezone.now()
    subscriber.save(update_fields=["is_active", "confirmed_at"])

    return redirect("/")


def confirm_unsubscribe(request, token):
    subscriber = get_object_or_404(Subscriber, confirm_token=token)
    subscriber.is_active = False
    subscriber.save(update_fields=["is_active"])

    return redirect("/")

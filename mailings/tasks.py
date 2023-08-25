from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from mailings.models import TopArticle
from users.models import User


@shared_task
def send_weekly_email():
    top_articles = TopArticle.objects.select_related('article').values_list(
        'article__title',
        'article__pk',
    )
    links_articles = []
    for title_article, id__article in top_articles:
        links_articles.append(
            {
                'title': title_article,
                'url': f'{settings.URL_ARTICLES}{id__article}',
            },
        )
    template_name = 'email_weekly.html'
    context = {
        'links_articles': links_articles,
    }
    html_message = render_to_string(template_name, context)
    recipient_list = list(
        User.objects.filter(
            subscribed=True,
        ).values_list(
            'email',
            flat=True,
        ),
    )
    subject = settings.WEEKLY_SUBJECT
    from_email = settings.EMAIL_HOST_USER

    email = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()

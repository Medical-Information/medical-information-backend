from __future__ import absolute_import, unicode_literals

import os

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from dotenv import load_dotenv

from mailings.models import TopArticles
from users.models import User

load_dotenv()


@shared_task
def send_weekly_email():
    top_articles = TopArticles.objects.values_list(
        'articles__title',
        'articles__pk',
    )
    links_articles = []
    url_articles = os.environ.get('URL_ARTICLES')
    for title_article, id__article in top_articles:
        links_articles.append(
            {
                'title': title_article,
                'url': f'{url_articles}{id__article}',
            },
        )
    template_name = 'email_weekly.html'
    context = {
        'links_articles': links_articles,
    }
    html_message = render_to_string(template_name, context)
    recipient_list = list(
        User.objects.filter(
            role='user',
        ).values_list(
            'email',
            flat=True,
        ),
    )
    subject = os.environ.get('WEEKLY_SUBJECT')
    from_email = os.environ.get('EMAIL_HOST_USER')

    email = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()

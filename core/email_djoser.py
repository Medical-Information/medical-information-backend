from django.contrib.auth.tokens import default_token_generator
from djoser import email, utils
from djoser.conf import settings


class ActivationEmail(email.ActivationEmail):
    template_name = 'email_djoser/activation.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = f'?uid={utils.encode_uid(user.pk)}&token={default_token_generator.make_token(user)}'
        context["token"] = ''
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'email_djoser/confirmation.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'email_djoser/password_reset.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = f'?uid={utils.encode_uid(user.pk)}&token={default_token_generator.make_token(user)}'
        context["token"] = ''
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context


class PasswordConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = 'email_djoser/password_changed_confirmation.html'

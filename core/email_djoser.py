from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'email_djoser/activation.html'


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'email_djoser/confirmation.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'email_djoser/password_reset.html'


class PasswordConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = 'email_djoser/password_changed_confirmation.html'

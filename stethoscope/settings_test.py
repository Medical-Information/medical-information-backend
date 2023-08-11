from stethoscope.settings import *  # noqa: F403

# Exclude django_opensearch_dsl from INSTALLED_APPS
INSTALLED_APPS = [
    app for app in INSTALLED_APPS if app != 'django_opensearch_dsl'  # noqa: F405
]

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-5#fl%0_q0^40#kzec%roeu+y!e)7+ac1%#tj3s+uj*3gjr^h7_",
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "django_ckeditor_5",
    # local
    "apps.accounts",
    "apps.core",
    "apps.articles",
    "apps.humanoids",
    "apps.development",
    "apps.events",
    "apps.equipment",
    "apps.blog",
    "apps.ulstu",
    "apps.cloud",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "teamatrix.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
           # 'loaders': [
            #    'django.template.loaders.filesystem.Loader',
             #   'django.template.loaders.app_directories.Loader',
            #],
        },
    },
]

WSGI_APPLICATION = "teamatrix.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "accounts.User"

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Append content hash to filenames — prevents browsers from serving
# stale cached JS/CSS after a deployment.
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/dashboard/"
LOGOUT_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CKEditor 5
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  # загрузка изображений только для персонала

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading", "|",
                "bold", "italic", "underline", "strikethrough", "|",
                "fontSize", "fontColor", "fontBackgroundColor", "|",
                "link", "bulletedList", "numberedList", "|",
                "blockQuote", "insertTable", "imageUpload", "mediaEmbed", "|",
                "sourceEditing", "removeFormat",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Обычный текст", "class": "ck-heading_paragraph"},
                {"model": "heading1", "view": "h1", "title": "Заголовок 1", "class": "ck-heading_heading1"},
                {"model": "heading2", "view": "h2", "title": "Заголовок 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Заголовок 3", "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Заголовок 4", "class": "ck-heading_heading4"},
            ]
        },
        "image": {
            "toolbar": [
                "imageTextAlternative", "|",
                "imageStyle:alignLeft", "imageStyle:alignCenter", "imageStyle:alignRight",
            ],
        },
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells", "tableProperties", "tableCellProperties"],
        },
        "fontSize": {
            "options": ["tiny", "small", "default", "big", "huge"],
        },
    }
}

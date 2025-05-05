from os import getenv

POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = getenv("POSTGRES_DB", "postgres")

MAIL_FROM = getenv("MAIL_FROM", "Book catalog")
MAIL_EMAIL = getenv("MAIL_EMAIL", "")
MAIL_HOST = getenv("MAIL_HOST", "")
MAIL_PASSWORD = getenv("MAIL_PASSWORD", "")
MAIL_PORT = int(getenv("MAIL_PORT", "25"))

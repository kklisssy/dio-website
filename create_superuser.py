import os
import sys

import django


def main():
    """Create a Django superuser from environment variables."""

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin").strip()
    email = (
        os.environ.get("DJANGO_SUPERUSER_EMAIL")
        or os.environ.get("ADMIN_EMAIL")
        or ""
    ).strip()
    password = (
        os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        or os.environ.get("ADMIN_PASSWORD")
        or ""
    )

    if not all([username, email, password]):
        print("\n" + "=" * 60, file=sys.stderr)
        print("ERROR: superuser environment variables are not set", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("Set these in .env:", file=sys.stderr)
        print("  - DJANGO_SUPERUSER_USERNAME, default: admin", file=sys.stderr)
        print("  - DJANGO_SUPERUSER_EMAIL, or legacy ADMIN_EMAIL", file=sys.stderr)
        print("  - DJANGO_SUPERUSER_PASSWORD, or legacy ADMIN_PASSWORD", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)

    if not password.strip():
        print("\n" + "=" * 60, file=sys.stderr)
        print("ERROR: password cannot be empty", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dio_website.settings.production")
    django.setup()

    from django.contrib.auth import get_user_model
    from django.core.exceptions import ValidationError

    User = get_user_model()

    try:
        if User.objects.filter(username=username).exists():
            print("\n" + "=" * 60)
            print(f"Superuser '{username}' already exists")
            print("=" * 60 + "\n")
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            print("\n" + "=" * 60)
            print(f"Superuser '{username}' created successfully")
            print("=" * 60 + "\n")

    except ValidationError as e:
        print("\n" + "=" * 60, file=sys.stderr)
        print(f"VALIDATION ERROR: {e}", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("\n" + "=" * 60, file=sys.stderr)
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

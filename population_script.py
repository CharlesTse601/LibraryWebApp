import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()


def populate():
    print("Population script placeholder — implement once models are defined.")
    print("Done.")


if __name__ == '__main__':
    populate()

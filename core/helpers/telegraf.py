from django.conf import settings
from telegraph import Telegraph


def text_to_telegraph(title, msg):
    telegraph = Telegraph(settings.TELEGRAPH_ACCESS_TOKEN)
    response = telegraph.create_page(
        title,
        html_content=msg
    )

    return 'https://telegra.ph/{}'.format(response['path'])

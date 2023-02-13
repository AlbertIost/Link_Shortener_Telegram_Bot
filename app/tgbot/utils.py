import qrcode
from django.conf import settings
from io import BytesIO
from ugc.models import Link
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask


def get_qrcode(link: str):
    img = qrcode.make(link)
    bio = BytesIO()
    bio.name = 'qrcode.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio



def get_short_url(link: Link):
    return settings.HOST + '/' + link.token

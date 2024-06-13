import dicttoxml
from django.utils.encoding import smart_str
from rest_framework.renderers import BaseRenderer


class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_str(data, encoding=self.charset)


class XMLRenderer(BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'

    def render(self, data, media_type=None, renderer_context=None):
        return dicttoxml.dicttoxml(data)

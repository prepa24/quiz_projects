from django.utils import translation

class ForceDefaultLanguageMiddleware:
    """
    Fòse tout request yo sèvi ak Kreyòl ('ht') kèlkeswa header Accept-Language,
    cookie lang, oubyen lang nan URL la.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.default_lang = 'ht'

    def __call__(self, request):
        # Si w ta vle kite /admin an an anglè, dekomante 3 liy sa yo:
        # if request.path.startswith('/admin/'):
        #     translation.activate('en')
        #     request.LANGUAGE_CODE = 'en'
        #     return self.get_response(request)

        translation.activate(self.default_lang)
        request.LANGUAGE_CODE = self.default_lang
        response = self.get_response(request)
        translation.deactivate()
        return response
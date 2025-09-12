from django.utils import translation

class ForceDefaultLanguageMiddleware:
    """
    Fòse tout request yo sèvi ak Kreyòl ('ht') kèlkeswa header Accept-Language,
    cookie lang, oubyen lang nan URL la.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si w ta vle kite /admin an an anglè, dekomante 3 liy sa yo:
        # if request.path.startswith('/admin/'):
        #     translation.activate('en')
        #     request.LANGUAGE_CODE = 'en'
        #     return self.get_response(request)

        if not request.path.startswith(('/en/', '/es/')):  
            # Fòse kreyòl si pa gen prefiks lang
            translation.activate('ht')
            request.LANGUAGE_CODE = 'ht'
        response = self.get_response(request)
        translation.deactivate()
        return response
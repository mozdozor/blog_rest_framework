from rest_framework.throttling import SimpleRateThrottle,AnonRateThrottle


class RegisterThrottle(SimpleRateThrottle):
    scope = 'registerthrottle'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


# AnonRateThrottle kulllanımı bu şekilde bu ise giriş yapmamış kullancıı aynı sayfaya 5 kere get yada post yaparsa ip adresi kısıtlanır

#
# class RegisterThrottle(AnonRateThrottle):
#     scope = 'registerthrottle'

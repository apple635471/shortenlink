from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2LoginView,
    OAuth2CallbackView,
)


class FacebookOAuth2AdapterFixed(FacebookOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)
        login.token = token
        return login


oauth2_login = OAuth2LoginView.adapter_view(FacebookOAuth2AdapterFixed)
oauth2_callback = OAuth2CallbackView.adapter_view(FacebookOAuth2AdapterFixed)

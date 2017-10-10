from django.http import HttpResponseRedirect
from django.views import View


class UserRedirect(View):
    @staticmethod
    def get(request):
        return HttpResponseRedirect('/user/{}/'.format(request.user.username))

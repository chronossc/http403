from django.http import HttpResponse
from http import Http403

def testview(request):
  return HttpResponse(u"""<a href="/403view/">Go to 403 view</a>""")

def Http403View(request):
  raise Http403(u"This is custom message for permission denied.")



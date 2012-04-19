from django.conf import settings
from django.core.exceptions import ViewDoesNotExist
from django.http import HttpResponse
from django.template import RequestContext,Template,loader,TemplateDoesNotExist
from django.utils.importlib import import_module
import httplib

class HttpException(Exception):
    """ Exception for Http Errors"""
	def __init__(self, message, status=500):
		self.status = status
		super(HttpException, self).__init__(message)

class HttpExceptionMiddleware(object):
	"""
	Replace Status code raises for a {{status}}.html rendered template
	"""
	def process_exception(self, request, exception):
		"""
		Render a {{status}}.html template or a hardcoded html as status page, but only if
		exception is instance of HttpException class
		"""
		# we need to import to use isinstance
		from http import HttpException
		if not isinstance(exception,HttpException):
			# Return None make that django reraise exception:
			# http://docs.djangoproject.com/en/dev/topics/http/middleware/#process_exception
			return None

		print exception.status
	
		try:
			# Handle import error but allow any type error from view
			callback = getattr(import_module(settings.ROOT_URLCONF),'handler' + str(exception.status))
			return callback(request,exception)
		except (ImportError,AttributeError),e:
			# doesn't exist a handler{{status}}, try get template
			try:
				t = loader.get_template(str(exception.status) + '.html')
			except TemplateDoesNotExist:
				# doesn't exist a template in path, use hardcoded template
				t = Template("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<HTML>
  <HEAD>
    <TITLE>
    {% if message %}
		{{message}}
	{% else %}
    Sorry {{w3cname}} error to {{ request.META.PATH }}.
    {% endif%}
    </TITLE>
  </HEAD>
  <BODY>
    <h2>{{w3cname}}</h2>
    <p>{% if message %}
		{{message}}
	{% else %}
    Sorry {{w3cname}} error to {{ request.META.PATH }}.
    {% endif%}</p>
  </BODY>
</HTML>""")

		# now use context and render template      
		c = RequestContext(request, {
		'message': exception.message,
		'w3cname': httplib.responses.get(exception.status, str(exception.status))
		})
      
		return HttpResponse(t.render(c), status=exception.status)
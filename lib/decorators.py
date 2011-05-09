# -*- coding: utf-8 -*-

"""
	:copyright: (c) 2011 by Tobias Heinzen 
	:license: BSD, see LICENSE for more details
"""

from flask import render_template, make_response, redirect, url_for, current_app
from functools import wraps
from lib.repository import RepositoryError

def templated(template):
	def decorator(f):
		@wraps(f)
		def template_function(*args, **kwargs):
			# error when no template is given
			if template is None:
				raise Exception("no template given")

			# get the context from the executed function
			context = None
			try:
				context = f(*args, **kwargs)
			except RepositoryError as error:
				return redirect(url_for('not_found'))
			except:
				raise

			if context is None:
				context = {}
			elif not isinstance(context, dict):
				return context

			# render the context using given template
			try:
				response = render_template(template, **context)
				return response
			except RepositoryError as error:
				return redirect(url_for('not_found'))
			except:
				raise

		return template_function
	return decorator

def cached(keyfn):
	def decorator(f):
		@wraps(f)
		def cache_function(*args, **kwargs):
			key = keyfn(*args, **kwargs)
			if key is None:
				result = f(*args, **kwargs)
			else:
				from lib.utils import cache
				result = cache.get(key)
				if result is None:
					result = f(*args, **kwargs)
					cache.set(key, result, timeout=current_app.config['CACHE_TIMEOUT'])
			return result

		return cache_function
	return decorator

def response_mimetype(mimetype):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			result = f(*args, **kwargs)
			response = make_response(result)
			response.mimetype = mimetype
			return response

		return wrapped
	return decorator

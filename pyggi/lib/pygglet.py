# -*- coding: utf-8 -*-

"""
    :copyright: (c) 2012 by Tobias Heinzen
    :license: BSD, see LICENSE for more details
"""

from flask import Blueprint

class PyggletStore(object):
    def __init__(self):
        self.pygglets = []

    def register(self, pygglet):
        assert isinstance(pygglet, Pygglet)
        self.pygglets.append(pygglet)

__pygglets__ = PyggletStore()

class Pygglet(object):
    def __init__(self, name, import_name):
        from pyggi.lib.decorators import templated, cached
        import functools

        self.blueprint = Blueprint(name, import_name, template_folder='templates')
        self.get = functools.partial(self.blueprint.route, methods=['GET'])
        self.post = functools.partial(self.blueprint.route, methods=['POST'])
        self.templated = templated
        self.cached = cached

        __pygglets__.register(self)

        self._main_menu = None

    def set_main_menu(self, template):
        self._main_menu = template

    def get_repository(self, name):
        from pyggi.lib.utils import get_repository_path
        from pyggi.lib.repository.gitr import GitRepository
        return GitRepository(repository=get_repository_path(name))

    def get_ref(self, repository, tree):
        from pyggi.lib.utils import get_repository_path
        from pyggi.lib.repository.gitr import GitRepository
        return GitRepository.resolve_ref(get_repository_path(repository), tree)

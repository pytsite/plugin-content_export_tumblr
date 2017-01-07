"""
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang
    from plugins import content_export
    from . import _driver

    lang.register_package(__name__, alias='content_export_tumblr')
    content_export.register_driver(_driver.Driver())


_init()

"""PytSite Tumblr Content Export Driver
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from frozendict import frozendict as _frozendict
from pytsite import logger as _logger, router as _router
from plugins import widget as _widget, content_export as _content_export, content as _content, tumblr as _tumblr


class Driver(_content_export.AbstractDriver):
    """Content Export Driver.
    """

    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'tumblr'

    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        return 'content_export_tumblr@tumblr'

    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get human readable driver options.
        """
        return driver_options.get('user_blog')

    def get_settings_widget(self, driver_opts: _frozendict, form_url: str) -> _widget.Abstract:
        """Add widgets to the settings form of the driver.
        """
        return _tumblr.widget.Auth(
            uid='driver_opts',
            oauth_token=driver_opts.get('oauth_token'),
            oauth_token_secret=driver_opts.get('oauth_token_secret'),
            screen_name=driver_opts.get('screen_name'),
            user_blog=driver_opts.get('user_blog'),
            callback_uri=form_url,
        )

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title))

        try:
            opts = exporter.driver_opts  # type: _frozendict
            oauth_token = opts.get('oauth_token')
            oauth_token_secret = opts.get('oauth_token_secret')

            s = _tumblr.session.Session(oauth_token, oauth_token_secret)

            tags = exporter.add_tags  # type: tuple

            if entity.has_field('tags'):
                tags += tuple(t.title for t in entity.f_get('tags'))

            thumb_url = entity.images[0].get_url(width=640) if entity.images else None
            author = entity.author.full_name
            description = entity.f_get('description') if entity.has_field('description') else ''
            s.blog_post_link(opts['user_blog'], entity.url, entity.title, description, thumb_url,
                             author=author, tags=','.join(tags))
        except Exception as e:
            raise _content_export.error.ExportError(e)

        _logger.info("Export finished. '{}'".format(entity.title))

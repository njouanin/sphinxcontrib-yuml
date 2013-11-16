# -*- coding: utf-8 -*-
"""
    sphinxcontrib.yuml
    ~~~~~~~~~~~~~~~~~~~~~~

    Embed yuml diagrams on your documentation.

    :copyright: Copyright 2013 by Nicolas Jouanin <nicolas.jouanin@gmail.com>.
    :license: GPLv3
"""

import posixpath
import urllib2, urllib
from os import path
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.errors import SphinxError
from sphinx.util import ensuredir, relative_uri
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

DEFAULT_FORMATS = dict(html='png', latex='pdf', text=None)
DEFAULT_OPTIONS = dict(style='scruffy', direction='LR', type='class')

def get_hashid(text, options):
    hashkey = text.encode('utf-8') + str(options)
    hashid = sha(hashkey).hexdigest()
    return hashid

def get_filename(text, options, term):
    hashid = get_hashid(text, options)
    fname = 'diagram-%s.%s' % (hashid, term)
    return fname

class YumlError(SphinxError):
    category = 'Yuml error'

class YumlDirective(directives.images.Image):
    """Directive to insert Yuml markup

    Example::

        .. yuml:: 
           :alt: [Customer]->[Billing Address]
           :type: class, activity or usecase
           :scale: positive integer value
           :direction: LR, TD or RL
           :style: boring, plain, scruffy

           [Customer]->[Billing Address]
    """
    type_values = ('class', 'activity', 'usecase')
    direction_values = ('LR', 'RL', 'TD')
    style_values=('boring', 'plain', 'scruffy')

    def type_choice(argument):
        return directives.choice(argument, YumlDirective.type_values)

    def scale_choice(argument):
        return directives.choice(argument, YumlDirective.scale_values)

    def direction_choice(argument):
        return directives.unchanged

    def style_choice(argument):
        return directives.choice(argument, YumlDirective.style_values)
            
    # this enables content in the directive
    has_content = True
    required_arguments=0
    own_option_spec = {'type': type_choice,
                    'scale': directives.positive_int,
                    'direction': direction_choice,
                    'style':style_choice}
    option_spec = directives.images.Image.option_spec.copy()
    option_spec.update(own_option_spec)

    def run(self):
        yuml_options = dict([(k,v) for k,v in self.options.items() if k in self.own_option_spec])
        self.arguments = ['']

        (image_node,) = directives.images.Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node]
        text = '\n'.join(self.content)
        image_node.yuml = dict(text=text,options=yuml_options)
        return [image_node]
        
def render_yuml_images(app, doctree):
    app.builder.info('Rendering Yuml')
    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'yuml'):
            continue

        uri = img['uri']
        text = img.yuml['text']
        options = img.yuml['options']
        try:
            img['uri'] = render_yuml(app, uri, text, options)
            img['candidates']={'?':''}
        except YumlError, exc:
            app.builder.warn('yuml error: ' + str(exc))
            img.replace_self(nodes.literal_block(text, text))
            continue

def render_yuml(app, uri, text, options):
    """
    Render yuml into a image file.
    """
    format_map = DEFAULT_FORMATS.copy()
    format_map.update(app.builder.config.yuml_format)

    option_map = DEFAULT_OPTIONS.copy()
    option_map.update(options)

    term = format_map[app.builder.format]
    fname = get_filename(text, options, term)
    
    if app.builder.format == 'html':
        # HTML
        imgpath = relative_uri(app.builder.env.docname,'_images')
        relfn = posixpath.join(imgpath, fname)
        outfn = path.join(app.builder.outdir, '_images', fname)
    else:
        # Non-HTML
        if app.builder.format != 'latex':
            app.builder.warn('yuml: the builder format %s is not supported.' % app.builder.format)
        relfn = fname
        outfn = path.join(app.builder.outdir, fname)

    ensuredir(path.dirname(outfn))
    docdir = (path.dirname(app.builder.env.docname))

    try:
        app.debug('[Yuml] generating diagram in %s' % fname)
        opts = option_map['style']
        if 'scale' in option_map:
            opts += ';scale:%s' % option_map['scale']
        opts += ';dir:%s' % option_map['direction']
        try:
            data = urllib.parse.quote(text, encoding='utf-8')
        except Exception:
            data = urllib.quote(text.encode('utf-8'))
        url = '%s/%s/%s/%s.%s' % (app.builder.config.yuml_server_url.strip('/'), opts, option_map['type'], data, term)
        app.debug('[Yuml]   with URL %s' % url)
        headers = {
            'User-Agent' : 'sphinxcontrib/yuml v0.1',
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = urllib2.Request(url, None, headers)
        rep = urllib2.urlopen(req).read()
        out = open(outfn, 'wb')
        out.write(rep)
        out.close()
    except Exception as e:
        raise YumlError(str(e))

    return relfn

def setup(app):
    app.add_config_value('yuml_server_url', 'http://yuml.me/diagram/', 'html')
    app.add_config_value('yuml_format', DEFAULT_FORMATS, 'html')
    app.add_config_value('yuml_options', DEFAULT_OPTIONS, '')
    app.connect('doctree-read', render_yuml_images)
    app.add_directive('yuml', YumlDirective)
    
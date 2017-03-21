import peewee
import jinja2
import poobrains
import markdown


def magic_markdown_loader(storable, handle):

    storables = poobrains.storage.Storable.children_keyed()
    for k, v in storables.iteritems():
        storables[k.lower()] = v # Allows us to use the correct case, or just lowercase

    cls = storables[storable]
    return cls.load(handle)


class MagicDict(dict):

    """ Magical dict to (try to) generate links on demand """

    loader = None

    def __init__(self, *args, **kwargs):

        super(MagicDict, self).__init__(*args, **kwargs)
        self.set_loader(magic_markdown_loader)


    def __contains__(self, key):
        
        if not super(MagicDict, self).__contains__(key):

            if self._valid_magickey(key):
                
                storable, handle = key.split('/')
                try:
                    return bool(self.loader(storable, handle))
                except:
                    return False

            return False

        return True
    
    
    def __getitem__(self, key):

        if not super(MagicDict, self).__contains__(key):

            if self._valid_magickey(key):

                storable, handle = key.split('/')
                try:
                    instance = self.loader(storable, handle)

                    try:
                        url = instance.url('full')
                    except:

                        try:
                            url = instance.url('raw')
                        except:

                            try:
                                url = instance.url('teaser')
                            except:
                                url = "#NOLINK" # FIXME: What's the more elegant version of this, again?

                    if hasattr(instance, 'reference_title'):
                        title = instance.reference_title
                    elif hasattr(instance, 'title'):
                        title = instance.title
                    elif hasattr(instance, 'filename'):
                        title = instance.filename
                    elif hasattr(instance, 'description'):
                        title = instance.description
                    else:
                        title = None

                    return (url, title)

                except:
                    raise KeyError("Couldn't load '%s.%s'." % storable, handle)


        return super(MagicDict, self).__getitem__(key)


    def _valid_magickey(self, key):

        return '/' in key and len(key.split('/')) == 2


    def set_loader(self, loader):
        self.loader = loader



class pooMarkdown(markdown.Markdown):

    def __init__(self, *args, **kwargs):
        
        super(pooMarkdown, self).__init__(*args, **kwargs)
        self.references = MagicDict()


try:

    import config
    if hasattr(config, 'MARKDOWN_CLASS') and issubclass(config.MARKDOWN_CLASS, markdown.Markdown):
        cls = config.MARKDOWN_CLASS
    else:
        cls = pooMarkdown

except ImportError:
    cls = pooMarkdown

md = cls(output_format="html5") # means we can globally register markdown extensions with "poobrains_markdown.md.registerExtensions


class MarkdownString(str):

    def render(self):
        return jinja2.Markup(md.convert(self))


class MarkdownFieldDescriptor(peewee.FieldDescriptor):

    def __set__(self, instance, value):

        if not isinstance(value, MarkdownString):
            value = MarkdownString(value)
        instance._data[self.att_name] = value
        instance._dirty.add(self.att_name)


class MarkdownField(poobrains.storage.fields.TextField):

    def add_to_class(self, model_class, name):

        super(MarkdownField, self).add_to_class(model_class, name)
        setattr(model_class, name, MarkdownFieldDescriptor(self))

import peewee
import jinja2
import poobrains
import markdown

try:

    import config
    if hasattr(config, 'MARKDOWN_CLASS') and issubclass(config.MARKDOWN_CLASS, markdown.Markdown):
        cls = config.MARKDOWN_CLASS
    else:
        cls = markdown.Markdown

except ImportError:
    cls = markdown.Markdown


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

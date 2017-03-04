import peewee
import jinja2
import poobrains
import markdown


class MarkdownString(str):

    def render(self):
        return jinja2.Markup(markdown.markdown(self))


class MarkdownFieldDescriptor(peewee.FieldDescriptor):

#    def __get__(self, instance, instance_type=None):
#        if instance is not None:
#            data = instance._data.get(self.att_name)
#            if not isinstance(data, MarkdownString):
#                data = MarkdownString(data)
#
#            return data
#
#        return self.field

    def __set__(self, instance, value):

        if not isinstance(value, MarkdownString):
            value = MarkdownString(value)
        instance._data[self.att_name] = value
        instance._dirty.add(self.att_name)


class MarkdownField(poobrains.storage.fields.TextField):

    def add_to_class(self, model_class, name):

        super(MarkdownField, self).add_to_class(model_class, name)
        setattr(model_class, name, MarkdownFieldDescriptor(self))

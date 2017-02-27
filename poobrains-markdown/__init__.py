import poobrains
import markdown

class MarkdownField(poobrains.storage.TextField):

    def __str__(self):
        return markdown.markdown(self)

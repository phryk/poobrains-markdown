#! /usr/bin/env python
# -*- coding: utf-8 -*-

import poobrains
import poobrains_markdown

app = poobrains.app


@poobrains.app.expose('/article', mode='full')
class Article(poobrains.auth.Administerable):

    title = poobrains.storage.fields.CharField(null=False)
    text = poobrains_markdown.MarkdownField()

    @property
    def reference_title(self):

        """
        prepends Florb before the title for magic markdown references ("[text][storable/handle]")
        """

        return "Florb %s" % self.title

if __name__ == '__main__':
    app.run()

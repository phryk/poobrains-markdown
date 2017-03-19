#! /usr/bin/env python
# -*- coding: utf-8 -*-

import poobrains
import poobrains_markdown

app = poobrains.app


@poobrains.app.expose('/article', mode='full')
class Article(poobrains.auth.Administerable):

    title = poobrains.storage.fields.CharField(null=False)
    text = poobrains_markdown.MarkdownField()


if __name__ == '__main__':
    app.run()

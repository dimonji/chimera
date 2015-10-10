"""
Набор документов для формирования поста.
"""

from system.document import BaseDocument
from motorengine import EmbeddedDocumentField, StringField, ListField, DateTimeField


class PostTagsDocument(BaseDocument):
    """
    Теги для постов. Одиночные документы которые используется в рамках списка тегов для поиска и описания тем для поста.

    :type title: str Заголовок тега;
    :type alias: str Псевдоним тега;
    """
    title = StringField()
    alias = StringField()


class PostMetaDocument(BaseDocument):
    """
    Набор служебной информации о посте о датах создания/изменения поста, информация об авторе и т.д.

    :type dateCreate: str Дата создания;
    :type dateUpdate: str Дата создания;
    :type author: str Автор поста;
    """

    dateCreate = DateTimeField(auto_now_on_insert=True)
    dateUpdate = DateTimeField(auto_now_on_update=True)
    author = StringField()


class PostDocument(BaseDocument):
    """
    Пост - текстовая запись. Относиться к каталогу, имеет сервисную информацию о себе, позволяет теггирование.

    :type alias: str Псевдоним поста для использования его в url для последующей идентификации;
    :type aliasCatalog: str Псеводним каталога к которому относится пост и который будет показываться в рамках этой категории;
    :type title: str Человеческий заголовок для поста;
    :type tags: list Список названий тегов для последующего теггирования и выбора постов по одинаковым тегам;
    :type meta: PostMetaDocument Сервсисная информация о посте - дате создания, авторе, и т.д.;
    :type text: str Текст поста;
    """

    __collection__ = "post"

    alias = StringField()
    aliasCatalog = StringField()
    title = StringField()
    tags = ListField(EmbeddedDocumentField(StringField))
    meta = EmbeddedDocumentField(PostMetaDocument)
    text = StringField()

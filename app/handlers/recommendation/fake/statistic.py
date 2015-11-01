import random
import system.utils.exceptions
from tornado.gen import coroutine
from system.handler import BaseHandler
from documents.recommendation.fake import FakeUserDocument


class FakeStatisticHandler(BaseHandler):

    @coroutine
    def get(self):
        """Запрос данных по пользователям (случайные 10)."""
        collection_critic = yield FakeUserDocument().objects.find_all()

        # Перемешивание втупую и срез 10 пользователей
        random.shuffle(collection_critic)
        fake_user_list = {}
        for document_critic in collection_critic[:10]:
            fake_user_list[str(document_critic._id)] = document_critic.info.name

        raise system.utils.exceptions.Result(content={"fakeUserList": fake_user_list})

    @coroutine
    def post(self):
        """Расчет статистики.

        В качестве параметров передавать список необходимых данных: двоих пользователей или фильм.
        Возвращать данные рассчитанные данные.

        """
        from system.components.recommendations.statistic import Recommendations
        # 5501eec480a9e10c639d60e0 5501eec480a9e10c639d60e4
        user1 = self.get_argument("user1", "")
        user2 = self.get_argument("user2", "")
        movie = self.get_argument("movie", "")

        # todo
        user1 = "5501eec480a9e10c639d60e0"
        user2 = "5501eec480a9e10c639d60e4"
        movie = "tt0407887"
        # todo
        collection_critic = yield FakeUserDocument().objects.limit(100).find_all()

        # Формирование массива данных для анализа
        list_critic = {}
        for document_critic in collection_critic:
            # Массив данных имеет вид [ид пользователя => [ид объекта => оценка,] ]
            list_critic[str(document_critic._id)] = document_critic.critic
        # print(list_critic)

        # Recommendations
        instance_recommendations = Recommendations(list_critic)

        result = {}
        if movie != "":
            # Для проверки объектов
            result = {
                # Фильмы похожие на
                "matches": instance_recommendations.top_matches(movie, 3, instance_recommendations.TYPE_TRANSFORMS,
                                                                instance_recommendations.pearson),
                # Кто еще не смотрел фильм
                "recommendations": instance_recommendations.get_recommendations_transforms(movie),
                # Похожие фильмы
                #"similarItems": instance_recommendations.similar_items,
                # Выработка рекомендации по образцам
                "pearson": instance_recommendations.get_recommendations_items(user1),
            }
        elif (user1 != "") and (user2 != ""):
            # Для сравнения пользователей
            result = {
                # Евклидово расстояние
                "euclid": instance_recommendations.euclid(instance_recommendations.source[user1],
                                                          instance_recommendations.source[user2]),
                # Корреляця Пирсона
                "pearson": instance_recommendations.pearson(instance_recommendations.source[user1],
                                                            instance_recommendations.source[user2]),
                # Коэффициент Жаккара
                "jaccard": instance_recommendations.jaccard(instance_recommendations.source[user1],
                                                            instance_recommendations.source[user2]),
                # Манхэттенское расстояние
                "manhattan": instance_recommendations.manhattan(instance_recommendations.source[user1],
                                                                instance_recommendations.source[user2]),
                # Ранжирование критиков
                "matches": instance_recommendations.top_matches(user1, 2, instance_recommendations.TYPE_SOURCE,
                                                                instance_recommendations.pearson),
                # Выработка рекомендации
                "recommendations": instance_recommendations.get_recommendations(user1),
            }

        raise system.utils.exceptions.Result(content=result)

        # print(
        #     'Люди:', user1, 'и', user2, '\n',
        #     'Евклидово расстояние		', instance_recommendations.euclid(instance_recommendations.source, user1, user2), '\n',
        #     'Корреляця Пирсона			', instance_recommendations.pearson(instance_recommendations.source, user1, user2), '\n',
        #     'Коэффициент Жаккара		', instance_recommendations.jaccard(instance_recommendations.source, user1, user2), '\n',
        #     'Манхэттенское расстояние	', instance_recommendations.manhattan(instance_recommendations.source, user1, user2), '\n',
        #     '\n',
        #     'Ранжирование критиков		', instance_recommendations.top_matches(user1, 2, instance_recommendations.TYPE_SOURCE, instance_recommendations.pearson), '\n',
        #     'Выработка рекомендации		', instance_recommendations.get_recommendations(user1), '\n',
        #     '\n',
        #     'Фильмы похожие на 			', movie, instance_recommendations.top_matches(movie, 3, instance_recommendations.TYPE_TRANSFORMS, instance_recommendations.pearson), '\n',
        #     'Кто еще не смотрел фильм	', movie, instance_recommendations.get_recommendations_transforms(movie), '\n',
        #     # 'AAAAAAAAAA	', instance_recommendations.transforms, '\n',
        #     # '\n',
        #     # 'Похожие фильмы	\n			', instance_recommendations.similar_items, '\n',
        #     # 'Выработка рекомендации по образцам', instance_recommendations.get_recommendations_items(user1), '\n',
        # )
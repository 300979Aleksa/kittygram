import datetime as dt
# print(dt.datetime.now())

import webcolors

from rest_framework import serializers

from .models import Cat, Owner, Achievement, AchievementCat, CHOICES


class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data


class OwnerSerializer(serializers.ModelSerializer):
    # cats = serializers.StringRelatedField(many=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')

class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        # fields = ('id', 'name') - при смене наименования, меняем данные в мета классе
        fields = ('id', 'achievement_name')

class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)
    
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class CatSerializer(serializers.ModelSerializer):
    # achievements = AchievementSerializer(read_only=True, many=True) - read_only=True убираем для ввода и изменения показателей котов 
    achievements = AchievementSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    # color = Hex2NameColor()
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        # fields = ('id', 'name', 'color', 'birth_year')
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 
                  'achievements', 'age')
        # fields = '__all__'

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year
    
    def create(self, validated_data):
        # Если в исходном запросе не было поля achievements
        # print(self.initial_data)
        if 'achievements' not in self.initial_data:
            # То создаём запись о котике без его достижений
            cat = Cat.objects.create(**validated_data)
            return cat
        # print(validated_data)
        # Уберем список достижений из словаря validated_data и сохраним его
        achievements = validated_data.pop('achievements')

        # Создадим нового котика пока без достижений, данных нам достаточно
        # print(validated_data)
        # print(**validated_data)
        cat = Cat.objects.create(**validated_data)

        # Для каждого достижения из списка достижений
        for achievement in achievements:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat)
        return cat
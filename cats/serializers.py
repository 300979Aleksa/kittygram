from rest_framework import serializers

from .models import Cat, Owner, Achievement, AchievementCat


  
class OwnerSerializer(serializers.ModelSerializer):
    # cats = serializers.StringRelatedField(many=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')

class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    # achievements = AchievementSerializer(read_only=True, many=True) - read_only=True убираем для ввода и изменения показателей котов 
    achievements = AchievementSerializer(many=True, required=False)

    class Meta:
        model = Cat
        # fields = ('id', 'name', 'color', 'birth_year')
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements')
        # fields = '__all__'

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
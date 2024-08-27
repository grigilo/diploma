from user.serializers import UserSerializer

from rest_framework import serializers

from feed.models import Ad, Comment


class AdCreateSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации создания объявления
    """

    class Meta:
        model = Ad
        fields = ["title", "price", "description"]


class AdUpdateSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации обновления объявления
    """

    title = serializers.CharField(max_length=128, required=False)
    price = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Ad
        fields = ["title", "price", "description"]

    # def validate(self, data):
    #     user = self.context['request'].user
    #     ad_id = self.instance.id if self.instance else None
    #     if Ad.objects.filter(id=ad_id, author=user).exists():
    #         return data
    #     raise serializers.ValidationError("Вы не являетесь владельцем этого объявления")


class AdSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации отображения объявления
    """

    class Meta:
        model = Ad
        fields = ["title", "price", "description", "author", "id"]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации создания и обновления комментария
    """

    class Meta:
        model = Comment
        fields = ["text"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации отображения объявления
    """

    author = UserSerializer()
    ad = AdSerializer()

    class Meta:
        model = Comment
        fields = ["text", "id", "author", "ad"]

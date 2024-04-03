from rest_framework import serializers

class ImageUrlSerializer(serializers.Serializer):
    image_url = serializers.CharField(max_length=200)

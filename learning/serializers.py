from rest_framework import serializers
from .models import Character, Radical, CharacterSet


class RadicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radical
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    radical_1 = RadicalSerializer(read_only=True)
    radical_2 = RadicalSerializer(read_only=True)
    radical_3 = RadicalSerializer(read_only=True)
    msg = serializers.SerializerMethodField()
    radical_1_id = serializers.SerializerMethodField()
    radical_2_id = serializers.SerializerMethodField()
    radical_3_id = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = '__all__'

    # these methods are depreciated
    def get_radical_1_id(self, obj):
        return obj.radical_1.pk

    def get_radical_2_id(self, obj):
        return obj.radical_2.pk if obj.radical_2 else 0

    def get_radical_3_id(self, obj):
        return obj.radical_3.pk if obj.radical_3 else 0

    def get_msg(self, obj):
        return "WARNING: 'radical_1_id', 'radical_2_id', 'radical_3_id' " \
               "are depreciated and will be removed in future version, " \
               "use 'radical_1', 'radical_2', and 'radical_3' instead"


class CharacterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSet
        fields = '__all__'

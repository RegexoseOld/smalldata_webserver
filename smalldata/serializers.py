from rest_framework import serializers
from .models import Utterance, Category, TrainingUtterance, SongState, Topic, Show
import enchant

d = enchant.Dict("de_DE")


def is_german_text(sentence):
    accept_ratio = 0.5  # accept_ratio percent of the words need to known by the used enchant library
    """
    return True if any word in the sentence is known to german.model
    """
    words = sentence.split(" ")
    n_german = 0.
    for word in words:
        if d.check(word) or d.check(word.capitalize()) or d.check(word.lower()):
            n_german += 1

    if n_german / len(words) < accept_ratio:
        raise serializers.ValidationError("Utterance has no german words")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'german_name')


class UtteranceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    msg_id = serializers.CharField(read_only=True)
    text = serializers.CharField(validators=[is_german_text])

    class Meta:
        model = Utterance
        fields = '__all__'

    #  Overwrite `to_internal_value` and `create` to make sure `msg_id` is contained in `validated_data` but not passed
    #  to Model.create()
    def to_internal_value(self, data):
        internal_value = super(UtteranceSerializer, self).to_internal_value(data)
        msg_id_value = data.get("msg_id")
        my_non_model_field_value = msg_id_value
        internal_value.update({
            "msg_id": my_non_model_field_value
        })
        return internal_value

    def create(self, validated_data):
        validated_data.pop('msg_id', None)
        return super().create(validated_data)


class SongStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongState
        fields = '__all__'


class TrainingUtteranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingUtterance
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

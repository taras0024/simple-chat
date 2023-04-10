from rest_framework import serializers

from db.chats.models import Thread, Message
from db.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ReadMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ('id', 'text', 'sender', 'is_read')


class WriteMessageSerializer(serializers.ModelSerializer):
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())
    text = serializers.CharField(required=True)

    class Meta:
        model = Message
        fields = ('text', 'thread')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context['user']
        thread = attrs['thread']
        if user not in thread.participants.all():
            raise serializers.ValidationError('User is not a participant of this thread')
        return attrs

    def create(self, validated_data):
        message = Message.objects.create(
            thread=validated_data['thread'],
            sender=self.context['user'],
            text=validated_data['text']
        )
        return message


class ReadThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = ReadMessageSerializer(many=True)

    class Meta:
        model = Thread
        fields = ('id', 'participants', 'messages')


class WriteThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ()

    def create(self, validated_data):
        user = self.context['user']
        thread = Thread.objects.filter(creator=user).first()
        if thread:
            return thread

        thread = Thread.objects.create(creator=user)
        thread.participants.add(user)
        return thread

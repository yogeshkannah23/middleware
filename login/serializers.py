from rest_framework import serializers
from login.models import User,Post

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email', 'password']
        extra_kwargs = {
            'password': {
                'write_only':True,
            }
        }

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'discription', 'created_on']
        read_only_fields = ['author','created_on']
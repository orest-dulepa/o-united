from rest_framework.serializers import ModelSerializer, RelatedField
from work.models import TaskCategoryList


class TaskCategorySerializer(ModelSerializer):
    class Meta:
        model = TaskCategoryList
        fields = '__all__'

    def to_representation(self, instance):
        instance = super(TaskCategorySerializer, self).to_representation(instance)
        if instance["parent"] is None:
            children = TaskCategoryList.objects.filter(parent_id=instance["id"], active=True).all()
            instance["children"] = TaskCategorySerializer(children, many=True).data
        del instance["parent"]
        return instance

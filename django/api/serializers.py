from django.contrib.auth.models import User, Group
from django.db.models.fields import SlugField
from rest_framework import serializers
from gregory.models import Articles, Trials

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
	source = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

	class Meta:
		model = Articles
		fields = ['article_id','title','summary','link','published_date','source','relevant','ml_prediction_gnb','ml_prediction_lr','discovery_date','noun_phrases','doi']

class TrialSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Trials
		fields = ['trial_id','title','summary','published_date','link']



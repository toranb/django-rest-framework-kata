import json
from django.test import TestCase
from codecamp.ember.models import Speaker, Tag, Rating


class RatingTests(TestCase):

    def setUp(self):
        self.first_rating = Rating(score=9, feedback='legit')
        self.last_rating = Rating(score=2, feedback='broken')
        self.first_rating.save()
        self.last_rating.save()

    def test_will_return_json_with_list_of_ratings(self):
        response = self.client.get('/codecamp/ratings/')
        ratings = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(ratings), 2)

    def test_ratings_json_has_an_attribute_for_each_item(self):
        response = self.client.get('/codecamp/ratings/')
        ratings = json.loads(response.content)
        self.assertEqual(ratings[0]['score'], 9)
        self.assertEqual(ratings[0]['feedback'], 'legit')
        self.assertEqual(ratings[1]['score'], 2)
        self.assertEqual(ratings[1]['feedback'], 'broken')

    def test_detail_ratings_endpoint_returns_attributes_for_given_rating_id(self):
        response = self.client.get('/codecamp/ratings/{}/'.format(self.last_rating.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"id": 2, "score": 2, "feedback": "broken"}')

    def test_http_post_will_create_rating_and_return_201(self):
        data = {'score': 9, 'feedback': 'nice try'}
        response = self.client.post('/codecamp/ratings/', data)
        self.assertEqual(response.status_code, 201)

    def test_http_post_will_create_rating_and_return_created_rating_json(self):
        data = {'score': 9, 'feedback': 'nice try'}
        response = self.client.post('/codecamp/ratings/', data)
        created_rating = json.loads(response.content)
        self.assertEqual(created_rating['score'], 9)
        self.assertEqual(created_rating['feedback'], 'nice try')

    def test_http_post_without_data_returns_400(self):
        response = self.client.post('/codecamp/ratings/', {})
        self.assertEqual(response.status_code, 400)

    def test_http_put_will_update_first_rating_and_return_200(self):
        data = {'score': 124, 'feedback': 'updated feedback'}
        response = self.client.put('/codecamp/ratings/{}/'.format(self.first_rating.pk), data)
        self.assertEqual(response.status_code, 200)

    def test_http_put_will_update_first_rating_and_return_updated_rating_json(self):
        data = {'score': 124, 'feedback': 'updated feedback'}
        response = self.client.put('/codecamp/ratings/{}/'.format(self.first_rating.pk), data)
        updated_rating = json.loads(response.content)
        self.assertEqual(updated_rating['score'], 124)
        self.assertEqual(updated_rating['feedback'], 'updated feedback')

    def test_http_delete_will_remove_first_rating_and_return_204(self):
        response = self.client.delete('/codecamp/ratings/{}/'.format(self.first_rating.pk))
        self.assertEqual(response.status_code, 204)

    def test_http_delete_will_remove_first_rating_and_return_empty_content(self):
        response = self.client.delete('/codecamp/ratings/{}/'.format(self.first_rating.pk))
        self.assertEqual(response.content, '')

    def test_http_delete_will_return_404_when_incorrect_id_used_to_delete_rating(self):
        response = self.client.delete('/codecamp/ratings/999999999999999999/')
        self.assertEqual(response.status_code, 404)


class TagTests(TestCase):

    def setUp(self):
        self.first_tag = Tag(description='javascript')
        self.last_tag = Tag(description='python')
        self.first_tag.save()
        self.last_tag.save()

    def test_will_return_json_with_list_of_tags(self):
        response = self.client.get('/codecamp/tags/')
        tags = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(tags), 2)

    def test_tags_json_returns_first_tag_json(self):
        response = self.client.get('/codecamp/tags/')
        speakers = json.loads(response.content)
        self.assertEqual(speakers[0]['description'], 'javascript')

    def test_tags_json_returns_last_tag_json(self):
        response = self.client.get('/codecamp/tags/')
        speakers = json.loads(response.content)
        self.assertEqual(speakers[0]['description'], 'javascript')

    def test_detail_tags_endpoint_returns_attributes_for_given_tag_id(self):
        response = self.client.get('/codecamp/tags/{}/'.format(self.first_tag.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"id": 1, "description": "javascript"}')

    def test_http_post_will_create_tag_and_return_201(self):
        data = {'description': 'new'}
        response = self.client.post('/codecamp/tags/', data)
        self.assertEqual(response.status_code, 201)

    def test_http_post_will_create_tag_and_return_created_tag_json(self):
        data = {'description': 'new'}
        response = self.client.post('/codecamp/tags/', data)
        created_tag = json.loads(response.content)
        self.assertEqual(created_tag['description'], 'new')

    def test_http_post_without_data_returns_400(self):
        response = self.client.post('/codecamp/tags/', {})
        self.assertEqual(response.status_code, 400)

    def test_http_put_will_update_first_tag_and_return_200(self):
        data = {'description': 'updated'}
        response = self.client.put('/codecamp/tags/{}/'.format(self.first_tag.pk), data)
        self.assertEqual(response.status_code, 200)

    def test_http_put_will_update_first_tag_and_return_updated_tag_json(self):
        data = {'description': 'updated'}
        response = self.client.put('/codecamp/tags/{}/'.format(self.first_tag.pk), data)
        updated_speaker = json.loads(response.content)
        self.assertEqual(updated_speaker['description'], 'updated')

    def test_http_delete_will_remove_first_tag_and_return_204(self):
        response = self.client.delete('/codecamp/tags/{}/'.format(self.first_tag.pk))
        self.assertEqual(response.status_code, 204)

    def test_http_delete_will_remove_first_tag_and_return_empty_content(self):
        response = self.client.delete('/codecamp/tags/{}/'.format(self.first_tag.pk))
        self.assertEqual(response.content, '')

    def test_http_delete_will_return_404_when_incorrect_id_used_to_delete_tag(self):
        response = self.client.delete('/codecamp/tags/999999999999999999/')
        self.assertEqual(response.status_code, 404)


class SpeakerTests(TestCase):

    def setUp(self):
        self.first_speaker = Speaker(name='foo')
        self.last_speaker = Speaker(name='bar')
        self.first_speaker.save()
        self.last_speaker.save()

    def test_will_return_json_with_list_of_speakers(self):
        response = self.client.get('/codecamp/speakers/')
        speakers = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(speakers), 2)

    def test_speakers_json_has_an_attribute_for_each_item(self):
        response = self.client.get('/codecamp/speakers/')
        speakers = json.loads(response.content)
        self.assertEqual(speakers[0]['name'], 'foo')

    def test_speakers_json_returns_last_speaker_json(self):
        response = self.client.get('/codecamp/speakers/')
        speakers = json.loads(response.content)
        self.assertEqual(speakers[0]['name'], 'foo')

    def test_detail_speakers_endpoint_returns_attributes_for_given_speaker_id(self):
        response = self.client.get('/codecamp/speakers/{}/'.format(self.first_speaker.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"id": 1, "name": "foo"}')

    def test_http_post_will_create_speaker_and_return_201(self):
        data = {'name': 'who'}
        response = self.client.post('/codecamp/speakers/', data)
        self.assertEqual(response.status_code, 201)

    def test_http_post_will_create_speaker_and_return_created_speaker_json(self):
        data = {'name': 'who'}
        response = self.client.post('/codecamp/speakers/', data)
        created_speaker = json.loads(response.content)
        self.assertEqual(created_speaker['name'], 'who')

    def test_http_post_without_data_returns_400(self):
        response = self.client.post('/codecamp/speakers/', {})
        self.assertEqual(response.status_code, 400)

    def test_http_put_will_update_first_speaker_and_return_200(self):
        data = {'name': 'updated name'}
        response = self.client.put('/codecamp/speakers/{}/'.format(self.first_speaker.pk), data)
        self.assertEqual(response.status_code, 200)

    def test_http_put_will_update_first_speaker_and_return_updated_speaker_json(self):
        data = {'name': 'updated name'}
        response = self.client.put('/codecamp/speakers/{}/'.format(self.first_speaker.pk), data)
        updated_speaker = json.loads(response.content)
        self.assertEqual(updated_speaker['name'], 'updated name')

    def test_http_delete_will_remove_first_speaker_and_return_204(self):
        response = self.client.delete('/codecamp/speakers/{}/'.format(self.first_speaker.pk))
        self.assertEqual(response.status_code, 204)

    def test_http_delete_will_remove_first_speaker_and_return_empty_content(self):
        response = self.client.delete('/codecamp/speakers/{}/'.format(self.first_speaker.pk))
        self.assertEqual(response.content, '')

    def test_http_delete_will_return_404_when_incorrect_id_used_to_delete_speaker(self):
        response = self.client.delete('/codecamp/speakers/999999999999999999/')
        self.assertEqual(response.status_code, 404)

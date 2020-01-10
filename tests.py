from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

""" Sample Data """
sample_id_list = ['hY7m5jjJ9mM','CQ85sUNBK7w']
sample_song_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_song = {
    'title': 'Dont mean a thing',
    'composer': 'Duke Ellington',
    'subgenre': 'swing',
    'fileContents': 'fileContents'
}

sample_form_data = {
    'title': sample_song['title'],
    'composer': sample_song['composer'],
    'subgenre': sample_song['subgenre'],
    'fileContents': sample_song['fileContents']
}

class SongsTest(TestCase):
    """ Flask tests """
    def setUp(self):

        #Get the Flask test client
        self.client = app.test_client()

        #Show Flask erors that happen during tests
        app.config ['TESTING'] = True

    def test_index(self):
        """Test the playlists homepage"""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

    def test_new(self):
        """Test the new song creation page"""
        result = self.client.get('/songs_new')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_song(self, mock_find):
        """test showing a single song."""
        mock_find.return_value = sample_song

        result = self.client.get(f'/detail/{sample_song_id}')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_song(self, mock_find):
        """test editing a single song."""
        mock_find.return_value = sample_song

        result = self.client.get(f'/detail/{sample_song_id}/edit')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_song(self, mock_insert):
        '''Test submitting a new song'''
        result = self.client.post('/detail', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_song)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_song(self, mock_update):
            result = self.client.post(f'/detail/{sample_song_id}', data=sample_form_data)

            self.assertEqual(result.status, '302 FOUND')
            mock_update.assert_called_with({'_id': sample_song_id}, {'$set': sample_song})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_song(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/detail/{sample_song_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_song_id})

if __name__ == '__main__':
    unittest_main()

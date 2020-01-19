import mock
import unittest
import requests
import os
import shutil

from datetime import datetime
from requests.exceptions import HTTPError
from amcrest import AmcrestCamera
from amcrest.exceptions import CommError


def snapshot_query(query):
    url = "http://localhost:10000"
    params = {'action': 'getConfig'}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.content


class TestRequestsCall(unittest.TestCase):
    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        """
        helper function that builds mock responses
        """
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        with open('tests/snapshot.jpg', 'rb') as f:
            try:
                shutil.copyfileobj(f, mock_resp.raw)
            except HTTPError as error:
                raise CommError(error)
        return mock_resp

    @mock.patch('requests.get')
    def test_snapshot(self, mock_get):
        """test snaspshot query method"""
        mock_resp = self._mock_response(content="")
        mock_get.return_value = mock_resp
        now = datetime.now()
        path = os.path.join(os.getenv("HOME"), "tmp",
                            now.strftime("%Y%m%d-%H%M%S"))
        if not os.path.exists(path):
            os.mkdir(path)

        camera = AmcrestCamera('localhost', 10000, 'admin', 'admin').camera
        # Allows to bypass authentication
        camera._token = "XYZ"
        camera.snapshot(channel=1)
        # camera.snapshot(path_file=os.path.join(path,
        # "snapshot04.jpeg"), channel=1, stream=True)

        result = snapshot_query('')
        self.assertEqual(result, '')
        self.assertTrue(mock_resp.raise_for_status.called)

    @mock.patch('requests.get')
    def test_failed_query(self, mock_get):
        """test case where camera is down"""
        mock_resp = self._mock_response(
            status=500,
            raise_for_status=HTTPError("camera is down")
        )
        mock_get.return_value = mock_resp
        self.assertRaises(HTTPError, snapshot_query, 'camera')


if __name__ == '__main__':
    unittest.main()

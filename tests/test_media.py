"""Test log.py functions."""
import responses
import datetime

from .mocktestcase import MockTestCase


class TestMedia(MockTestCase):
    """Tests for media.py."""
    @responses.activate
    def test_download_file(self):
        self.add_init_responses()

        body = '*'.join([str(x) for x in range(17)])

        responses.add(
            responses.GET,
            self.format_url('RPC_Loadfile//mnt/sd/test.dat'),
            body=body,
            status=200)

        c = self.get_amcrest().camera
        content = c.download_file('/mnt/sd/test.dat').decode('utf-8')
        self.assertEqual(body, content)

    @responses.activate
    def test_log_find(self):
        self.add_init_responses()

        responses.add(
            responses.GET,
            self.format_url('mediaFileFind.cgi', {
                'action': 'factory.create'}),
            body='result=123\r\n',
            status=200)

        responses.add(
            responses.GET,
            self.format_url('mediaFileFind.cgi', {
                'action': 'findFile',
                'object': 123,
                'condition.Channel': 0,
                'condition.StartTime': datetime.datetime(2020, 1, 2, 3, 4, 5),
                'condition.EndTime': datetime.datetime(2020, 1, 2, 3, 4, 10)}),
            body='OK\r\n',
            status=200)

        url_next = self.format_url('mediaFileFind.cgi', {
            'action': 'findNextFile',
            'object': 123,
            'count': 100})

        responses.add(
            responses.GET,
            url_next,
            body='\r\n'.join('''found=2
items[0].Channel=0
items[0].Cluster=0
items[0].Compressed=false
items[0].Disk=0
items[0].Duration=480
items[0].EndTime=2020-01-06 06:13:00
items[0].Events[0]=VideoMotion
items[0].FilePath=/mnt/sd/2020-01-06/001/dav/06/06.05.00-06.13.00[M][0@0][0].mp4
items[0].Flags[0]=Event
items[0].Length=248362892
items[0].Overwrites=0
items[0].Partition=0
items[0].Redundant=false
items[0].Repeat=0
items[0].StartTime=2020-01-06 06:05:00
items[0].Summary.TrafficCar.PlateColor=Yellow
items[0].Summary.TrafficCar.PlateNumber=
items[0].Summary.TrafficCar.PlateType=Yellow
items[0].Summary.TrafficCar.Speed=60
items[0].Summary.TrafficCar.VehicleColor=White
items[0].SummaryOffset=0
items[0].Type=dav
items[0].WorkDir=/mnt/sd
items[0].WorkDirSN=0
items[1].Channel=0
items[1].Cluster=0
items[1].Compressed=false
items[1].Disk=0
items[1].Duration=480
items[1].EndTime=2020-01-06 06:21:00
items[1].Events[0]=VideoMotion
items[1].FilePath=/mnt/sd/2020-01-06/001/dav/06/06.13.00-06.21.00[M][0@0][0].mp4
items[1].Flags[0]=Event
items[1].Length=241799877
items[1].Overwrites=0
items[1].Partition=0
items[1].Redundant=false
items[1].Repeat=0
items[1].StartTime=2020-01-06 06:13:00
items[1].Summary.TrafficCar.PlateColor=Yellow
items[1].Summary.TrafficCar.PlateNumber=
items[1].Summary.TrafficCar.PlateType=Yellow
items[1].Summary.TrafficCar.Speed=60
items[1].Summary.TrafficCar.VehicleColor=White
items[1].SummaryOffset=0
items[1].Type=dav
items[1].WorkDir=/mnt/sd
items[1].WorkDirSN=0

'''.splitlines()),
            status=200)

        responses.add(
            responses.GET,
            url_next,
            body='\r\n'.join('''found=2
items[0].Channel=0
items[0].Cluster=0
items[0].Compressed=false
items[0].Disk=0
items[0].Duration=34
items[0].EndTime=2020-01-06 06:36:44
items[0].Events[0]=VideoMotion
items[0].FilePath=/mnt/sd/2020-01-06/001/dav/06/06.36.10-06.36.44[M][0@0][0].mp4
items[0].Flags[0]=Event
items[0].Length=17561629
items[0].Overwrites=0
items[0].Partition=0
items[0].Redundant=false
items[0].Repeat=0
items[0].StartTime=2020-01-06 06:36:10
items[0].Summary.TrafficCar.PlateColor=Yellow
items[0].Summary.TrafficCar.PlateNumber=
items[0].Summary.TrafficCar.PlateType=Yellow
items[0].Summary.TrafficCar.Speed=60
items[0].Summary.TrafficCar.VehicleColor=White
items[0].SummaryOffset=0
items[0].Type=dav
items[0].WorkDir=/mnt/sd
items[0].WorkDirSN=0

'''.splitlines()),
            status=200)

        responses.add(
            responses.GET,
            url_next,
            body='\r\n'.join('''found=0

'''.splitlines()),
            status=200)

        responses.add(
            responses.GET,
            self.format_url('mediaFileFind.cgi', {
                'action': 'factory.close',
                'object': 123}),
            body='\r\n'.join('''Error
ErrorID=2, Detail=Invalid Request!

'''.splitlines()),
            status=200)

        responses.add(
            responses.GET,
            self.format_url('mediaFileFind.cgi', {
                'action': 'factory.destroy',
                'object': 123}),
            body='\r\n'.join('''Error
ErrorID=2, Detail=Invalid Request!

'''.splitlines()),
            status=200)

        c = self.get_amcrest().camera
        time_start = datetime.datetime(2020, 1, 2, 3, 4, 5)
        time_end = datetime.datetime(2020, 1, 2, 3, 4, 10)
        media = list(c.find_files(time_start, time_end))
        self.assertEqual(2, len(media))

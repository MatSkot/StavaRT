import datetime
import unittest
from unittest import IsolatedAsyncioTestCase

from app.geodistance import get_distance_for_path, geo_distance
from app.libs.models import GeoPath, GeoCoords

PATH = [
    {"longitude": 16.955337524414062, "latitude": 51.05477573092765},
    {"longitude": 16.959457397460938, "latitude": 51.0301674442006},
    {"longitude": 16.963577270507812, "latitude": 51.00597815100905},
    {"longitude": 17.01644897460937, "latitude": 51.0107306152741},
    {"longitude": 17.060394287109375, "latitude": 51.03491742972195},
    {"longitude": 17.03018188476562, "latitude": 51.05563894221938},
    {"longitude": 17.00477600097656, "latitude": 51.07764539352731},
    {"longitude": 16.955337524414062, "latitude": 51.08842904844898},
    {"longitude": 16.950531005859375, "latitude": 51.109126619728926},
    {"longitude": 17.00408935546875, "latitude": 51.11171316466534},
    {"longitude": 17.065887451171875, "latitude": 51.103521942404186},
    {"longitude": 17.0947265625, "latitude": 51.07635118600777},
    {"longitude": 17.103652954101562, "latitude": 51.04571104081335},
    {"longitude": 17.110519409179688, "latitude": 51.0098665670808},
    {"longitude": 17.072067260742188, "latitude": 50.98609893339354},
    {"longitude": 17.00477600097656, "latitude": 50.96491387693772},
    {"longitude": 16.929931640625, "latitude": 50.96404897546097},
    {"longitude": 16.87774658203125, "latitude": 50.99128563729097},
    {"longitude": 16.864013671875, "latitude": 51.034485632974125},
    {"longitude": 16.857833862304688, "latitude": 51.076782592536524},
    {"longitude": 16.8804931640625, "latitude": 51.107402176013},
    {"longitude": 16.929931640625, "latitude": 51.12938401413808},
    {"longitude": 16.971817016601562, "latitude": 51.138432319543924},
    {"longitude": 16.950531005859375, "latitude": 51.14790959500491},
    {"longitude": 16.90933227539062, "latitude": 51.14704810491208},
    {"longitude": 16.872940063476562, "latitude": 51.13886314700494},
    {"longitude": 16.835861206054688, "latitude": 51.11904092252057},
    {"longitude": 16.810455322265625, "latitude": 51.093173060268896},
    {"longitude": 16.805648803710938, "latitude": 51.061249423389796},
    {"longitude": 16.811828613281246, "latitude": 51.02412130394265},
    {"longitude": 16.826934814453125, "latitude": 50.99603960672508},
    {"longitude": 16.845474243164062, "latitude": 50.97399437028297},
    {"longitude": 16.875, "latitude": 50.95280379090146},
    {"longitude": 16.915512084960938, "latitude": 50.93982519613568},
    {"longitude": 16.956710815429688, "latitude": 50.92597736758682},
    {"longitude": 17.025375366210938, "latitude": 50.90303283111257},
    {"longitude": 17.063827514648438, "latitude": 50.90996067566236},
    {"longitude": 17.109146118164062, "latitude": 50.93333453988655},
    {"longitude": 17.129058837890625, "latitude": 50.958426723359935},
    {"longitude": 17.137985229492188, "latitude": 50.984369903296745},
    {"longitude": 17.150344848632812, "latitude": 51.013322663272966},
    {"longitude": 17.148284912109375, "latitude": 51.0400986768664},
    {"longitude": 17.140045166015625, "latitude": 51.06470168927767},
    {"longitude": 17.136611938476562, "latitude": 51.081959157150536},
    {"longitude": 17.133865356445312, "latitude": 51.09187928712511},
    {"longitude": 17.127685546875, "latitude": 51.132400312945464},
    {"longitude": 17.13729858398437, "latitude": 51.16126063523994},
    {"longitude": 17.2320556640625, "latitude": 51.144894309328016},
    {"longitude": 17.3199462890625, "latitude": 51.04830113331224},
    {"longitude": 17.314453125, "latitude": 50.878777255570405}
]


class TestGeoDistance(IsolatedAsyncioTestCase):

    async def test_performance(self):
        st = datetime.datetime.now()
        model = GeoPath(geo_path=PATH)
        await get_distance_for_path(model.geo_path)
        execution_time = datetime.datetime.now() - st
        limit = datetime.timedelta(seconds=10)
        self.assertTrue(execution_time < limit)

    async def test_calculation(self):
        distance = await geo_distance(
            GeoCoords(**PATH[0]),
            GeoCoords(**PATH[1]))
        self.assertEqual(distance, 3573.481381993602)


class TestModels(unittest.TestCase):

    def test_valid(self):
        t00 = GeoCoords(**PATH[1])
        self.assertEqual(t00.dict(), PATH[1])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            GeoCoords(latitude=91, longitude='123,123a'),

    def test_to_short(self):
        with self.assertRaises(ValueError):
            GeoPath(geo_path=[PATH[1]])

    def test_to_long(self):
        with self.assertRaises(ValueError):
            GeoPath(geo_path=PATH+[PATH[6]])

from unittest import TestCase
from unittest.mock import Mock

from mapgenerator.algorithms.fortunes import event

class TestEvent(TestCase):
    def setUp(self):
        self.event_type = Mock(spec=event.EventType)
        self.point = Mock(spec=event.Point)

    def test_konstruktorille_pateva_piste(self):
        e = event.Event(10, self.event_type, self.point)

        self.assertAlmostEqual(e.point, self.point)

    def test_konstruktorille_pateva_site_event(self):
        event_type = event.EventType.SITE_EVENT

        e = event.Event(10, event_type, self.point)

        self.assertAlmostEqual(e.type, event_type)

    def test_konstruktorille_pateva_circle_event(self):
        event_type = event.EventType.CIRCLE_EVENT

        e = event.Event(10, event_type, self.point)

        self.assertAlmostEqual(e.type, event.EventType.CIRCLE_EVENT)

    def test_konstruktorille_epapateva_piste(self):
        point = 10

        with self.assertRaises(TypeError):
            e = event.Event(10, self.event_type, point)

    def test_konstruktorille_epapateva_event_tyyppi(self):
        event_type = 10

        with self.assertRaises(TypeError):
            e = event.Event(10, event_type, self.point)

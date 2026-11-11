import csv
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch
from carpark import CarParkingSystem

class ParkingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'records.csv'
        self.system = CarParkingSystem(self.path)

    def record(self, space, active=True):
        return ['LA07EDC', 'TICKET', str(space), '2026-11-11 10:00:00.000000',
                'Parking...' if active else '2026-11-11 11:00:00.000000', '2']

    def test_exited_cars_release_spaces(self):
        self.system.car_parking_records = [self.record(i, False) for i in range(1, 8)]
        self.assertIn(self.system.createParkingSpace(), range(1, 8))

    def test_full_car_park_returns_none(self):
        self.system.car_parking_records = [self.record(i) for i in range(1, 8)]
        self.assertIsNone(self.system.createParkingSpace())

    def test_only_unoccupied_space_allocated(self):
        self.system.car_parking_records = [self.record(i) for i in range(1, 7)]
        self.assertEqual(self.system.createParkingSpace(), 7)

    def test_empty_csv_is_supported(self):
        self.path.touch()
        self.assertEqual(CarParkingSystem(self.path).car_parking_records, [])

    def test_roundtrip_and_failed_replace_preserves_previous_file(self):
        self.system.car_parking_records = [self.record(1)]
        self.system.writeParkingRecords()
        original = self.path.read_bytes()
        self.system.car_parking_records.append(self.record(2))
        with patch('carpark.os.replace', side_effect=OSError('simulated disk failure')):
            with self.assertRaises(OSError): self.system.writeParkingRecords()
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(len(list(self.path.parent.iterdir())), 1)
        self.assertEqual(CarParkingSystem(self.path).car_parking_records, [self.record(1)])

    def test_negative_duration_cannot_create_negative_fee(self):
        self.assertEqual(self.system.calculateFee(timedelta(hours=-1)), 0)
        self.assertEqual(self.system.calculateFee(timedelta(minutes=90)), 3)

if __name__ == '__main__': unittest.main()

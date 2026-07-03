# assets/tests.py
from django.test import TestCase
from django.db import IntegrityError
from assets.models import Asset

class AssetModelTest(TestCase):

    def setUp(self):
        # Membuat data contoh awal untuk pengujian
        Asset.objects.create(
            equipment_id="PMP-01",
            equipment_name="Water Pump A",
            model_type="Centrifugal",
            serial_number="SN12345",
            capacity="11 kW",
            area=Asset.AreaChoices.PRODUCTION,
            location="Line 1"
        )

    def test_asset_creation_success(self):
        """Memastikan data aset berhasil disimpan dengan parameter yang benar"""
        asset = Asset.objects.get(equipment_id="PMP-01")
        self.assertEqual(asset.equipment_name, "Water Pump A")
        self.assertEqual(str(asset), "PMP-01 - Water Pump A")

    def test_duplicate_equipment_id_raised_error(self):
        """Memastikan sistem menolak Equipment ID yang kembar/duplikat"""
        with self.assertRaises(IntegrityError):
            Asset.objects.create(
                equipment_id="PMP-01",  # ID Sama
                equipment_name="Water Pump B",
                model_type="Submersible",
                location="Line 2"
            )
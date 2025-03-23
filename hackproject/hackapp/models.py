from django.db import models

class Farmer(models.Model):
    farmer_name = models.CharField(max_length=255)
    land_area = models.FloatField()
    assets_worth = models.FloatField()
    previous_loans = models.FloatField()
    paid_loans = models.FloatField()
    ongoing_loans = models.FloatField()
    assets_insurance_coverage = models.CharField(max_length=255)
    crop_name = models.CharField(max_length=255)
    water_availability = models.CharField(max_length=255)
    land_ownership = models.CharField(max_length=255)
    soil_quality = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    credit_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.farmer_name

    class Meta:
        db_table = 'hackapp_farmer'  # Explicitly set table name
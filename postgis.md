1. Install & Setup GeoDjango
Install dependencies

For PostgreSQL + PostGIS:

sudo apt install binutils libproj-dev gdal-bin postgis

Install Python package:

pip install psycopg[binary]  # for PostgreSQL

Update settings.py

INSTALLED_APPS = [
    ...
    'django.contrib.gis',
]

Set PostGIS backend:

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'your_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

2. Create a Model with PolygonField

from django.contrib.gis.db import models

class LandParcel(models.Model):
    name = models.CharField(max_length=255)
    boundary = models.PolygonField(geography=True, srid=4326)

    def __str__(self):
        return self.name

    geography=True → stores in GPS coordinates (WGS84)

    srid=4326 → standard for latitude/longitude

3. Create & Apply Migrations

python manage.py makemigrations
python manage.py migrate

4. Create Polygon Object in Python

from django.contrib.gis.geos import Polygon
from yourapp.models import LandParcel

# Polygon coordinates (longitude, latitude)
coords = [
    (30.1234, -0.1234),
    (30.1250, -0.1234),
    (30.1250, -0.1250),
    (30.1234, -0.1250),
    (30.1234, -0.1234),  # Last point must equal first
]

poly = Polygon(coords)

parcel = LandParcel.objects.create(name="Main Farm", boundary=poly)

5. Query Polygons

from django.contrib.gis.geos import Point

# Check if a point is inside a parcel
p = Point(30.124, -0.124)
LandParcel.objects.filter(boundary__contains=p)

Other spatial lookups:

    boundary__intersects

    boundary__within

    boundary__distance_lte

6. Use in Django Admin

from django.contrib.gis import admin
from .models import LandParcel

@admin.register(LandParcel)
class LandParcelAdmin(admin.OSMGeoAdmin):
    list_display = ('name',)

    OSMGeoAdmin gives a map widget in admin

    Allows drawing polygons directly on a map

7. Use in API (DRF)

If using DRF with GeoDjango:

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import LandParcel

class LandParcelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = LandParcel
        geo_field = "boundary"
        fields = ("id", "name", "boundary")

API POST example:

{
    "name": "Farm A",
    "boundary": {
        "type": "Polygon",
        "coordinates": [
            [
                [30.1234, -0.1234],
                [30.1250, -0.1234],
                [30.1250, -0.1250],
                [30.1234, -0.1250],
                [30.1234, -0.1234]
            ]
        ]
    }
}

Tips & Notes

    Polygon must be closed → first point = last point

    Coordinates order → (longitude, latitude)

    SRID 4326 → GPS coordinates

    Use PointField for single locations and PolygonField for areas

    GeoDjango + PostGIS gives access to spatial queries and map widgets

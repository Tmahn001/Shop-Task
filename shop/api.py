from django.contrib.gis.utils import GeoIP

g = GeoIP() 
lat,lng = g.lat_lon(user_ip)
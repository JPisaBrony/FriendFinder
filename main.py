from kivy.garden.mapview import MapView, MapMarker
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
import requests

class GpsTest(App):

    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def build(self):
        self.gps = gps
        self.markers = []
        try:
            self.gps.configure(on_location=self.on_location, on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        self.gps.start()
        self.mapview = MapView(zoom=20)
        layout = FloatLayout(oritentation='vertical')

        layout.add_widget(self.mapview)
        self.lat = Label(text="lat", font_size='50sp', pos=(0,0))
        self.lon = Label(text="lon", font_size='50sp', pos=(0,200))
        layout.add_widget(self.lat)
        layout.add_widget(self.lon)

        return layout
        #return self.mapview
        #return Builder.load_string(kv)

    @mainthread
    def on_location(self, **kwargs):
        items = []
        for k, v in kwargs.items():
            items.append(k)
            items.append(v)

        for x in self.markers:
            self.mapview.remove_marker(x)

        location = str(items[7]) + "_" + str(items[5])
        name = "josh"
        r = requests.get("http://students.cs.ndsu.nodak.edu/~philippy/response/a.php?info=" + name + "," + location)

        clients = r.text.split(";")

        for x in clients[:-1]:
            c = x.split(",")
            cord = c[1].split("_")
            m1 = MapMarker(lat=float(cord[0]), lon=float(cord[1]))
            self.mapview.add_marker(m1)
            self.markers.append(m1)

        self.mapview.center_on(items[7], items[5])
        self.lat.text = str(items[7])
        self.lon.text = str(items[5])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

if __name__ == '__main__':
    GpsTest().run()

from kivy.garden.mapview import MapView, MapMarker
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread

kv = '''
BoxLayout:
    orientation: 'vertical'

    Label:
        text: app.gps_location

    Label:
        text: app.gps_status

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'

        ToggleButton:
            text: 'Start' if self.state == 'normal' else 'Stop'
            on_state:
                app.gps.start() if self.state == 'down' else app.gps.stop()
'''


class GpsTest(App):

    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def build(self):
        self.gps = gps
        try:
            self.gps.configure(on_location=self.on_location, on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        #self.gps.start()
        #self.mapview = MapView(zoom=11, lon=2.000, lat=2.000)
        #self.mapview = MapView(zoom=11, lon=46.2342, lat=-96.2342)
        self.mapview = MapView(zoom=20, lat=50.6394, lon=3.057)
        self.mapview.map_source = "mapquest-osm"
        #m1 = MapMarker(lat=50.6394, lon=3.057)
        #mapview.add_marker(m1)
        #Builder.load_string(kv)
        return self.mapview
        #return Builder.load_string(kv)

    @mainthread
    def on_location(self, **kwargs):
        #self.gps_location = '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        items = []
        for k, v in kwargs.items():
            items.append(k)
            items.append(v)

        self.mapview.center_on(items[5], items[7])

        #self.gps_location = str(items[4]) + "=" + str(items[5]) + "\n" + str(items[6]) + "=" + str(items[7])

        #self.map.center_on()

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

if __name__ == '__main__':
    GpsTest().run()

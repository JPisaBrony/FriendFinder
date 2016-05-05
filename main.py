from kivy.garden.mapview import MapView, MapMarker
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests
import PIL
import PIL.Image
import PIL.ImageDraw

class GpsTest(App):

    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def build(self):
        self.gps = gps
        self.markers = []
        self.nametext = ""
        try:
            self.gps.configure(on_location=self.on_location)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        layout = BoxLayout(orientation='vertical')
        self.mapview = MapView(zoom=20)
        self.text = TextInput(text="Enter Name", size_hint=(1,0.05))
        self.but = Button(text="Submit", size_hint=(1,0.05))
        self.but.bind(on_press=self.start)
        layout.add_widget(self.text)
        layout.add_widget(self.but)
        layout.add_widget(self.mapview)
        return layout

    @mainthread
    def on_location(self, **kwargs):
        items = []
        for k, v in kwargs.items():
            items.append(k)
            items.append(v)

        for x in self.markers:
            self.mapview.remove_marker(x)

        location = str(items[7]) + "_" + str(items[5])
        r = requests.get("http://students.cs.ndsu.nodak.edu/~philippy/response/a.php?info=" + self.nametext + "," + location)

        clients = r.text.split(";")

        for x in clients[:-1]:
            c = x.split(",")
            cord = c[1].split("_")
            m1 = MapMarker(lat=float(cord[0]), lon=float(cord[1]))
            image = PIL.Image.new("RGBA", (80,50))
            draw = PIL.ImageDraw.Draw(image)
            draw.text((10,10), c[0], fill=(0,0,0))
            imger = c[0] + ".png"
            image.save(imger)
            m1.source = imger
            self.mapview.add_marker(m1)
            self.markers.append(m1)

        self.mapview.center_on(items[7], items[5])

    def start(self, value):
        self.nametext = self.text.text
        self.gps.start()

if __name__ == '__main__':
    GpsTest().run()

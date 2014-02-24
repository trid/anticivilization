from label import Label
from panel import Panel

__author__ = 'TriD'


class ExpeditionWidget(Panel):
    def __init__(self, x, y, expedition):
        Panel.__init__(self, x, y, 200, 80)
        self.expedition = expedition
        self.specialists_label = Label(0, 0, "Workers/Warriors: %d/%d" % (expedition.workers, expedition.warriors))
        self.people_label = Label(0, 20, "Population: %d" % expedition.people)
        self.destination_label = Label(0, 40, "Destination: (%d, %d)" % (expedition.path[0].x, expedition.path[0].y))
        self.regularity_label = Label(0, 60, "Regular: %s" % ("Yes" if expedition.regular else "No"))
        self.add(self.specialists_label)
        self.add(self.people_label)
        self.add(self.destination_label)
        self.add(self.regularity_label)
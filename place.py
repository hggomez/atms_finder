# This class emulates a tuple, but contains an id
class Place(object):
    def __init__(self, id, long, lat):
        self.id = id
        self.coords = (long, lat)

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        return self.coords[i]

    def __repr__(self):
        return 'Place({}, {}, {})'.format(self.coords[0], self.coords[1], self.id)
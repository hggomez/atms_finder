from haversine import haversine

# This class emulates a tuple, but contains an id
class Place(object):

  @classmethod
  def fromATM(cls, atm):
    return cls(atm.id, atm.lat, atm.long)

  @classmethod
  def haversine(cls, place1, location):
    return haversine(place1.coordinates, location)

  def __init__(self, id, lat, long):
      self.counter = 0
      self.id = id
      self.coordinates = (lat, long)

  def __len__(self):
      return len(self.coordinates)

  def __getitem__(self, i):
      return self.coordinates[i]

  def __repr__(self):
      return 'Place(lat: {}, long: {}, id: {})'.format(self.coordinates[0], self.coordinates[1], self.id)
# This class emulates a tuple, but contains an id
class ATM(object):

  def __init__(self, id, lat, long, bank, network, location, remaining_extractions):
      self.id = id
      self.lat = lat
      self.long = long
      self.bank = bank
      self.network = network
      self.location = location
      self.remaining_extractions = remaining_extractions

  def __repr__(self):
    return "( id: " + str(self.id) + ", lat: " +  str(self.lat) +\
      ", long: " +  str(self.long) +  ", bank: " +  str(self.bank) +\
      ", network: " +  str(self.network) + ", location: " +  str(self.location) +\
      ", remaining_extractions: " +  str(self.remaining_extractions) + " )"
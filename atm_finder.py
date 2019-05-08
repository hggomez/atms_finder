import sqlite3
import kdtree
from place import Place



class ATM_finder(object):
  def __init__(self):
    # TODO: CALCULATE A PROPER APROXIMATION OF 500M
    self.meters_500 = 234324.0
    # Indexes in the tuples returned from the db
    id = 0
    long = 1
    lat = 2

    self.connection = sqlite3.connect('cajeros-automaticos.db')
    cursor = self.connection.cursor()
    cursor.execute("select id, long, lat from 'cajeros-automaticos' where red = 'LINK';")
    self.finder = {}
    self.finder["LINK"] = kdtree.create([Place(c[id], c[long], c[lat]) for c in cursor.fetchall()])
    cursor.execute("select id, long, lat from 'cajeros-automaticos' where red = 'BANELCO';")
    self.finder["BANELCO"] = kdtree.create([Place(c[id], c[long], c[lat]) for c in cursor.fetchall()])


    # Create tree from list places

  def find_atms(self, location, network):
    atms = self.finder[network].search_knn(location, 3)
    # TODO: DROP ATMS OUT OF THE 500M RADIUS
    atms = [atm[0].data.id for atm in atms if atm[1] <= self.meters_500]
    cursor = self.connection.cursor()
    info_atm = lambda id : cursor.execute("select id, banco, ubicacion, extracciones_restantes from 'cajeros-automaticos' where id = {}".format(id)).fetchone()    
    atms = [info_atm(id) for id in atms]
    for i in atms:
      print(i)

atmloc = ATM_finder()
atmloc.find_atms([-58.3855564406903,-34.6110359897049], "LINK")
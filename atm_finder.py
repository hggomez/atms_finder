import sqlite3
import random
import kdtree
from place import Place
from atm import ATM
import schedule
from time import sleep
from threading import Thread

class ATM_finder(object):
  
  atm_fields = "id, lat, long, bank, network, address, remaining_extractions"

  def __init__(self):
    self.atms_amount = 3
    db_connection = self.db_connection()
    self.finder = {}
    cursor = db_connection.cursor()
    cursor.execute("select id, lat, long from 'atms' where network = 'LINK' and remaining_extractions != 0;")
    self.finder["LINK"] = kdtree.create([Place(*atm) for atm in cursor.fetchall()])
    cursor.close()
    cursor = db_connection.cursor()
    cursor.execute("select id, lat, long from 'atms' where network = 'BANELCO' and remaining_extractions != 0;")
    self.finder["BANELCO"] = kdtree.create([Place(*atm) for atm in cursor.fetchall()])
    cursor.close()
    db_connection.close()
    Thread(target = self.atm_refiller).start()

  def db_connection(self):
    return sqlite3.connect('atms.db')
 
  def atm_refiller(self):
      schedule.every().day.at('9:00').do(self.refill_atms)
      while True:
        schedule.run_pending()
        sleep(1)

  def refill_atms(self):
    if datetime.datetime.today().weekday() not in [5,6]:
      db_connection = sqlite3.connect('atms.db', timeout=30)
      db_connection.execute("update 'atms' set remaining_extractions = 1000;")
      db_connection.commit()
      db_connection.close()
  
  def random_atm(self, atms):
    if len(atms) == 1:
      return atms[0]
    elif len(atms) == 2:
      return random.choices(atms, cum_weights=[70,100])[0]
    else:
      return random.choices(atms, cum_weights=[70,90,100])[0]

  def find_atms(self, location, network):
    db_connection = self.db_connection()
    sorted_atms = self.finder[network].search_knn(location, self.atms_amount, dist=Place.haversine)
    node_info = 0
    distance_to_location = 1
    sorted_ids = [atm[node_info].data.id for atm in sorted_atms if atm[distance_to_location] <= 0.5]
    if len(sorted_ids) == 0:
      return []
    sorted_atms = self.atms_info(sorted_ids, db_connection)
    self.update_chosen_atm_info(sorted_atms, db_connection)
    db_connection.close()
    return sorted_atms

  def atms_info(self, sorted_ids, db_connection):
    cursor = db_connection.cursor()
    query_string = "select {0} from 'atms' where id = {1} ".format(self.__class__.atm_fields, sorted_ids[0])
    for id in sorted_ids[1:]:
      query_string = query_string + "or id = {0} ".format(id)
    atms = [ATM(*atm) for atm in cursor.execute(query_string).fetchall()]
    cursor.close()
    sorted_atms = [atm for atm, _ in sorted(zip(atms, sorted_ids), key=lambda pair: pair[1])]
    return sorted_atms

  def update_chosen_atm_info(self, sorted_atms, db_connection):
    chosen_atm = self.random_atm(sorted_atms)
    remaining_extractions = chosen_atm.remaining_extractions - 1
    query_string = "update 'atms' set remaining_extractions = {0} WHERE id = {1};"
    db_connection.execute(query_string.format(remaining_extractions, chosen_atm.id))
    db_connection.commit()
    if remaining_extractions == 0:
      chosen_atm = Place.fromATM(chosen_atm)
      self.finder[chosen_atm.network].remove(chosen_atm)
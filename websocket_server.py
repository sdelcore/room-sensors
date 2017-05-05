#!/usr/bin/python
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from room_sensors import Room_Sensors
import json

def date_handler(obj):
  if hasattr(obj, 'isoformat'):
    return obj.isoformat()
  else:
    raise TypeError

clients = []
class WS_Server(WebSocket):
  room = Room_Sensors()

  def handleMessage(self):
    to_get = {
  		"sound": [self.data],
  		"light": [self.data],
  		"temperature": [self.data, "dht11_temperature"],
  		"humidity": ["dht11_humidity"]
    }

    to_get = {"sensors": to_get[self.data]}
    readings = self.room.getReadingsFromDB(to_get)
    msg = json.dumps(readings, default=date_handler)

    for client in clients:
      	client.sendMessage(unicode(msg))

  def handleConnected(self):
    readings = self.room.getReadingsFromDB()
    msg = json.dumps(readings, default=date_handler)

    for client in clients:
      client.sendMessage(unicode(msg))
    
    clients.append(self)

  def handleClose(self):
    clients.remove(self)
    print(self.address, 'closed')
    
    for client in clients:
      client.sendMessage(self.address[0] + u' - disconnected')

server = SimpleWebSocketServer('', 8000, WS_Server)
server.serveforever()

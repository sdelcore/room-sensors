from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from room_sensors import Room_Sensors

class WS_Server:
  room = Room_Sensors()

	def handleMessage(self):
       for client in clients:
          if client != self:
            client.sendMessage(self.data)

  def handleConnected(self):
    print(self.address, 'connected')
    date = datetime.datetime.now()
    month = date.strftime("%m")
    day = date.strftime("%d")
    year = date.strftime("%Y")
    for client in clients:
      client.sendMessage(JSON.dumps(room.getReadingsFromDB(room.sensors.values(), day, month, year)))
    clients.append(self)

  def handleClose(self):
     clients.remove(self)
     print(self.address, 'closed')

server = SimpleWebSocketServer('', 8000, WS_Server)
server.serveforever()
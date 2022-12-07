from fastapi import FastAPI, Request

app = FastAPI()

activeRooms = []


class Message():
    def __init__(self,message,id,userId):
        self.message = message
        self.id = id
        self.userId = userId

class User():
    def __init__(self,name,id):
        self.name = name
        self.userId = id
    
    def getUserId(self):
        return self.id
        
class Room():
    def __init__(self,room_id):
        self.room_id = room_id
        self.activeUsers = 0
        self.currentMessageID = 0
        self.name = 0
        self.messages = []
        self.connectedUser = []

    def addUser(self,name):
        userId = self.currentUserId
        self.connectedUser.append(User(name,userId))
        self.currentUserId += 1
        self.activeUsers += 1
        return userId 
    
    def removeUser(self,userId):
        self.activeUsers -= 1
        return userId
    
    def storeMessage(self,message,userId):
        self.messages.append(Message(message,self.currentMessageID,userId))
        self.currentMessageID += 1



@app.get("/createRoom")
def create_room():
    roomId = len(activeRooms)
    newRoom = Room(roomId)
    activeRooms.append(newRoom)
    return {"roomId": len(activeRooms)-1}


@app.post("/joinRoom")
async def join_room(info : Request):
    data = await info.json()
    roomId = data['roomId']
    userName = data['userName']
    room = activeRooms[int(roomId)]
    userId = room.addUser(userName)
    return {"Status": "Success","userId":userId}

@app.post("/leaveRoom")
async def join_room(info : Request):
    data = await info.json()
    roomId = data['roomId']
    userId = data['userId']
    room = activeRooms[int(roomId)]
    room.removeUser(userId)
    return {"Status": "Success","RoomID":roomId}
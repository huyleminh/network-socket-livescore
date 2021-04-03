import threading

Thread = threading.Thread

class MainThreadServer(Thread):
    def __init__(self, serverSocket):
        Thread.__init__(self)
        self.daemon = True
        self._serverSocket = serverSocket # Server socket bind
        self._userConnections = []
        self._userAddresses = []

    def run(self):
        print("Server is listening new connections.")

        while True:
            try:
                userConnection, userAddress = self._serverSocket.accept()
                print(userAddress[0] + " has connected.")

                # Append user address
                # Append user connection
                self._userConnections.append(userConnection)

                # Create new thread for current user
                currentUserThread = Thread(target=self.childrenThread, args=(userConnection))
                currentUserThread.start()
            except:
                break

    def childrenThread(userConnection):
        userConnection.send(bytes("Welcome.", "utf8"))

        while True:
            userRequest = userConnection.recv(2048).decode("utf8")
            print("Receive: %s" %userRequest)

            if userRequest != "q":
                pass
            else:
                pass
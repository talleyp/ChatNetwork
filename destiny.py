import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time	


def on_message(ws, message):
    # if "NAMES" in message:
    # 	line = message.strip('NAMES ')
    # 	line = json.loads(line)
    # 	users = [x['nick'] for x in line["users"]]
    # 	print(users)
    # if "MSG" in message:
    # 	line = message.strip('MSG ')
    # 	line = json.loads(line)
    # 	sender = line["nick"]
    # 	msg = line["data"]
    # 	graph_creator.test_line(G,users, message=msg,sender=sender)


def on_error(ws, error):
    print("error: %s" % error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(30000):
            time.sleep(1)
            #ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://destiny.gg:9998/ws",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    G = nx.DiGraph()
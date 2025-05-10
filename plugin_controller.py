#import argparse
import queue
import threading

from pythonosc import dispatcher, osc_server, udp_client

from constants import RECEIVE_PORT, FORWARD_PORT
from logger import setup_logger
from utils import load_osc_addresses


logging = setup_logger("OSC Forwarder")
data_queue = queue.Queue()


def forward_osc_messages(client, osc_addresses, data_queue):

    while True:
        params = data_queue.get()
        if len(params) != len(osc_addresses):
            logging.error(f"Mismatch: received {len(params)} values, but {len(osc_addresses)} addresses are expected.")
        else:
            for addr, value in zip(osc_addresses, params):
                client.send_message(addr, value)
                logging.info(f"Sent {value} to {addr}")

        data_queue.task_done()


def receive_osc_params(unused_addr, *args):

    params = list(args)
    data_queue.put(params)
    logging.info(f"Received OSC message: {params}")


def main(filepath):

    # Load OSC addresses from the specified file
    osc_addresses = load_osc_addresses(filepath)
    if not osc_addresses:
        logging.error("No OSC addresses loaded! Exiting.")
        return

    # Set up the OSC client to send messages to REAPER
    client = udp_client.SimpleUDPClient("localhost", FORWARD_PORT)

    # Start the forwarding thread
    forwarding_thread = threading.Thread(
        target=forward_osc_messages, args=(client, osc_addresses, data_queue), daemon=True
    )
    forwarding_thread.start()

    # Set up the OSC server to receive messages
    dispatcher_map = dispatcher.Dispatcher()
    dispatcher_map.map("/interpolated_data", receive_osc_params)

    server = osc_server.ThreadingOSCUDPServer(("localhost", RECEIVE_PORT), dispatcher_map)
    logging.info(f"Receiving OSC messages on port {RECEIVE_PORT}, forwarding to REAPER on port {FORWARD_PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server.")
        server.shutdown()


### receive on 9109
### send on 9110
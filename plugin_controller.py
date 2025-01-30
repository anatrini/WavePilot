import argparse
import queue
import threading
from pythonosc import dispatcher, osc_server, udp_client
from logger import setup_logger
from utils import load_osc_addresses


def get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filepath',
                        dest='filepath',
                        type=str,
                        required=True,
                        help="Path to the JSON file containing OSC addresses.")

    parser.add_argument('-r', '--receive_port',
                        dest='receive_port',
                        type=int,
                        default=9109,
                        help="Port to receive OSC messages from external sources.")

    parser.add_argument('-s', '--send_port',
                        dest='send_port',
                        type=int,
                        default=9110,
                        help="Port to send OSC messages to REAPER.")

    return parser.parse_args()


logging = setup_logger('OSC Forwarder')
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


def main():

    args = get_arguments()

    filepath = args.filepath
    receive_port = args.receive_port
    send_port = args.send_port

    # Load OSC addresses from the specified file
    osc_addresses = load_osc_addresses(filepath)
    if not osc_addresses:
        logging.error("No OSC addresses loaded! Exiting.")
        return

    # Set up the OSC client to send messages to REAPER
    client = udp_client.SimpleUDPClient("localhost", send_port)


    # Start the forwarding thread
    forwarding_thread = threading.Thread(target=forward_osc_messages, args=(client, osc_addresses, data_queue), daemon=True)
    forwarding_thread.start()

    # Set up the OSC server to receive messages
    dispatcher_map = dispatcher.Dispatcher()
    dispatcher_map.map('/interpolated_data', receive_osc_params)

    server = osc_server.ThreadingOSCUDPServer(('localhost', receive_port), dispatcher_map)
    logging.info(f"Receiving OSC messages on port {receive_port}, forwarding to REAPER on port {send_port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server.")
        server.shutdown()


if __name__ == "__main__":
    main()


### receive on 9109
### send on 9110
import socket
import requests


class MessageServer:
    """Class that allows a connection to and from a single client."""
    def __init__(self):
        """Initialises server socket and listens for a connection."""
        self.server_socket = None
        self.listen_for_connection()

    def listen_for_connection(self):
        """Function that listens for a connection."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = '127.0.0.1'
        local_port = 65432

        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming connection...")
        self.server_socket.listen()

        self.connection, address = self.server_socket.accept()
        print(f"Connection to {address} established. Suilad!")

    def receive_message(self):
        """Function that receives a message from the connected client.

        Returns:
            str: The message from the client.
        """
        data = self.connection.recv(1024)

        if not data:
            return

        received_message = data.decode('utf-8')

        print(received_message)
        return received_message

    def send_message(self, message):
        """Function that sends a message to the connected client.

        Args:
            message (str): Message being sent to the client.
        """
        self.connection.sendall(str(message).encode('utf-8'))

    def close_server(self):
        """Function that closes the server socket."""
        self.server_socket.close()


class Translator:
    """Class that translates a message received by the server."""
    def __init__(self, url):
        self.url = url

    def translate(self, text):
        """Function that translates text.

        Args:
            text (str): Text from 

        Returns:
            (str): 
        """
        querystring = {
            "text": text
            }

        response = requests.request("POST", self.url, data=querystring)

        response_json = response.json()
        print(response_json)

        if "error" in response_json:
            return (response_json["error"]["message"], True)
        else:
            contents = response_json["contents"]
            translation = contents["translated"]
            return (translation, False)


# Class for Sindarin language. Tested to work with Quenya API, and open to adding more.
# Will need to add function to main() to determine user's translation choice.
class SindarinTranslator(Translator):
    def __init__(self):
        URL = "https://api.funtranslations.com/translate/sindarin.json"

        Translator.__init__(self, URL)


def main():

    translation_server = MessageServer()
    translator = SindarinTranslator()

    while True:
        message = translation_server.receive_message()

        if not message:
            continue

        if message == "/exit":
            break

        translation, is_error = translator.translate(message)
        translation_server.send_message(translation)

        if is_error:
            break

    translation_server.close_server()

main()

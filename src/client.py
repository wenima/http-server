"""Client side."""

import socket

message = """That's a saving of 6 characters per method. However, I don't believe Bruce proposes this so that he has to type less. I think he's more concerned about the time wasted by programmers (presumably coming from other languages) where the 'self' parameter doesn't need to be specified, and who occasionally forget it (even though they know better -- habit is a powerful force). It's true that omitting 'self' from the parameter list tends to lead to more obscure error messages than forgetting to type 'self.' in front of an instance variable or method reference. Perhaps even worse (as Bruce mentions) is the error message you get when the method is declared correctly but the call has the wrong number of arguments, like in this example given by Bruce: Let me first bring up a few typical arguments that are brought in against Bruce's proposal.

There's a pretty good argument to make that requiring explicit 'self' in the parameter list reinforces the theoretical equivalency between these two ways of calling a method, given """


def client(message):
    """Client function."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    print('sending the following message:', message, 'to server at: ', socket.gethostbyname('127.0.0.1'))
    client.sendall(message.encode('utf8'))
    buffer_length = 8
    reply_complete = False
    server_message = []
    while not reply_complete:
        part = client.recv(buffer_length)
        server_message.append(part.decode('utf8'))
        print('Receiving message from server...')
        print(server_message[-1])
        if len(part) < buffer_length:
            break
        else:
            print('Hold on, there is more...Receiving...')
    final_message = ''.join(server_message)
    print('The full message is: ', final_message)
    client.close()
    return final_message

client(message)

#This is an über secret special information about what happens at the CF office after midnight! Please treat with Confidentiality!")

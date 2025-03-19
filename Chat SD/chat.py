import grpc
import threading
import time
from concurrent import futures
import chat_pb2
import chat_pb2_grpc

# Servidor gRPC
class ChatServer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []
        self.lock = threading.Lock()

    def SendMessage(self, request, context):
        with self.lock:
            self.messages.append(request)
        return chat_pb2.Empty()

    def ReceiveMessage(self, request, context):
        last_index = 0
        while True:
            with self.lock:
                if len(self.messages) > last_index:
                    for msg in self.messages[last_index:]:
                        yield msg
                    last_index = len(self.messages)
            time.sleep(1)

# Função para iniciar o servidor gRPC
def start_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor iniciado na porta {port}")
    server.wait_for_termination()

# Função para enviar mensagens
def send_message(stub, sender):
    while True:
        content = input("Digite sua mensagem: ")
        if content.lower() == 'sair':
            break
        message = chat_pb2.Message(sender=sender, content=content)
        stub.SendMessage(message)

# Função para receber mensagens
def receive_messages(stub):
    while True:
        try:
            for message in stub.ReceiveMessage(chat_pb2.Empty()):
                print(f"{message.sender}: {message.content}")
        except grpc.RpcError as e:
            print(f"Erro ao receber mensagens: {e}. Tentando reconectar em 5 segundos...")
            time.sleep(5)

# Função principal para iniciar o chat
def start_chat(port1, port2, sender1, sender2):
    # Inicia o servidor para o primeiro nó
    server_thread1 = threading.Thread(target=start_server, args=(port1,))
    server_thread1.daemon = True
    server_thread1.start()

    # Inicia o servidor para o segundo nó
    server_thread2 = threading.Thread(target=start_server, args=(port2,))
    server_thread2.daemon = True
    server_thread2.start()

    # Aguarda os servidores iniciarem
    time.sleep(2)

    # Conecta o primeiro nó ao segundo
    channel1 = grpc.insecure_channel(f'localhost:{port2}')
    stub1 = chat_pb2_grpc.ChatServiceStub(channel1)

    # Conecta o segundo nó ao primeiro
    channel2 = grpc.insecure_channel(f'localhost:{port1}')
    stub2 = chat_pb2_grpc.ChatServiceStub(channel2)

    # Inicia as threads para enviar e receber mensagens
    send_thread1 = threading.Thread(target=send_message, args=(stub1, sender1))
    receive_thread1 = threading.Thread(target=receive_messages, args=(stub1,))

    send_thread2 = threading.Thread(target=send_message, args=(stub2, sender2))
    receive_thread2 = threading.Thread(target=receive_messages, args=(stub2,))

    send_thread1.start()
    receive_thread1.start()
    send_thread2.start()
    receive_thread2.start()

    send_thread1.join()
    receive_thread1.join()
    send_thread2.join()
    receive_thread2.join()

# Ponto de entrada do programa
if __name__ == '__main__':
    # Define as portas e os nomes dos usuários
    port1 = 50051
    port2 = 50052
    sender1 = "Alice"
    sender2 = "Bob"

    # Inicia o chat
    start_chat(port1, port2, sender1, sender2)
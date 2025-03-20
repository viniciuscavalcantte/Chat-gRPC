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
            print(f"Mensagem recebida de {request.sender}: {request.content}")  # Log de mensagem recebida
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
        try:
            stub.SendMessage(message)
            print(f"Mensagem enviada para o outro nó: {content}")  # Log de mensagem enviada
        except grpc.RpcError as e:
            print(f"Erro ao enviar mensagem: {e}")

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
def start_chat(port, target_port, sender):
    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()

    # Aguarda o servidor iniciar
    time.sleep(2)

    # Conecta ao outro nó com reconexão automática
    while True:
        try:
            print(f"Tentando conectar ao nó na porta {target_port}...")
            channel = grpc.insecure_channel(f'localhost:{target_port}')
            stub = chat_pb2_grpc.ChatServiceStub(channel)
            # Testa a conexão
            stub.SendMessage(chat_pb2.Message(sender=sender, content="Testando conexão..."))
            print(f"Conectado ao nó na porta {target_port}")
            break
        except grpc.RpcError as e:
            print(f"Erro ao conectar ao nó na porta {target_port}: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)

    # Inicia as threads para enviar e receber mensagens
    send_thread = threading.Thread(target=send_message, args=(stub, sender))
    receive_thread = threading.Thread(target=receive_messages, args=(stub,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

# Ponto de entrada do programa
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("Uso: python chat.py <porta_local> <porta_destino> <nome_usuario>")
        sys.exit(1)

    port = int(sys.argv[1])
    target_port = int(sys.argv[2])
    sender = sys.argv[3]

    start_chat(port, target_port, sender)

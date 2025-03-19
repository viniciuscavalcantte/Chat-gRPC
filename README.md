# Chat-gRPC

Um chat distribuído onde múltiplos nós enviam e recebem mensagens simultaneamente usando gRPC. Cada nó é cliente e servidor ao mesmo tempo.

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7+
- Instale as dependências:
  ```bash
  pip install grpcio grpcio-tools
  Passos
Clone o repositório:

bash
Copy
git clone https://github.com/viniciuscavalcantte/Chat-gRPC.git
cd Chat-gRPC
Compile o arquivo .proto:

bash
Copy
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
Execute o chat:

Modo Distribuído (dois nós separados):

bash
Copy
# Nó 1 (Alice)
python chat.py 50051 50052 Alice

# Nó 2 (Bob)
python chat.py 50052 50051 Bob
Modo Integrado (ambos os nós no mesmo script):

bash
Copy
python chat_integrado.py

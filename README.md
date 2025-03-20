# Sistema de Chat gRPC

Este projeto é uma implementação de um **chat usando gRPC**, onde as mensagens podem ser enviadas simultaneamente, ou seja, nao precisa esperar receber uma mensagem para poder enviar.

Este projeto é um requisito para obtenção de nota na disciplina **Sistemas Distribuídos**, ministrada pelo professor **Tércio Silva**.

---

## 📂 Estrutura do Projeto
```
├── Chat SD/
│   ├── chat.proto
│   └── chat.py
|   └── chat_pb2.py
|   └── chat_pb2_grpc.py
└── README.md
```

## 🚀 Tecnologias Utilizadas
- **Python 3**
- **gRPC**
- **Protocol Buffers**
- **Threading**
- **Concurrent Futures**

---

## ⚙️ Como Rodar o Projeto

### 1️⃣ Clone o repositório:
```bash
git clone https://github.com/seuusuario/chat-grpc.git
cd chat-grpc
```

### 2️⃣ Instale as dependências:
Certifique-se de ter o `pip` instalado e execute:
```bash
pip install grpcio grpcio-tools
```

### 3️⃣ Gere os arquivos gRPC:
Para gerar os arquivos a partir do arquivo `chat.proto`, rode:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
```

### 4️⃣ Como testar, Terminal 1 (Alice):
Para iniciar o servidor na porta 50051, no terminal 1 execute:
```bash
python chat.py 50051 50052 Alice 
```

### 5️⃣ Terminal 2 (Bob):
Execute
```bash
python chat.py 50052 50051 Bob
```

### 💡 Enviando Mensagens
- Digite sua mensagem e pressione **Enter** para enviar.
- Para sair do chat, digite:  
  ```
  sair
  ```

---

## 🌐 Funcionamento do Chat

### 🖥️ Servidor
- Inicializa e escuta conexões dos clientes.
- Utiliza gRPC para gerenciar as trocas de mensagens de forma simultânea.
- Permite o envio e recebimento de mensagens sem bloqueio.

### 💻 Cliente
- Conecta ao servidor gRPC e permite o envio de mensagens em tempo real.
- Recebe mensagens dos demais clientes conectados ao servidor.

---

## 📝 Protocol Buffers (chat.proto)

O arquivo `chat.proto` define a estrutura das mensagens e os serviços oferecidos pelo servidor, incluindo:
- **Mensagem de Texto**: Estrutura que contém o nome do remetente e o conteúdo da mensagem.
- **Serviço de Chat**: Define métodos para enviar e receber mensagens.

**Estrutura do arquivo `chat.proto`:**
```proto
syntax = "proto3";

service ChatService {
    rpc SendMessage (Message) returns (Empty);
    rpc ReceiveMessage (Empty) returns (stream Message);
}

message Message {
    string sender = 1;
    string content = 2;
}

message Empty {}
```

---

## 🚩 Finalizando o Servidor
Para encerrar o servidor, utilize `Ctrl + C` no terminal onde ele está rodando.

---

## 💡 Observações
- O sistema utiliza threads para permitir o envio e recebimento de mensagens simultaneamente.
- Em caso de falha de conexão, o cliente tenta reconectar automaticamente a cada 5 segundos.

---

## 👥 Desenvolvedores
- **José Vinicius Cavalcante Soares** - 22112113  
- **Liedson da Silva Santos** - 22110823  
- **Thalia de Oliveira Santos** - 21110245  

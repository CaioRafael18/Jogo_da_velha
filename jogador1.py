import socket
import threading 

class Jogo_da_Velha:

    def __init__(self):
        self.placar = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.vez = "X"
        self.voce = "X"
        self.adversario = "0"
        self.vencedor = None
        self.fim_de_jogo = False

        self.counter = 0

    def host_game(self,host,port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(1)

        client, addr = server.accept()

        self.voce = "X"
        self.adversario = "0"
        threading.Thread(target=self.conexao, args=(client,)).start()
        server.close()

    def conectar_o_jogo(self,host,port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host,port))

        self.voce = "0"
        self.adversario = "X"
        threading.Thread(target=self.conexao, args=(client,)).start()

    def conexao(self,client):
        while not self.fim_de_jogo:
            if self.vez == self.voce:
                move = input("Faça sua jogada! (linha,coluna[0,1,2] ex:0,0): ")
                if self.verificar_movimento(move.split(',')):
                    client.send(move.encode('utf-8'))
                    self.movimento(move.split(','), self.voce)
                    self.vez = self.adversario
                else:
                    print("Movimento inválido, por favor tente novamente!")
            else:
                data = client.recv(1024)
                if not data:
                    break
                else: 
                    self.movimento(data.decode('utf-8').split(','), self.adversario)
                    self.vez = self.voce
        client.close()
    
    def movimento(self,move,player):
        if self.fim_de_jogo:
            return
        self.counter += 1
        self.placar[int(move[0])][int(move[1])] = player
        self.print_placar()
        if self.verificar_vencedor():
            if self.vencedor == self.voce:
                print("Parabéns, você ganhou!")
                exit()
            elif self.vencedor == self.adversario:
                print("Você Perdeu! Boa sorte na Proxima!")
                exit()
        else:
            if self.counter == 9:
                print("ahhhh que pena, Deu empate! Tente novamente!")
                exit()
    def verificar_movimento(self,move):
        return self.placar[int(move[0])][int(move[1])] == " "
    
    def verificar_vencedor(self):
        for linha in range(3):
            if self.placar[linha][0] == self.placar[linha][1] == self.placar[linha][2] != " ":
                self.vencedor = self.placar[linha][0]
                self.fim_de_jogo = True
                return True
        for coluna in range(3):
            if self.placar[0][coluna] == self.placar[1][coluna] == self.placar[2][coluna] != " ":
                self.vencedor = self.placar[0][coluna]
                self.fim_de_jogo = True
                return True
        if self.placar[0][0] == self.placar[1][1] == self.placar[2][2] != " ":
            self.vencedor = self.placar[0][0]
            self.fim_de_jogo = True
            return True
        if self.placar[0][2] == self.placar[1][1] == self.placar[2][0] != " ":
            self.vencedor = self.placar[0][2]
            self.fim_de_jogo = True
            return True
        return False
    
    def print_placar(self):
        for linha in range(3):
            print(" | ".join(self.placar[linha]))
            if linha != 2:
                print("-------")

game = Jogo_da_Velha()
game.host_game("localhost", 1010)



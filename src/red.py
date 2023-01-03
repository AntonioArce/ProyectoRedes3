from router import Router
import logging
import networkx as nx
import matplotlib.pyplot as plt

class Red():

    def __init__(self, ip, name, user="root", password="root"):
        self.ip = ip
        self.name = name
        self.user = user
        self.password = password
        self.routers = {}

    def leerTopologia(self):
        # Obteniendo información de los routers
        router_cercano = Router(self.ip, self.name, self.user, self.password)
        print(router_cercano)
        router_cercano.buscarVecinos(self.routers)

        
        # Generando gráfico
        plt.clf() # Limpiando imagen
        G = nx.Graph()
        print(self.routers)
        for router in self.routers: # Agregando routers
            print("si grafico")
            G.add_node(router, name=router)
        for r1 in self.routers: # Generando conexiones
            for r2 in self.routers[r1]["conectados"]:
                print("si")
                G.add_edge(r1, r2)

        nx.draw_networkx(G, with_labels=True, node_color="r") # Creando gráfico
        plt.savefig("static/topologia.jpg")
    
    def obtenerRouters(self):
        return self.routers
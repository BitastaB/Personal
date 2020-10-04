import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D
import time

def plot(w,G,t,ax1):
    ax1.set_title(f"Iteration : {t}")
    artists = [ax1.scatter(w[:,0],w[:,1],w[:,2],c = 'r',s=5)]
    for i,e in enumerate(G.edges()):
        artists.extend(ax1.plot([w[e[0]][0], w[e[1]][0]], [w[e[0]][1], w[e[1]][1]],[w[e[0]][2], w[e[1]][2]],c = 'black'))
    plt.pause(0.15)
    plt.savefig('/home/bitasta/PycharmProjects/SOM/Csv-for-exam/som-old-ring-online.png')
    for a in artists:
        a.remove()
    #time.sleep(.05)


def initGraph(kx,ky):
  #  print("init graph")
#uncomment for grid G
  #  G = nx.generators.lattice.grid_2d_graph(kx,ky)
#uncomment for ring G
    G = nx.generators.lattice.grid_2d_graph(kx, 1, periodic=True)

    G = nx.convert_node_labels_to_integers(G)
    return G

def som(arr,ax1):
    k = np.size(arr,0)
   # print("k : ",k)

    #Initialize the graph with random weight vectors
    kx=24
    ky=5
    G = initGraph(kx,ky)

    #Max no. of desired iterations
    tMax = 10000

    #randomly choosing weight vector from sample space of arr

    #uncomment for grid G
   # random_indices = np.random.choice(arr.shape[0], size = kx*ky, replace=False)

    #uncomment for ring G
    random_indices = np.random.choice(arr.shape[0], size = kx, replace=False)
    w = arr[random_indices, :]


    #topological distance matrix D
    D = np.asarray(nx.floyd_warshall_numpy(G))**2


    for t in range(tMax):

        #randomly choosing a sample point from arr
        random_indices = np.random.choice(k, size=1, replace=False)
        x = arr[random_indices, :]

        #calculating closest weight vector : winner neuron
        i = np.argmin(np.linalg.norm((w-x),axis=1))
        winner_neuron = w[i]


        #learning rate
        etaT = 1 - t/tMax

        #topological adaption rate
        sigmaT = np.exp(-t/tMax)


        #update each weight vector
        for j in range(w.shape[0]):

        #neighbourhood function
            h = np.exp((-D[i][j]**2)/(2*sigmaT))
            w[j] = w[j]+(etaT * h * (x - w[j]))

     #   for n,v in enumerate (G):
            #print("n = ",n," ",w[n])
    #       G.nodes[v]['pos'] = w[n]

        plot(w,G,t,ax1)
    return w

fig = plt.figure(figsize=(10,7))
ax1 = fig.add_subplot(1, 1, 1,projection='3d')
arr=np.genfromtxt('q3dm1-path1-old.csv', delimiter=',', encoding="utf-8-sig")
ax1.scatter(arr[:,0],arr[:,1],arr[:,2],c = 'b',s=1)
w = som(arr,ax1)

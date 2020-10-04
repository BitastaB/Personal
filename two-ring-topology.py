import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot(w,G,t,ax1):
    ax1.set_title(f"Iteration : {t+1}")
    artists = [ax1.scatter(w[:,0],w[:,1],w[:,2],c = 'blue',s=45,zorder=5)]
    for i,e in enumerate(G.edges()):
        artists.extend(ax1.plot([w[e[0]][0], w[e[1]][0]], [w[e[0]][1], w[e[1]][1]],[w[e[0]][2], w[e[1]][2]], c='blue',zorder=5))
    plt.pause(0.01)
    plt.savefig("/home/bitasta/PycharmProjects/SOM/Images/som-2-ring_online_10000.png")
    for a in artists:
        a.remove()


def initGraph(k):

    k = int(k/2)
    G1 = nx.generators.lattice.grid_2d_graph(k, 1, periodic=True)
    G2 = nx.generators.lattice.grid_2d_graph(k, 1, periodic=True)
    G = nx.union(G1, G2,rename=('G1-','G2-'))
    G = nx.convert_node_labels_to_integers(G)
    for i,j in zip(range(k),range(k,k*2)):
        G.add_edge(i,j)
    return G


def somBatch(arr,ax1):
    n = np.size(arr,0)
    b = np.zeros(n,dtype=int)
    #Initialize the graph with random weight vectors
    k=24
    G = initGraph(k)

    #Max no. of desired iterations
    tMax = 200

    #randomly choosing weight vector from sample space of arr
    random_indices = np.random.choice(arr.shape[0], size = k, replace=False)
    w = arr[random_indices, :]


    #topological distance matrix D
    D = np.asarray(nx.floyd_warshall_numpy(G))**2


    for t in range(tMax):

        for j in range(n):
            b[j] = np.argmin(np.linalg.norm((w-arr[j])**2,axis=1))

        #topological adaption rate
        sigmaT = np.exp(-t/tMax)


        #update each weight vector
        for i in range(w.shape[0]):

            q = 0
            v = 0
        #neighbourhood function
            for j in range(n):
                h = np.exp((-D[b[j]][i]**2)/(2*sigmaT**2))
                q = q+(arr[j]*h)
                v = v + h
            w[i] = q/v
        plot(w,G,t,ax1)
    return w

def somOnline(arr,ax1):
    k = np.size(arr,0)
   # print("k : ",k)

    #Initialize the graph with random weight vectors
    kx=24

    G = initGraph(kx)

    #Max no. of desired iterations
    tMax = 10000

    #randomly choosing weight vector from sample space of arr

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
        i = np.argmin(np.linalg.norm((w-x)**2,axis=1))
        winner_neuron = w[i]
        #print("w.shape",w.shape)

        #learning rate
        etaT = 1 - t/tMax

        #topological adaption rate
        sigmaT = np.exp(-t/tMax)

        #update each weight vector
        for je in range(w.shape[0]):

        #neighbourhood function
            #print("i = ",i," j = ",je)
            h = np.exp((-D[i][je]**2)/(2*sigmaT**2))
            w[je] = w[je]+(etaT * h * (x - w[je]))

        plot(w,G,t,ax1)
    return w

fig = plt.figure(figsize=(7,5))
ax1 = fig.add_subplot(1, 1, 1,projection='3d')
arr=np.genfromtxt('q3dm1-path1-old.csv', delimiter=',', encoding="utf-8-sig")
ax1.scatter(arr[:,0],arr[:,1],arr[:,2],c = 'black',s=10,alpha=0.1)
w = somBatch(arr,ax1)

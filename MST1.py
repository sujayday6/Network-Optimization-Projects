
'''
Here change the number of vertices on line number 13 and input file name on line number 119
also change the number of edges on line numer 212 
'''
from gurobipy import *

#from math import sqrt
#import matplotlib.pyplot as plt


class MST:
    nvertices =100  # enter number of vertices in graph
    nedges =  212   # Enter number of edges
    weight = []
    location=[]
    MST_Model = Model()
    x = tupledict()

    def read(self, inputfile):
        f = open(inputfile, 'r')
        line = f.readline()
        fields = str.split(line)



        for i in range(self.nedges):
            self.location.append([])
        for i in range(self.nvertices):
            self.weight.append([0 for i in range(self.nvertices)])

        n = 0
        for line in f:
            fields = line.split(',')
            loc_x = int(fields[0])
            loc_y = int(fields[1])
            dist = int(fields[2])
            self.location[n] = [loc_x, loc_y,dist]
            n += 1
        f.close



        for i in range(self.nvertices):
            for j in range(self.nvertices):
                self.weight[i][j]=0

        for i in range(self.nedges):
            a=self.location[i][0]
            b=self.location[i][1]
            self.weight[a][b]=self.location[i][2]
            self.weight[b][a]=self.location[i][2]



    def initialize(self):
        for i in range(self.nvertices):
            for j in range(self.nvertices):
                if i != j and self.weight!=0:
                    self.x[i,j] = self.MST_Model.addVar(vtype=GRB.BINARY, obj = self.weight[i][j], name='x_{}{}'.format(i,j))

        self.MST_Model.modelSense = GRB.MINIMIZE
        self.MST_Model.Params.lazyConstraints = 1
        self.MST_Model.update()


        self.MST_Model.addConstr((quicksum(self.x[i,j] for i in range(self.nvertices)for j in range(self.nvertices) if self.weight[i][j]!=0 and i!=j)) == (self.nvertices-1))#, name='leave_{}'.format(i))

    def solve(self):


        def subtourelim(model, where):
            if where == GRB.callback.MIPSOL:
                    edges = []
                #for i in range(n):
                    x_sol = model.cbGetSolution(model._x)
                    edges = tuplelist((i,j) for i,j in model._x.keys() if x_sol[i,j] > 0.5)
                    adjList = [[] for i in range(self.nvertices)]
                    for i, j in edges:
                        adjList[i].append(j)
                    # find the shortest cycle in the selected edge list
                    components = subtour(adjList)
                    print(components)
                    count = 0
                    if len(components) > 1:
                        # add a subtour elimination constraint
                        for component in components:

                         if len(component)>=2:
                             count+=1
                        if count>1:
                         for component in components:
                            if(len(component)>=2):
                                #print('Add constraint for component: {}'.format(component))
                                model.cbLazy(quicksum(self.x[i,j] for i in component for j in component if i != j) <= len(component) - 1)

        def subtour(adjList):
            discover = [0 for i in range(self.nvertices)]
            components = []
            for i in range(self.nvertices):
                component = []
                queue = []
                if discover[i] == 0:
                    discover[i] = 1
                    component.append(i)
                    queue.append(i)
                    while queue:
                        v = queue.pop(0)
                        for u in adjList[v]:
                            if discover[u] == 0:
                                discover[u] = 1
                                component.append(u)
                                queue.append(u)
                    components.append(component)
            return components



        '''
        def subtourelim(model, where):
            if where == GRB.Callback.MIPSOL:
                #model._iter += 1
                ########### Get Solution ########
                x_sol = model.cbGetSolution(model._x)
                edges = tuplelist((i,j) for i,j in model._x.keys() if x_sol[i,j] > 0.5)
                adjList = [[] for i in range(self.nvertices)]
                for i, j in edges:
                    adjList[i].append(j)
                #plotSolution(edges, model._iter)
                ########### Separation Algorithm ##########
                discover = [0 for i in range(self.nvertices)]
                components = []
                for i in range(self.nvertices):
                    component = []
                    queue = []
                    if discover[i] == 0:
                        discover[i] = 1
                        component.append(i)
                        queue.append(i)
                        while queue:
                            v = queue.pop(0)
                            for u in adjList[v]:
                                if discover[u] == 0:
                                    discover[u] = 1
                                    component.append(u)
                                    queue.append(u)
                        components.append(component)

                for component in components:
                    if len(component) >=2:
                        print('Add constraint for component: {}'.format(component))
                        model.cbLazy(quicksum(self.x[i,j] for i in component for j in component if i != j) <= len(component) - 1)
        #
        '''

        #
        #
        self.MST_Model._x = self.x
        #self.TSP_Model._iter = iter
        self.MST_Model.params.LazyConstraints = 1
        self.MST_Model.optimize(subtourelim)
        for i in range(self.nvertices):
            for j in range(self.nvertices):
                if i!=j and self.weight[i][j]!=0:
                    print("x[%d][%d]=%d"%(i,j,self.x[i,j].x))





instance = MST()
instance.read('100Nodes.dat')
instance.initialize()
instance.solve()

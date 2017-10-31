#!/usr/bin/env python
from graph_tool.all import *

def main():
	v = []
	minimalPaths = []
	global reliability

	loadGraph = input("Carregar grafo? (y/n): ")
	if loadGraph == "y":
		#Carrega grafo salvo
		which = input("1- 5v7e\n2- 5v5e\n3- 7v11e\n")
		if which == "1" or which == "5v7e":
			g = load_graph("graph5v7e.xml.gz")
			for vertex in g.get_vertices():
				v.append(vertex)
		elif which == "2" or which == "5v5e":
			g = load_graph("graph5v5e.xml.gz")
			for vertex in g.get_vertices():
				v.append(vertex)
		elif which == "3" or which == "7v11e":
			g = load_graph("graph7v11e.xml.gz")
			for vertex in g.get_vertices():
				v.append(vertex)
		vprob = input("Confiabilidade dos vértices: ")
	else:
		#Gera novo grafo
		g = generateGraph()
		for vertex in g.get_vertices():
			v.append(vertex)
		#g = randomGraph()
		vprob = input("Confiabilidade dos vértices: ")
		#Define uma propriedade para os vértices
		vertice_prob = g.new_vertex_property("double")
		g.vp.prob = vertice_prob
	#Carrega propriedades dos vértices
	for i in g.get_vertices():
		g.vp.prob[i] = vprob

	#Desenha novo grafo e salva
	#graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(200, 200), output="graph7v11e.png")
	#g.save("graph7v11e.xml.gz")

	#Encontra caminhos mínimos entre o primeiro e último vértices
	for path in all_paths(g, v[0], v[-1]):
		minimalPaths.append(path)
	overlap(g, minimalPaths, minimalPaths[:], "sub")
	print("Confiabilidade do grafo = {}".format(reliability))

def generateGraph():
	#Gera novo grafo
	g = Graph(directed = False)
	for i in range(8):
		vertex = g.add_vertex()
	g.add_edge(v[0], v[1])
	g.add_edge(v[0], v[2])
	g.add_edge(v[0], v[3])
	g.add_edge(v[1], v[4])
	g.add_edge(v[1], v[5])
	g.add_edge(v[2], v[5])
	g.add_edge(v[2], v[6])
	g.add_edge(v[3], v[6])
	g.add_edge(v[4], v[7])
	g.add_edge(v[5], v[7])
	g.add_edge(v[6], v[7])

	return g

def randomGraph():
	#Gera grafo aleatório com vértices definidos em n e grau de cada um definido em degree
	n = int(input("Numero de Vertices: "))
	g = random_graph(N=n, deg_sampler=degree, directed=False)
	return g

def degree():
	#Define o grau de cada vértice.
	#Deve retornar uma tupla de dois inteiros para graus interno e externo em grafos dirigidos, ou um inteiro para grafos não-dirigidos.
	return 2

def overlap(g, mainStack, stack, previousOperation):
	global reliability
	# step1
	if stack == mainStack:
		operation = "sum"
	elif stack != mainStack and previousOperation == "sub":
		operation = "sum"
	else:
		operation = "sub"
	# step2
	delete = []
	for i in range(len(stack)-2):
		for j in range(i+1, len(stack)-1):
			if set(stack[i]).intersection(stack[j]) == set(stack[i]):
				if j not in delete:
					delete.append(j)
			elif set(stack[i]).intersection(stack[j]) == set(stack[j]):
				if i not in delete:
					delete.append(i)
	delete.sort()
	for i in delete[::-1]:
		del stack[i]
	# step3
	if len(stack) == 1:
		if operation == "sum":
			for path in stack:
				pathReliability = 1
				for node in path:
					pathReliability *= g.vp.prob[node]
				reliability += pathReliability
		else:
			for path in stack:
				pathReliability = 1
				for node in path:
					pathReliability *= g.vp.prob[node]
				reliability -= pathReliability
		return
	# step4
	if operation == "sum":
		for path in stack:
			pathReliability = 1
			for node in path:
				pathReliability *= g.vp.prob[node]
			reliability += pathReliability
	else:
		for path in stack:
			pathReliability = 1
			for node in path:
				pathReliability *= g.vp.prob[node]
			reliability -= pathReliability
	# step5
	if len(stack) > 1:
		for i in range(1, len(stack)):
			newStack = []
			for j in range(i):
				newStack.append(list(set(stack[i]).union(stack[j])))
			overlap(g, mainStack, newStack, operation)
	# step6
	return

if __name__ == '__main__':
	reliability = 0
	main()

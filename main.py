from app.window import Window
from robot.graph import Graph

# window class with tkinter usage
window = Window("Test", 500, 500)

# graph class for showing 3D graph and visualizing robot movement
graph = Graph()


graph.plot_graph(window.root)
window.run()

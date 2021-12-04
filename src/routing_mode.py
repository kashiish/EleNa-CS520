from abc import ABC, abstractmethod
import osmnx

class RoutingMode(ABC):
	"""
		RoutingMode interface defines actions that will be used by all the routing modes, but implemented with different behavior. It will also have the shared operations that will be used across all routings.

		The Context class can use this routing strategy. 

		Cite: https://www.tutorialspoint.com/design_pattern/strategy_pattern.html
	"""

	def __init__(self):
		pass

	@abstractmethod
	def routing_action(self, graph, start, end, x, elevation_setting):
		pass

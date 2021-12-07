class Context:
    """
    Context uses the routing actions of each defined strategy.
    """

    def __init__(self, routing_mode):
        self._routing_mode = routing_mode

    @property
    def routing_mode(self):
        """
        Get the routing mode (strategy)
        """
        return self._routing_mode

    @routing_mode.setter
    def routing_mode(self, routing_mode):
        """
        Set the routing mode (strategy)
        """
        self._routing_mode = routing_mode

    def execute_routing_mode(self, graph, start, end, x=0, elevation_setting=None):
        """
        Execute routing algorithm of chosen strategy.
        """
        return self._routing_mode.routing_action(graph, start, end, x, elevation_setting)
        
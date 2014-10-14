import ProbabilityTable

class Node(object):
    """
    A BeliefNode represents an event in a belief network. Such an event holds a table of probabilities
        which define a relationship between its influencers (input nodes), and its influencees (output nodes).

    As input, a BeliefNode takes in a set of booleans representing the state of events stored in the BeliefNode's table.
        The BeliefNode will then use these knowns and its set of posteriors to produce an output.

    The output of a BeliefNode is a constant value, P, where 0 <= P <= 1. This value represents the likelihood of a queried event occuring
        given all other knowledge of the system.

    """
    def __init__(self, event_name, parents = [], prob_func = None):
        """
        BeliefNode Parameters:

        event_name (string): describes event represented by node (e.g: "Player is bluffing")
        cpt (array of ProbabilityTable): a collection of poterior probabilities
        prob_func (function): the function used by the node to compute probability
        parents (list of BeliefNode or None): the events which influence the probability of this event
        children (list of BeliefNode or None): the events where are influenced by the probability of this event
        """

        self.event_name = event_name
        self.cpt = None
        self.prob_func = prob_func
        self.parents = parents
        self.children = []

    def __eq__(self, other):
        return self.event_name == other.event_name

    def __repr__(self):
        """ Magic method to describe node in a print statement """
        return "Event: %s" % self.event_name, self.cpt

    def influences(self, node):
        self.children.append(node)

    def influencedBy(self, node):
        self.parents.append(node)


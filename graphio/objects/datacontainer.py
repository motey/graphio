from graphio import NodeSet, RelationshipSet


class Container:
    """
    A container for a collection of Nodes, Relationships, NodeSets and RelationshipSets.

    A typical parser function to e.g. read an Excel file produces a mixed output which then has to
    be processed accordingly.

    Also, sanity checks and data statistics are useful.
    """

    def __init__(self, objects=None):
        self.objects = []

        # add objects if they are passed
        if objects:
            for o in objects:
                self.objects.append(o)

    @property
    def nodesets(self):
        """
        Get the NodeSets in the Container.
        """
        return get_instances_from_list(self.objects, NodeSet)

    @property
    def relationshipsets(self):
        """
        Get the RelationshipSets in the Container.
        """
        return get_instances_from_list(self.objects, RelationshipSet)

    def get_nodeset(self, labels, merge_keys):
        for nodeset in self.nodesets:
            if set(nodeset.labels) == set(labels) and set(nodeset.merge_keys) == set(merge_keys):
                return nodeset

    def get_relationshipset(self, rel_type: str):
        return next([r for r in self.relationshipsets if r.rel_type == rel_type], None)

    def add(self, object):
        self.objects.append(object)

    def add_all(self, objects):
        for o in objects:
            self.add(o)

    def merge_nodesets(self):
        """
        Merge all node sets if merge_key is defined.
        """
        for nodeset in self.nodesets:
            nodeset.merge(nodeset.merge_keys)

    def create_relationshipsets(self):
        for relationshipset in self.relationshipsets:
            relationshipset.create()

    def create_nodeset(self):
        for relationshipset in self.relationshipsets:
            relationshipset.create()

    def add_node(self, labels: list[str], properties: dict, merge_keys: list[str] = None):
        ns = self.get_nodeset(labels, merge_keys)
        if ns is None:
            ns = NodeSet(labels, merge_keys)
            self.add(ns)
        ns.add_node(properties)

    def add_relationship(
        self,
        rel_type: str,
        properties: dict,
        start_node_labels: list(str) = None,
        end_node_labels: list(str) = None,
        start_node_properties: list(str) = None,
        end_node_properties: list(str) = None,
    ):
        rs = self.get_relationshipset(rel_type)
        if rs is None:
            if None not in (
                start_node_labels,
                end_node_labels,
                start_node_properties,
                end_node_properties,
            ):
                rs = RelationshipSet(
                    rel_type=rel_type,
                    start_node_labels=start_node_labels,
                    end_node_labels=end_node_labels,
                    start_node_properties=start_node_properties,
                    end_node_properties=end_node_properties,
                )
                self.add(rs)
            else:
                ValueError(
                    "Could not create Relationshipset. Missing parameters {}".format(
                        [
                            list(param.keys())[0]
                            for param in [
                                {"start_node_labels": start_node_labels},
                                {"end_node_labels": end_node_labels},
                                {"start_node_properties": start_node_properties},
                                {"end_node_properties": end_node_properties},
                            ]
                            if param[list(param.keys())[0]] is None
                        ]
                    )
                )
        rs.add_relationship(properties)


def get_instances_from_list(list, klass):
    """
    From a list of objects, get all objects that are instance of klass.

    :param list: List of objects.
    :param klass: The reference class.
    :return: Filtered list if objects.
    """
    output = []
    for o in list:
        if isinstance(o, klass):
            output.append(o)
    return output

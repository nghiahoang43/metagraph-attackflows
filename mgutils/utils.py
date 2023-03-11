from library import *
from nodes import *
def convertAllToNodes(objects):
    not_property_types = ["extension-definition", "identity", "attack-flow"]
    # hashmap[id] = node
    nodeById = {}
    # list for each type of node
    actions = []
    assets = []
    conditions = []
    operators = []
    relationships = []
    others = []
    for i in range(len(objects)):
        node = objects[i]
        if node["type"] == "attack-action":
            id = node["id"]
            name = node["name"]
            tactic_id = node["tactic_id"] if "tactic_id" in node else ""
            tactic_ref = node["tactic_ref"] if "tactic_ref" in node else ""
            technique_id = node["technique_id"] if "technique_id" in node else ""
            technique_ref = node["technique_ref"] if "technique_ref" in node else ""
            description = node["description"] if "description" in node else ""
            command_ref = node["command_ref"] if "command_ref" in node else ""
            asset_refs = node["asset_refs"] if "asset_refs" in node else []
            effect_refs = node["effect_refs"] if "effect_refs" in node else []
            newNode = AttackAction(id, name, tactic_id, tactic_ref, technique_id, technique_ref, description, command_ref, asset_refs, effect_refs)
            if newNode in actions:
                index = actions.index(newNode)
                prevNode = actions[index]
                prevNode.union(newNode)
            else:
                actions.append(newNode)
        elif node["type"] == "attack-asset":
            id = node["id"]
            name = node["name"]
            description = node["description"] if "description" in node else ""
            object_ref = node["object_ref"] if "object_ref" in node else "[]"
            newNode = AttackAsset(id, name, description, object_ref)
            assets.append(newNode)
        elif node["type"] == "attack-condition":
            id = node["id"]
            description = node["description"] if "description" in node else ""
            true_refs = node["on_true_refs"] if "on_true_refs" in node else []
            false_refs = node["on_false_refs"] if "on_false_refs" in node else []
            newNode = AttackCondition(id, description, true_refs, false_refs)
            conditions.append(newNode)
        elif node["type"] == "attack-operator":
            id = node["id"]
            operator = node["operator"]
            effect_refs = node["effect_refs"] if "effect_refs" in node else []
            newNode = AttackOperator(id, operator, effect_refs)
            operators.append(newNode)
        elif node["type"] == "relationship":
            id = node["id"]
            source_ref = node["source_ref"]
            target_ref = node["target_ref"]
            newNode = Relationship(id, source_ref, target_ref)
            relationships.append(newNode)
        else:
            # Create STIX Common Properties
            if node["type"] not in not_property_types:
                id = node["id"]
                type = node["type"]
                name = node["name"] if "name" in node else ""
                newNode = Others(id, type, name)
                others.append(newNode)
            else:
                continue
        nodeById[node["id"]] = newNode
    allNodes = {}
    allNodes["actions"] = actions
    allNodes["assets"] = assets
    allNodes["conditions"] = conditions
    allNodes["operators"] = operators
    allNodes["relationships"] = relationships
    allNodes["others"] = others
    return nodeById, allNodes


# Function to get the outNode from (a) condition node/s
def getEndOfCondition(node, nodeById):
    outNodes = []
    if isinstance(node, AttackCondition):
        conditionNode = nodeById[node.getId()]
        true_refs = conditionNode.getTrueRefs()
        false_refs = conditionNode.getFalseRefs()
        for t_ref in true_refs:
            true_node = nodeById[t_ref]
            if isinstance(true_node, AttackCondition):
                outNodes.append(getEndOfCondition(true_node), nodeById)
            else:
                outNodes.append(true_node.id)
        for f_ref in false_refs:
            false_node = nodeById[f_ref]
            if isinstance(false_node, AttackCondition):
                outNodes.append(getEndOfCondition(false_node), nodeById)
            else:
                outNodes.append(false_node.id)
    return outNodes

def runMetagraph(generating_set, mg):
    generating_list = list(generating_set)
    source = set()
    target = set()
    for i in range(1,len(generating_list)+1):
        print(i, generating_list[i-1])
    source_idx = input("Choose your souce: ")
    source_idx = int(source_idx)
    source.add(generating_list[source_idx-1])
    is_more_source = input("Do you want to add more source?(y/n) ")
    while is_more_source != "n":
        if is_more_source != "y":
            print("Invalid input")
            is_more_source = input("Do you want to add more source?(y/n) ")
            continue
        source_idx = input("Choose your souce: ")
        source_idx = int(source_idx)
        source.add(generating_list[source_idx-1])
        is_more_source = input("Do you want to add more source?(y/n) ")

    target_idx = input("Choose your target: ")
    target_idx = int(target_idx)
    target.add(generating_list[target_idx-1])
    is_more_target = input("Do you want to add more target?(y/n) ")
    while is_more_target != "n":
        if is_more_target != "y":
            print("Invalid input")
            is_more_target = input("Do you want to add more target?(y/n) ")
            continue
        target_idx = input("Choose your target: ")
        target_idx = int(target_idx)
        target.add(generating_list[target_idx-1])
        is_more_target = input("Do you want to add more target?(y/n) ")
        
    metapaths = mg.get_all_metapaths_from(source,target)
    if metapaths:
        for metapath in metapaths:
            print(repr(metapath))
    else:
        print('There is no metapaths from {source} to {target}'.format(source=source, target=target))

def createAttackEdge(mg, generating_set, nodeById, flow_dict):
    for node in generating_set:
        if isinstance(node, AttackAction):
            refs = []
            refs = node.getAssetRefs()+node.getEffectRefs()
            # if node.technique_id == 'T1595.002':
            #     print(refs)
            while len(refs) > 0: 
                ref = refs.pop()
                if ref in nodeById:
                    outNode = nodeById[ref]
                    # print(node, outNode)
                    if isinstance(outNode, AttackCondition):
                        refs+=getEndOfCondition(outNode, nodeById)
                    elif isinstance(outNode, AttackOperator):
                        if node.id == "attack-operator--79cffc5f-d104-4780-8ba6-9c94462110ed":
                            print('dkjld')
                        operatorNode = nodeById[outNode.getId()]
                        if outNode.operator == "AND":
                            operatorNode.addInNode(node)
                        else:
                            operatorOutNodes = operatorNode.getOutNodes()
                            for operatorOutNode in operatorOutNodes:
                                refs.append(operatorOutNode.id)
                    elif isinstance(outNode, AttackAction):
                        mg.add_edges_from([Edge({node}, {outNode})])
                        flow_dict[node].append(outNode)
    return mg, flow_dict

def createOperatorEdge(mg, operators, flow_dict):
    for operator in operators:
        if operator.operator == "AND":
            inNodes = operator.getInNodes()
            outNodes = operator.getOutNodes()
            print(inNodes, outNodes)
            if len(inNodes) == 0:
                continue
            mg.add_edges_from([Edge(set(inNodes), set(outNodes))])
            for node in inNodes:
                flow_dict[node]+=outNodes
    return mg, flow_dict

def createRelationshipEdge(mg, relationships, nodeById, flow_dict):
    for relationship in relationships:
        source_node = nodeById[relationship.source_ref]
        target_node = nodeById[relationship.target_ref]
        if isinstance(source_node, AttackAction) and isinstance(target_node, AttackAction):
            mg.add_edges_from([Edge({source_node}, {target_node})])
            flow_dict[source_node].append(target_node)
    return mg, flow_dict
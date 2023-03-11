class AttackAction:
    def __init__(self, id, name, tactic_id="", tactic_ref="", technique_id="",technique_ref="", description="", command_ref="", asset_refs=[], effect_refs=[]):
        self.type = "attack-action"
        self.id = id
        self.name = name
        self.tactic_id = tactic_id
        self.tactic_ref = tactic_ref
        self.technique_id = technique_id
        self.technique_ref = technique_ref
        self.description = description
        self.command_ref = command_ref
        self.asset_refs = asset_refs
        self.effect_refs = effect_refs

    def getId(self):
        return self.id

    def getDescription(self):
        return self.description

    def getAssetRefs(self):
        return self.asset_refs

    def getEffectRefs(self):
        return self.effect_refs 
    
    def union(self, node):
        if not isinstance(node, AttackAction):
            return self
        self.asset_refs += node.asset_refs
        self.asset_refs = list(set(self.asset_refs))
        self.effect_refs += node.effect_refs
        self.effect_refs = list(set(self.effect_refs))
        return self
            
    def __repr__(self):
        if self.technique_id:
            return self.technique_id
        elif self.tactic_id:
            return self.tactic_id
        return self.name

    def __eq__(self, other):
        if other.type != "attack-action":
            return False
        if (self.technique_id and other.technique_id):
            return self.technique_id == other.technique_id
        elif (self.tactic_id and other.tactic_id):
            return self.tactic_id == other.tactic_id
        elif (self.name and other.name):
            return self.name == other.name
        return False

    def __lt__(self, other):
        if other.type != "attack-action":
            return False
        return self.name < other.name

    def __hash__(self):
        if self.technique_id:
            return hash(self.technique_id)
        elif self.tactic_id:
            return hash(self.tactic_id)
        return hash(self.name)

class AttackAsset:
    def __init__(self, id, name, description="", object_ref=""):
        self.type = "attack-asset"
        self.id = id
        self.name = name
        self.description = description
        self.object_ref = object_ref
    
    def getId(self):
        return self.id

    def getObjectRefs(self):
        return self.object_ref
    
    def __repr__(self):
        return self.name

class AttackCondition:
    def __init__(self, id, description="", on_true_refs=[], on_false_refs=[]):
        self.type = "attack-condition"
        self.id = id
        self.description = description
        self.on_true_refs = on_true_refs
        self.on_false_refs = on_false_refs
    
    def getId(self):
        return self.id

    def getTrueRefs(self):
        return self.on_true_refs

    def getFalseRefs(self):
        return self.on_false_refs


class AttackOperator:
    def __init__(self, id, operator, effect_refs=[]):
        self.type = "attack-operator"
        self.id = id
        self.operator = operator
        self.effect_refs = effect_refs
        self.inNodes = []
        self.outNodes = []
    
    def getId(self):
        return self.id
    
    def addInNode(self, node):
        self.inNodes.append(node)

    def getInNodes(self):
        return self.inNodes

    def setOutNodes(self, nodeArr):
        self.outNodes = nodeArr
    
    def getOutNodes(self):
        return self.outNodes

    def __hash__(self):
        return hash(str(self))

class Others:
    def __init__(self, type, id, name):
        self.type = type
        self.id = id
        self.name = name

    def getId(self):
        return self.id

    def __repr__(self):
        if len(self.name) > 0:
            return self.name
        else:
            return self.type
    
class Relationship:
    def __init__(self, relationship_type, source_ref, target_ref):
        self.relationship_type = relationship_type
        self.source_ref = source_ref
        self.target_ref = target_ref
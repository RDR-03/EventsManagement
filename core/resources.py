class resource:
    def __init__(
        self,
        name,
        total_cuantity=1,
        available=0,
        in_use=0,
        dependencies=None,
        conflicts=None,
    ):
        self.name = name
        self.total_cuantity = total_cuantity
        self.available = available
        self.in_use = in_use

        if dependencies is None:
            self.dependencies = {}
        else:
            self.dependencies = dependencies

        if conflicts == None:
            self.conflicts = []
        else:
            self.conflicts = conflicts

    def increase_amount(self, amount):
        self.total_cuantity += amount
        return True

    def decrease_amount(self, amount):
        if amount > self.total_cuantity:
            return False
        else:
            self.total_cuantity -= amount
            return True

    def dependant_on(self, other_resource, amount=1):
        if other_resource in self.dependencies:
            return f"Ya está establecida una relación entre {self.name} y {other_resource.name}"

        self.dependencies[other_resource] = amount

    @classmethod
    def establish_conflict(cls, r1, r2):
        r1.conflicts.append(r2)
        r2.conflicts.append(r1)

    def set_available(self):
        self.available = self.total_cuantity - self.in_use

    def __str__(self):
        return f"{self.name}, Cantidad ({self.total_cuantity})"

    # Estos son los metodos encargados de la persistencia de datos de la clase con Json
    def to_dict(self):
        return {"name": self.name, "total_cuantity": self.total_cuantity}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["total_cuantity"], 0, 0)  # Available  # In_use

    ####################################################################################


def make_inventory(r1: resource, *ri: resource):
    inventory = {}
    inventory[r1.name] = r1
    for r in ri:
        inventory[r.name] = r

    return inventory

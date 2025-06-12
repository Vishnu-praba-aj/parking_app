class DynamicUser:
    def __init__(self, field_name, value):
        setattr(self, field_name, value)  # Dynamic field creation

    def __setattr__(self, name, value):
        if name == "age" and value < 0:
            raise ValueError("Age must be positive")
        super().__setattr__(name, value)
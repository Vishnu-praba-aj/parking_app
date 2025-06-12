# --- Python Section ---

class User:
    name: str
    age: int = 0
    email = ""
    _password = None

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        if not email or "@" not in email:
            raise ValueError("Invalid email")
        if age < 0:
            raise ValueError("Age must be positive")

    def set_password(self, pwd):
        """Set password with minimum length validation."""
        if len(pwd) < 8:
            raise ValueError("Password too short")
        self._password = pwd

    def validate(self):
        """Custom validation method."""
        if not self.name:
            raise ValueError("Name required")

class Admin(User):
    access_level: int = 1

    def __init__(self, name, age, email, access_level):
        super().__init__(name, age, email)
        self.access_level = access_level
        if access_level < 1 or access_level > 10:
            raise ValueError("Access level must be 1-10")

# --- Java Section (as a string for LLM test) ---

java_code = """
public class Car {
    private String licensePlate;
    private int year;
    private boolean isElectric = false;

    public Car(String licensePlate, int year) {
        this.licensePlate = licensePlate;
        this.year = year;
        if (year < 1886) {
            throw new IllegalArgumentException("Year must be >= 1886");
        }
    }

    public void setLicensePlate(String lp) {
        if (lp == null || lp.length() < 5) {
            throw new IllegalArgumentException("Invalid license plate");
        }
        this.licensePlate = lp;
    }
}
"""

# --- JavaScript Section (as a string for LLM test) ---

js_code = """
class Product {
    constructor(name, price) {
        this.name = name;
        this.price = price;
        if (price < 0) throw new Error("Price must be non-negative");
    }

    setName(name) {
        if (!name) throw new Error("Name required");
        this.name = name;
    }
}

class Inventory {
    constructor() {
        this.items = [];
    }
    addItem(item) {
        if (!item || !item.name) throw new Error("Invalid item");
        this.items.push(item);
    }
}
"""


import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

public class AdvancedValidationCar {

    @NotNull
    private String vin;

    @NotBlank
    private String ownerName;

    @Pattern(regexp = "[A-Z]{2}[0-9]{2} [A-Z]{3}")
    private String licensePlate;

    @Min(1886)
    @Max(2100)
    private int year;

    public AdvancedValidationCar(String vin, String ownerName, String licensePlate, int year) {
        this.vin = vin;
        this.ownerName = ownerName;
        this.licensePlate = licensePlate;
        this.year = year;
    }

    // Getters and setters omitted for brevity
}
 class DynamicCar {
    public void setField(String name, Object value) {
        // Simulate dynamic field creation (reflection in real code)
        // Not statically analyzable
    }
}

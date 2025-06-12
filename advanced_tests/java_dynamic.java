import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Size;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Negative;
import jakarta.validation.constraints.NegativeOrZero;
import jakarta.validation.constraints.Past;
import jakarta.validation.constraints.PastOrPresent;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.AssertFalse;

import java.math.BigDecimal;
import java.time.LocalDate;

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

    @Size(min = 2, max = 30)
    private String modelName;

    @Email
    private String contactEmail;

    @Positive
    private int numberOfDoors;

    @PositiveOrZero
    private int numberOfPreviousOwners;

    @Negative
    private int negativeTestValue;

    @NegativeOrZero
    private int negativeOrZeroTestValue;

    @Past
    private LocalDate registrationDate;

    @PastOrPresent
    private LocalDate lastServiceDate;

    @Future
    private LocalDate insuranceExpiryDate;

    @FutureOrPresent
    private LocalDate warrantyExpiryDate;

    @DecimalMin("0.0")
    @DecimalMax("1000000.0")
    private BigDecimal price;

    @Digits(integer = 5, fraction = 2)
    private BigDecimal engineCapacity;

    @AssertTrue
    private boolean isInsured;

    @AssertFalse
    private boolean isStolen;

    // Getters and setters omitted for brevity
}

class DynamicCar {
    public void setField(String name, Object value) {
        // Simulate dynamic field creation (reflection in real code)
        // Not statically analyzable
    }
}

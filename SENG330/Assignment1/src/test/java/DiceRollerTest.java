import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("DiceRoller Test Class")
public class DiceRollerTest {
  private static DiceRoller roller;

  @BeforeAll
  static void setUp() {
    roller = new DiceRoller();
  }

  @Test
  void testRollD20() {
    int roll = roller.rollDie(DiceTypes.D20);
    assertTrue(roll >= 1 && roll <= 20);
  }

  @Test
  void testRollD8() {
    int roll = roller.rollDie(DiceTypes.D8);
    assertTrue(roll >= 1 && roll <= 8);
  }
}

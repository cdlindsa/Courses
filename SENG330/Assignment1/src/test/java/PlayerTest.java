import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Player Test Class")
public class PlayerTest {
  private static Player player1;
  private static Player player2;

  @BeforeAll
  static void setUp() {
    player1 = new Player(4, 20, 6, "Aragorn");
    player2 = new Player(24, 40, 10, "Gandalf");
  }

  @Test
  void testGetInitiative() {
    player1.getInitiative();
    assertTrue(player1.getInitiativeScore() <= 24 && player1.getInitiativeScore() >= 5);
  }

  @Test
  void testAttack() {
    int damage = player1.attack();
    assertTrue(damage <= 14 && damage >= 7);
  }

  @Test
  void testTakeDamage() {
    player1.stopDefending();
    int damage = 5;
    int oldHP = player1.getHitPoints();
    int newHP = oldHP - damage;
    player1.takeDamage(damage);
    assertEquals(newHP, player1.getHitPoints());
  }

  @Test
  void testDefend() {
    player1.defend();
    assertTrue(player1.isDefending());
  }

}

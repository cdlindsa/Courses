import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Monster Test Class")
public class MonsterTest {
  private static Player monster1;
  private static Player monster2;

  @BeforeAll
  static void setUp() {
    monster1 = new Player(4, 20, 6, "Beholder");
    monster2 = new Player(24, 40, 10, "Tiamat");
  }

  @Test
  void testGetInitiative() {
    monster1.getInitiative();
    assertTrue(monster1.getInitiativeScore() <= 24 && monster1.getInitiativeScore() >= 5);
  }

  @Test
  void testAttack() {
    int damage = monster1.attack();
    assertTrue(damage <= 14 && damage >= 7);
  }

  @Test
  void testTakeDamage() {
    monster1.stopDefending();
    int damage = 5;
    int oldHP = monster1.getHitPoints();
    int newHP = oldHP - damage;
    monster1.takeDamage(damage);
    assertEquals(newHP, monster1.getHitPoints());
  }

  @Test
  void testDefend() {
    monster1.defend();
    assertTrue(monster1.isDefending());
  }

}

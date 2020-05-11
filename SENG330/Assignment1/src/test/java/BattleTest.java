import java.util.ArrayList;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Battle Test Class")
public class BattleTest {
  private static Battle battle;
  private static ArrayList<Player> players;
  private static ArrayList<Monster> monsters;

  @BeforeAll
  static void setUp() {
    players = new ArrayList<>();
    monsters = new ArrayList<>();
    players.add(new Player(4, 20, 4, "Aragorn"));
    monsters.add(new Monster(4, 15, 4, "Uruk-Hai"));
    players.add(new Player(4, 20, 4, "Legolas"));
    monsters.add(new Monster(4, 15, 4, "Uruk-Ho"));
    players.add(new Player(4, 20, 4, "Gimli"));
    monsters.add(new Monster(4, 15, 4, "Uruk-Hey"));
    players.add(new Player(4, 20, 4, "Gandalf"));
    monsters.add(new Monster(4, 15, 4, "Uruk-yo"));
    battle = new Battle(players, monsters);
  }

  @Test
  void testConductBattle() {
    assertFalse(battle.isBattleOver());
    battle.conductBattle();
    assertTrue(players.size() == 0 || monsters.size() ==0);
    assertTrue(battle.isBattleOver());
  }
}

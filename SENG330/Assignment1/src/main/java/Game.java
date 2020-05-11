import java.util.ArrayList;

public class Game {

  /**
   * The game's main class that serves as the application entry point.
   * @param args No arguments need to be passed.
   */
  public static void main(String[] args) {
    System.out.println("Welcome to this battle system prototype!");

    ArrayList<Player> heroes = new ArrayList<>();
    heroes.add(new Player(3, 20, 5, "Aragorn"));
    heroes.add(new Player(5, 15, 6, "Legolas"));
    heroes.add(new Player(2, 25, 4, "Gimli"));
    heroes.add(new Player(2, 10, 5, "Gandalf"));

    ArrayList<Monster> monsters = new ArrayList<>();
    monsters.add(new Monster(4, 15, 3, "Orc 1"));
    monsters.add(new Monster(4, 15, 3, "Orc 2"));
    monsters.add(new Monster(4, 15, 3, "Orc 3"));
    monsters.add(new Monster(4, 15, 3, "Orc 4"));
    monsters.add(new Monster(4, 15, 3, "Orc 5"));

    Battle battle = new Battle(heroes, monsters);
    battle.conductBattle();
  }
}

import java.util.Random;

public class DiceRoller {

  /**
   * This method generates a random number between the die maximum and 1.
   * @param die A DiceTypes object representing the type of die to be rolled.
   * @return An integer between 1 and the max value of the selected die type.
   */
  public int rollDie(DiceTypes die) {
    Random rand = new Random();
    return rand.nextInt(die.getMax() - 1) + 1;
  }
}

import java.util.ArrayList;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.Comparator;

public class Battle {
  private ArrayList<Player> heroes;
  private ArrayList<Monster> monsters;
  private ArrayList<Character> battleQueue;
  private boolean battleOver;
  private int roundCounter;
  private int monsterPartySize;
  private int playerPartySize;
  private Character attackedCharacter;
  private String output;

  /**
   * Initializes a battle instance between heroes and monsters.
   * @param heroes An ArrayList of player characters.
   * @param monsters An ArrayList of monster characters.
   */
  public Battle(ArrayList<Player> heroes, ArrayList<Monster> monsters) {
    this.heroes = heroes;
    this.monsters = monsters;
    this.battleQueue = new ArrayList<>();
    this.battleOver = false;
    this.roundCounter = 0;
    this.monsterPartySize =0;
    this.playerPartySize =0;
    this.output = "";
  }

  public boolean isBattleOver() {
    return this.battleOver;
  }

  /**
   * Runs a battle instance between two sets of characters.
   */
  public void conductBattle() {
    if (this.heroes.size()==0 && this.monsters.size() == 0){
      System.out.println("The battle cannot be conducted, there are no characters present!");
      this.battleOver = true;
    } else {
      characterInitialization();
    }
    while (!this.battleOver) {
    this.resolveRound();
    if (this.heroes.size() == 0) {
      System.out.println("The battle is over, and the monsters have won.");
      this.battleOver = true;
    } else if (this.monsters.size() == 0) {
      System.out.println("The battle is over, and the heroes have won.");
      this.battleOver = true;
    }
  }
  }

    /**
     * Initializes initiative score for each character, sorts list (descending) by initiative score.
     */
  private void characterInitialization(){
    this.heroes.removeAll(Collections.singletonList(null));
    for (Player character : heroes){
          character.getInitiative();
      }
    this.monsters.removeAll(Collections.singletonList(null));
    for (Monster character : monsters){
        character.getInitiative();
    }
    this.heroes.sort(Comparator.comparing(Character::getInitiativeScore).reversed());
    this.monsters.sort(Comparator.comparing(Character::getInitiativeScore).reversed());
  }

    /**
     * Establishes parties and sorts battleQueue by initiative score.
     */
  private void establishPartiesAndSort(){
    while (this.playerPartySize<5 && this.heroes.size()>this.playerPartySize){
      this.battleQueue.add(this.heroes.get(this.playerPartySize));
      this.playerPartySize++;
    }
    while (this.monsterPartySize<5 && this.monsters.size()>this.monsterPartySize){
      this.battleQueue.add(this.monsters.get(this.monsterPartySize));
      this.monsterPartySize++;
    }
    this.battleQueue.sort(Comparator.comparing(Character::getInitiativeScore).reversed());
  }

    /**
     * Helper function to remove character from respective lists
     * @param character to be removed
     */
  private void removeCharacter(Character character){
    if (character instanceof Monster){
      this.monsters.remove(character);
      this.monsterPartySize--;
    } else {
      this.heroes.remove(character);
      this.playerPartySize--;
    }
    this.battleQueue.remove(character);
  }

    /**
     * Picks attacked character by random.
     */
  private void findAttacked(Character attacker){
    this.attackedCharacter= getRandomCharacterFromList(this.battleQueue);
    if (attacker instanceof Monster){
      while (this.attackedCharacter instanceof Monster){
        this.attackedCharacter= getRandomCharacterFromList(this.battleQueue);
      }
    } else if (attacker instanceof Player){
      while (this.attackedCharacter instanceof Player){
        this.attackedCharacter= getRandomCharacterFromList(this.battleQueue);
      }
    }
  }
    /**
     * Note: I don't play DnD, so im treating initiative score like speed/dexterity.
     * Therefore, attacked Character defends if initiative score is 50% higher than attackers.
     * Modularized to allow for increased complexity.
     */
  private void determineDefending(int index){
      if (this.attackedCharacter.getInitiativeScore() >= this.battleQueue.get(index).getInitiativeScore()*1.5) {
          this.attackedCharacter.defend();
      }
  }

  /**
   * attack order determined by initiative score
   */
  private void resolveRound() {
    this.roundCounter++;
    establishPartiesAndSort();
    for(int i = 0; i< this.battleQueue.size(); i++){
      if (this.playerPartySize!=0 && this.monsterPartySize!=0) {
        findAttacked(this.battleQueue.get(i));
        determineDefending(i);
        this.attackedCharacter.takeDamage(this.battleQueue.get(i).attack());
        this.attackedCharacter.stopDefending();
        this.output = this.attackedCharacter.toString();
        System.out.println(output);
        if (this.attackedCharacter.getHitPoints() <= 0) {
          removeCharacter(this.attackedCharacter);
        }
      }
    }
    this.battleQueue.clear();
    this.monsterPartySize=0;
    this.playerPartySize=0;
  }

  /**
   * Helper function to select a random element from an ArrayList
   * @param characters The ArrayList to select an element from.
   * @return A random element from the given list.
   */
  private Character getRandomCharacterFromList(ArrayList characters) {
    Random rand = new Random();
    int randomIndex = rand.nextInt(characters.size());
    return (Character) characters.get(randomIndex);
  }
}

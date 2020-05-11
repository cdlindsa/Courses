public enum DiceTypes {
  D8(8),
  D20(20);

  private int dieMax;

  DiceTypes(int dieMax) {
    this.dieMax = dieMax;
  }

  public int getMax() {
    return this.dieMax;
  }
}

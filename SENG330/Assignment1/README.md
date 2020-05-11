Cameron Lindsay
SENG 330

# Assignment 1

### Overview
For this, and the remaining assignments: 
- code that does not compile will be given 0 marks (for that part of the assignment).
- since we auto-mark, following the template code and the naming conventions is vital to pass tests. 
- test early on the Travis server. This happens when you push your code to Github (origin). 
- Travis is limited in capacity; do not expect fast responses when the deadline is near. Wait times of 3-4 hours are possible.
- assignments are individual and **you must write your own code**. Plagiarism and copying from other students, from StackOverflow or other places, will be checked periodically. Students found to be in violation will be referred to the department committee and may receive a 0 on the assignment.

This assignment uses Gradle, a build tool. Gradle makes it easy to automate compile/test/build loops from the command line, and also has an Eclipse plugin. Gradle depends on a directory naming convention; do not move the src/test directories. 

To run your code from the command line, type `gradle build`. `gradle test` will execute the tests I've added to the code here. NB: **the full test suite is on Travis, and you should commit/push to Github to see these results**.
To run from IntelliJ, use the [Run Anything Window](https://www.jetbrains.com/help/idea/work-with-gradle-tasks.html) (likely top right).

There is no "functionality" here that is useful to a user; the test suite is the main/only way to see results. You can consider writing some print statements in Game.main().

### Tips
- Test-driven development writes test cases first, then makes the code pass those tests. First get your code to compile (syntax); then get the tests to pass (semantics).
- M1, M2, M3, and M4 notes will be important for this exercise.
- Don't change the tests we provide; you may wish to comment some out in order to do incremental work.
- Using (and fixing) Checkstyle prompts makes your code more readable. 

### Marking
- Marks are allocated for passing all tests (60%) and style/design (40%)
- We run tests on your code, but do not reveal all our tests. You should use Travis to ensure you pass our tests. 
- We may add tests until 2 days before the deadline. If you pass tests after that point, you can be confident you have achieved full test marks.

### Learning Objectives

This assignment covers the following topics discussed in M1-M4:
- Types and Classes
- Abstractions
- Encapsulation
- Scope
- Interfaces and Implementation
- Polymorphism
- Class Diagrams
- Comparators

Due: Jan 31, 2020 at midnight in Github.

---

## Assignment Case

As a new gaming developer at CoolGames Inc., you have been tasked with creating an adventure game based on a simplified variation of the popular mechanics of the fantasy role-playing game "_Dungeons and Dragons_".
While the story design team works on the setting, you are required to create the underlying mechanics that will bring the battle system to life.
A battle consists of several **characters** (**players** and **monsters**) taking turns based on **initiative** scores (which are adjustable based on initiative modifiers).
Each player and monster has their own initiative score.
A player and a monster can perform 2 basic actions; an **attack** action, and a **defend** action.
Attack actions cause damage, whereas a defend action reduces the amount of damage taken from an attack by half.

### Part 1 [/10]

Using JetUML (or similar design tools), create a class diagram of the various entities within the game and their properties.
You can add properties you feel are important (e.g., character name, ...etc.)
Feel free to use interfaces where necessary.
Only submit a ***.png** image embedded in the markdown file `class_diagram.md` in the documents directory of this repo.

### Part 2 [/10]

Using the skeleton code provided:
1. Implement a method for each type of character which generates their initiative score based on a die roll (random number between 1 and 20).
This number should be added to their initiative modifier and stored within their initiative score property.
2. Implement the `Comparable` interface for a character using character initiative scores.
Characters with a larger initiative score should rank higher than characters with lower initiative scores.
3. Override the `Object.toString()` method for the characters to print out the following:
```
System.out.println(aragorn): "Aragorn has 4 HP left."
```

### Part 3 [/10]

Using the skeleton code provided:
1. Implement a **battle** queue that contains characters sorted by their initiative scores (highest goes first).
"_Running_" the battle involves going through the queue in order of initiative scores, and attacking different characters (monsters attack players, and players attack monsters).
You can assume that target selection is random.
At the end of each round (iteration), each character should print out their current hit points.
2. Add a status property to each character that reflects their situation. Possible states are either "Alive" or "Unconscious".
Modify your battle queue so that characters always attack "_Alive_" characters.
A character becomes unconscious if their hit points drop to 0 or less.
3. Update the `Object.toString()` method for the characters to print out the following:
```
System.out.println(aragorn): "Aragorn has 0 HP left. Aragorn is unconscious."
``` 

### Tips

- D&D is a dice-based game. To generate a base initiative value, you will require some way to roll a 20-sided die. The outcome of the roll gets added to a character's initiative modifier. This, in turn, determines their overall initiative score for a particular battle.
- Attacking is similar. To generate a base damage value, you will require an 8-sided die. The outcome of the roll gets added to a character's attack modifier. This, in turn, determines the overall damage a character deals per round.
- D&D combat takes place over six second time increments referred to as rounds. A battle can consist of multiple rounds. You do not need to keep time. The round construct might help with implementing the battle queue.
- Some basic classes and methods have been provided to you, to help with your implementation. However, do not change the method names or signatures, as those are used in the tests. 

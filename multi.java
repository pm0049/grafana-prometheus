import java.util.*;

public class Multiple {
  public static void main(String[] args) {
    String inputSource = "MOV R\nRAHUL 30, 40, 50\nDCR R\nAND R\nRAHUL 33, 44, 55\nMUL 88\nHALT";
    String macroDefinition = "MACRO\nRAHUL &ARG1, &ARG2, &ARG3\nADD &ARG1\nSUB &ARG2\nOR &ARG3\nMEND";

    // Parse input source code and macro definition
    List<String> sourceCodeInstructions = Arrays.asList(inputSource.split("\n"));
    List<String> macroInstructions = Arrays.asList(macroDefinition.split("\n"));

    // Extract macro name and arguments from macro definition
    String macroName = macroInstructions.get(1).substring(0, macroInstructions.get(1).indexOf(" "));
    List<String> macroArguments = Arrays
        .asList(macroInstructions.get(1).substring(macroInstructions.get(1).indexOf(" ") + 1).split(", "));

    // Perform macro expansion
    List<String> expandedSourceCode = new ArrayList<>();
    int macroCalls = 0;
    int macroInstructionsCount = 0;
    List<List<String>> actualArguments = new ArrayList<>();

    for (String instruction : sourceCodeInstructions) {
      if (instruction.startsWith(macroName)) {
        // Macro call found
        macroCalls++;
        List<String> arguments = Arrays.asList(instruction.substring(instruction.indexOf(" ") + 1).split(", "));
        actualArguments.add(arguments);

        // Expand macro
        for (int i = 2; i < macroInstructions.size() - 1; i++) {
          String macroInstruction = macroInstructions.get(i);
          for (int j = 0; j < macroArguments.size(); j++) {
            macroInstruction = macroInstruction.replace("&" + macroArguments.get(j), arguments.get(j));
          }
          expandedSourceCode.add(macroInstruction);
          macroInstructionsCount++;
        }
      } else { // Non-macro instruction, add as it is
        expandedSourceCode.add(instruction);
      }
    }

    // Calculate statistics
    int totalInstructions = sourceCodeInstructions.size() - macroCalls + macroInstructionsCount;

    // Output expanded source code
    System.out.println("Output source code after Macro expansion:");
    for (String instruction : expandedSourceCode) {
      System.out.println(instruction);
    }

    // Output statistics
    System.out.println("\nStatistical output:");
    System.out.println("Number of instructions in input source code (excluding Macro calls) = " +
        (sourceCodeInstructions.size() - macroCalls));
    System.out.println("Number of Macro calls = " + macroCalls);
    System.out.println("Number of instructions defined in the Macro call = " + macroInstructionsCount);
    for (int i = 0; i < macroCalls; i++) {
      System.out.println("Actual argument during Macro call \"" + macroName + "\" = " +
          actualArguments.get(i));
    }
    System.out.println("Total number of instructions in the expanded source code = " +
        totalInstructions);
  }
}

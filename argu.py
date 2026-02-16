def expand_macro(source_code, macro_definition):
    macro_lines = macro_definition.strip().split('\n')[1:-1]
    macro_name, macro_body = macro_lines[0].split()[1], macro_lines[1:]
    expanded_code = []
    for line in source_code:
        if macro_name in line:
            arg = line.split()[1]  # Extracting the argument from the macro call
            for macro_instruction in macro_body:
                expanded_code.append(macro_instruction.replace('&ARG', arg))
        else:
            expanded_code.append(line)
    return expanded_code


def calculate_statistics(source_code, macro_calls):
    num_instructions = sum(1 for line in source_code if line.strip() and 'MACRO' not in line and 'MEND' not in line)
    num_macro_calls = len(macro_calls)
    num_instructions_in_macro = sum(1 for call in macro_calls for line in call[1:-1])
    actual_arguments = [call.split()[1] for call in macro_calls]
    expanded_source_code = expand_macro(source_code, macro_definition)
    total_instructions_expanded = sum(1 for line in expanded_source_code if line.strip())
    return (num_instructions, num_macro_calls, num_instructions_in_macro, actual_arguments, total_instructions_expanded)


if __name__ == "__main__":
    # Input Source Code with Macro Calls
    source_code = [
        "MOV R",
        "RAHUL 30",
        "DCR R",
        "AND R",
        "RAHUL 55",
        "MUL 88",
        "HALT"
    ]

    # Macro Definition
    macro_definition = """
    MACRO
    RAHUL &ARG
    ADD &ARG
    SUB &ARG
    OR &ARG
    MEND
    """

    # Find Macro Calls
    macro_calls = [line for line in source_code if 'RAHUL' in line]

    # Expand Macro Calls
    expanded_code = expand_macro(source_code, macro_definition)

    # Calculate Statistics
    stats = calculate_statistics(source_code, macro_calls)

    # Output Expanded Source Code
    print("Expanded Source Code:")
    for line in expanded_code:
        print(line)

    # Output Statistics
    print("\nStatistics:")
    print("Number of instructions in input source code (excluding Macro calls):", stats[0])
    print("Number of Macro calls:", stats[1])
    print("Number of instructions defined in the Macro call:", stats[2])
    print("Actual argument during each Macro call:", stats[3])
    print("Total number of instructions in the expanded source code:", stats[4])

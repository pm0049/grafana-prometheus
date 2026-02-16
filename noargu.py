def expand_macro(input_source, macro_definition):
    # Split input source code into lines
    lines = input_source.split('\n')

    # Find Macro calls and replace them with macro definition
    expanded_source = []
    macro_calls = 0
    macro_instructions = 3
    for line in lines:
        if "RAHUL" in line:
            macro_calls += 1
            # macro_instructions += 3 # Assuming each call expands to 3 instructions

            # Add macro definition to the expanded source
            macro_definition_lines = macro_definition.split('\n')
            expanded_source.extend(macro_definition_lines[1:-1])  # Exclude MACRO and MEND lines
        else:
            # Add non-macro lines to the expanded source
            expanded_source.append(line)

    # Calculate statistics
    input_instructions = sum(1 for line in lines if "RAHUL" not in line)
    total_instructions = input_instructions + macro_calls * macro_instructions

    # Join expanded source code into a string
    expanded_source_code = '\n'.join(expanded_source)

    return expanded_source_code, input_instructions, macro_calls, macro_instructions, total_instructions


# Input Source code with Macro calls
input_source_code = """MOV R
RAHUL
DCR R
AND R
RAHUL
MUL 88
HALT"""

# Macro definition
macro_definition = """
MACRO
RAHUL
 ADD 30
 SUB 25
 OR R
MEND"""

# Expand the macro
expanded_source, input_instructions, macro_calls, macro_instructions, total_instructions = expand_macro(input_source_code, macro_definition)

# Output the expanded source code
print("Output source code after Macro expansion:")
print(expanded_source)

# Output statistics
print("\nStatistical output:")
print(f"Number of instructions in input source code (excluding Macro calls) = {input_instructions}")
print(f"Number of Macro calls = {macro_calls}")
print(f"Number of instructions defined in the Macro call = {macro_instructions}")
print(f"Total number of instructions in the expanded source code = {total_instructions}")

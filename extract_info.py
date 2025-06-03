from ghidra.program.model.listing import Function
from ghidra.util.task import TaskMonitor

listing = currentProgram.getListing()

print("=== FUNCTIONS ===")
functions = listing.getFunctions(True)
for function in functions:
    print("Function: {} at {}".format(function.getName(), function.getEntryPoint()))

print("\n=== DISASSEMBLY (30 INSTRUCTIONS FROM ENTRY) ===")
instructions = listing.getInstructions(currentProgram.getMinAddress(), True)
i = 0
while instructions.hasNext() and i < 30:
    instr = instructions.next()
    print("{}: {}".format(instr.getAddress(), instr))
    i += 1

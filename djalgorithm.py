# Deutsch-Jozsa Algorithm practice qiskit practice
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_oracle(case, n):
    """
    Returns a quantum circuit implementing a Constant or Balanced oracle.
    n is number of qubits
    """
    # n input qubits, 1 output qubit
    oracle_qc = QuantumCircuit(n + 1)
    if case == "balanced":
        # A balanced oracle returns 0 for half of inputs and 1 for the other half.
        # We achieve this by using CNOTs with target (n) controlled by input qubits.
        # To vary the function, we wrap some controls in X gates based on a random bitstring.
        b_str = format(np.random.randint(1, 2 ** n), f'0{n}b')
        print(f"Balanced Oracle Secret String: {b_str}")
        # Place X gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        # Apply CNOTs (the core of the balanced function)
        for qubit in range(n):
            oracle_qc.cx(qubit, n)

        # Place X gates again to uncompute
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
    elif case == "constant":
        # A constant oracle always returns 0 or always returns 1.
        # Randomly decide if it's constant-0 or constant-1
        output = np.random.randint(2)
        print(f"Constant Oracle Output: {output}")
        if output == 1:
            oracle_qc.x(n)
    # Convert to a gate to make the circuit diagram cleaner
    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate

def dj_algorithm(oracle_gate, n):
    """
    Constructs the Deutsch-Jozsa circuit.
    """
    dj_circuit = QuantumCircuit(n + 1, n)
    # 1. Initialize output qubit to |-> state (Phase Kickback setup)
    dj_circuit.x(n)
    dj_circuit.h(n)
    # 2. Apply H-gates to input register
    for qubit in range(n):
        dj_circuit.h(qubit)
    dj_circuit.barrier()
    # 3. Apply the Oracle
    dj_circuit.append(oracle_gate, range(n + 1))
    dj_circuit.barrier()
    # 4. Apply H-gates to input register again (Interference)
    for qubit in range(n):
        dj_circuit.h(qubit)
    # 5. Measure the input register
    for i in range(n):
        dj_circuit.measure(i, i)
    return dj_circuit
n = 9 # number of qubits in simulation
oracle_type = 'constant'  # can change to constant
# Build Circuit
oracle = dj_oracle(oracle_type, n)
dj_circuit = dj_algorithm(oracle, n)
# Visualize
print("Circuit Diagram:")
print(dj_circuit.draw(output='text'))
# Run Simulation
simulator = AerSimulator()
transpiled_dj = transpile(dj_circuit, simulator)
result = simulator.run(transpiled_dj, shots=1024).result()
counts = result.get_counts()
print(f"\nResults for {oracle_type} oracle: {counts}")
# '000' means Constant.
#  Anything else Balanced
if '0' * n in counts:
    print("Prediction: Function is CONSTANT.")
else:
    print("Prediction: Function is BALANCED.")

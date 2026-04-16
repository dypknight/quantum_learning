"""
如两个量子比特，对11 做cz门，如果控制比特是 |1⟩：目标比特的相位翻转（即状态 |1⟩ 变为 -|1⟩，而 |0⟩ 保持不变）
若目标不是|11>,比如目标是|01>，先对q0做x门，转1，在做cz（q0，q1），再x（q0）（即撤销对q0的处理）

扩散算子放大目标态（对振幅取平均得到a平均、ax=2a平均-ax）、ax是振幅（带相位）
扩散算子 D=2∣s⟩⟨s∣−I

对n个qubit
D=H⊗nX⊗nCZn​X⊗nH⊗n
CZn表示“仅当所有 qubit 都是 1 时翻相位”的多控 Z。
R≈​根号下（N/M）*​π/4 
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile

# =========================
# 1. Oracle：只给目标态 |01> 加负号
# =========================
def oracle_01():
    qc = QuantumCircuit(2)

    # 目标是 |01>
    # 先把 |01> 变成 |11>
    # 第0位是0，所以对第0个qubit加X
    qc.x(0)

    # 对 |11> 加负号
    qc.cz(0, 1)

    # 还原
    qc.x(0)

    return qc





# 操作均匀态 = 操作 |00⟩（再用 H 来回映射）
# 扩散算子 D=2∣s⟩⟨s∣−I：H → X → CZ → X → H

# =========================
# 2. Diffusion（扩散算子）
# =========================
def diffusion_2qubit():
    qc = QuantumCircuit(2)

    # H^⊗2
    qc.h([0, 1])

    # X^⊗2
    qc.x([0, 1])

    # 对 |11> 加负号
    qc.cz(0, 1)

    # X^⊗2
    qc.x([0, 1])

    # H^⊗2
    qc.h([0, 1])

    return qc


# =========================
# 3. 主程序：Grover
# =========================
qc = QuantumCircuit(2, 2)

# Step 1: 初始化均匀叠加
qc.h([0, 1])

# Step 2: Oracle
qc.compose(oracle_01(), inplace=True)

# Step 3: Diffusion
qc.compose(diffusion_2qubit(), inplace=True)

# Step 4: 测量
qc.measure([0, 1], [0, 1])

print("Grover Circuit:")
print(qc.draw())

# =========================
# 4. 运行模拟
# =========================
simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1024).result()
counts = result.get_counts()

print("Measurement counts:")
print(counts)
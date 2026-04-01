from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def deutsch_jozsa(n):
    # 创建量子电路：n+1 个量子比特用于计算，n 个经典比特用于测量；最后一个量子比特（索引 n）是辅助比特
    qc = QuantumCircuit(n + 1, n)   
    breakpoint()

    qc.x(n)
    qc.h(range(n + 1))

    # 简单 balanced oracle
    for i in range(n):
        qc.cx(i, n)

    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc

qc = deutsch_jozsa(3)


sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
print(result.get_counts())

from scipy.integrate import quad
import numpy as np

def f(t):
    return 500 * np.exp(-0.3 * t)

I_analytical = 1666.67 * (1 - np.exp(-0.3 * 7))

I_numerical, _ = quad(f, 0, 7)

print(f"Аналитичний інтеграл: {I_analytical:.2f}")
print(f"Чисельний інтеграл: {I_numerical:.2f}")

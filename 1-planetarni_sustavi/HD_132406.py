import numpy as np
import matplotlib.pyplot as plt
import universe

au = 1.496 * 10**(11)
day = 24*60*60
m_sun = 1.989 * 10**(30)
m_jupiter = 1.898 * 10**(27)

m_1 = m_sun * 1.09
m_2 = m_jupiter * 6.7
semi_major_axis = au * 1.98
T = day * 974
e = 0.34

a = semi_major_axis
b = np.sqrt((1-e*e)*a*a)
print(b)
f = np.sqrt(a*a-b*b)
print(f)

p1 = universe.Planet(m_1, "HD 132406")
p2 = universe.Planet(m_2, "HD 132406 b")

planeti = [p1, p2]
svemir = universe.Universe(planeti)

v0_1 = p2.generate_initial_velocity_1(semi_major_axis, T)
v0_2 = p2.generate_initial_velocity_2(semi_major_axis, a+f, m_1)

p1.set_initial_conditions([0,0], [0, -(m_2/m_1)*v0_1])
p2.set_initial_conditions([semi_major_axis, 0], [0, v0_1])

numericki_period_1 = svemir.animate_plot(100000, 5*T, 1)

if type(numericki_period_1)==str:
    print(f"Numericki period 1 : {numericki_period_1}")
else:
    print(f"Numericki period 1 : {numericki_period_1} s")

p1.reset()
p2.reset()

p1.set_initial_conditions([0,0], [0, -(m_2/m_1)*v0_2])
p2.set_initial_conditions([semi_major_axis + f, 0], [0, v0_2])

numericki_period_2 = svemir.animate_plot(100000, 5*T, 1)

if type(numericki_period_2)==str:
    print(f"Numericki period 2 : {numericki_period_2}")
else:
    print(f"Numericki period 2 : {numericki_period_2} s")
# Heat Transfer - Exercise 5

A PySide6 app that simulates heat conduction between two bodies.

## How to run

```
uv run python Main.py
```

## How to use

1. Set the starting temperature of each body with its slider (0-200 °C). The color goes from black (0 °C) to red (200 °C).
2. Set the mass and heat capacity of each body. For the bar between them, pick a **Material** (the conductivity is set from the table below), or type the conductivity yourself. Typing a value switches the material to **Custom**.
3. Choose a **Speed** (x1, x10, x100). Higher speeds run more 0.01 s steps per timer tick; the physics stays the same.
4. Press **Start** to run the simulation and press it again (**Stop**) to stop it. It also stops by itself at equilibrium, when the two temperatures are less than 0.1 °C apart.
5. Press **Graphs** to open the graph window:
   - **Draw** adds the selected body (Body 1, Body 2 or Both) to the graph.
   - **Clear** clears the graph.
   - Move the mouse over the graph to see the time and temperatures at that point.
   - **Export to CSV** saves time, temperature 1 and temperature 2 to `heat_transfer_results.csv` and opens it in Excel.
6. Press **About** for details about the project.

## Physics

Every time step (Δt = 0.01 s):

- I₁ = σ · (T₂ − T₁), I₂ = σ · (T₁ − T₂)
- ΔQ = I · Δt
- ΔT = ΔQ / (m · c)
- New T = T + ΔT

## Materials

The table gives the thermal conductivity k of the material in W/(m·K). The bar between the bodies has a fixed A/L = 0.02 m (for example 2 cm² cross-section and 1 cm length), so σ = k · 0.02 J/s°C.

| Material | k [W/(m·K)] | σ [J/s°C] |
|---|---|---|
| Diamond | 1000 | 20.000 |
| Silver | 406 | 8.120 |
| Copper | 385 | 7.700 |
| Gold | 314 | 6.280 |
| Aluminum | 205 | 4.100 |
| Brass | 109 | 2.180 |
| Iron | 79.5 | 1.590 |
| Steel | 50.2 | 1.004 |
| Lead | 34.7 | 0.694 |
| Mercury | 8.3 | 0.166 |

## Files

| File | Content |
|---|---|
| `Body.py` | The `Body` class: mass, heat capacity, temperature and `add_heat` |
| `Main.py` | The main window and the simulation |
| `graph_window.py` | The graph window: draw, clear and export to CSV |
| `about_window.py` | The About window |
| `style.qss` | The style file shared by all the windows |

Tomer Ben-David, Afeka

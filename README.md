# Heat Transfer - Exercise 5

A PySide6 app that simulates heat conduction between two bodies.

## How to run

```
uv run python Main.py
```

## How to use

1. Set the starting temperature of each body with its slider (0-200 °C). The color goes from black (0 °C) to red (200 °C).
2. Set the mass and heat capacity of each body, and the conductivity between them.
3. Press **Start** to run the simulation and press it again (**Stop**) to stop it.
4. Press **Graphs** to open the graph window:
   - **Draw** adds the selected body (Body 1, Body 2 or Both) to the graph.
   - **Clear** clears the graph.
   - **Export to CSV** saves time, temperature 1 and temperature 2 to `heat_transfer_results.csv` and opens it in Excel.
5. Press **About** for details about the project.

## Physics

Every time step (Δt = 0.01 s):

- I₁ = σ · (T₂ − T₁), I₂ = σ · (T₁ − T₂)
- ΔQ = I · Δt
- ΔT = ΔQ / (m · c)
- New T = T + ΔT

## Files

| File | Content |
|---|---|
| `Body.py` | The `Body` class: mass, heat capacity, temperature and `add_heat` |
| `Main.py` | The main window and the simulation |
| `graph_window.py` | The graph window: draw, clear and export to CSV |
| `about_window.py` | The About window |
| `style.qss` | The style file shared by all the windows |

Tomer Ben-David, Afeka

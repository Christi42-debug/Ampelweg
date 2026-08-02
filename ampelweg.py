import marimo

__generated_with = "0.23.16"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Wedge
    from matplotlib.transforms import Affine2D

    return Wedge, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ampelwegproblem

    Ist man am schnellsten, wenn man direkt über die Ampel läuft oder diagnonal.
    """)
    return


@app.cell
def _(np):
    def gehweg_length(angle_deg):
        return np.tan(np.deg2rad(angle_deg))

    return (gehweg_length,)


@app.cell
def _(angle_slider, gehweg_length):
    gehweg = gehweg_length(angle_slider.value)
    x = [0, gehweg, 0, 0]  # x-Koordinaten der Eckpunkte (letzter Punkt schließt das Dreieck)
    y = [0, 1, 1, 0]    # y-Koordinaten der Eckpunkte
    return x, y


@app.cell
def _(Wedge, angle_slider, np, plt, x, y):
    # Plotten des Dreiecks
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(x, y, marker='o')  # 'marker' zeigt die Eckpunkte an

    # Diagonale
    ax.plot(x[:2], y[:2], color='C1')
    ax.text(np.mean(x[:2]) +0.05, np.mean(y[:2]) - 0.05, s='Diagonale', color='C1', ha='left', va='bottom')

    # Gehweg
    ax.plot(x[1:3], y[1:3], color='C2')
    ax.text(np.mean(x[1:3]), np.mean(y[1:3]), s='Gehweg', color='C2', ha='center', va='bottom')

    # Straße
    plt.plot(x[2:4], y[2:4], color='C3')
    plt.text(np.mean(x[2:4]), np.mean(y[2:4]), s='Straße', color='red', rotation=90, ha='right', va='center')

    # Achsengrenzen festlegen
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlim(-0.2, 2.7)

    # Gleiches Maßstabsverhältnis für x- und y-Achse erzwingen,
    # damit ein Kreis (und damit der Wedge) unabhängig vom Winkel
    # immer als Kreis erscheint, statt als Ellipse verzerrt zu werden.
    ax.set_aspect('equal', adjustable='box')

    # Mittelpunkt und Radius des Kreissegments
    center = (0, 0)
    radius = 0.3  # Radius des Segments

    # Kreissegment als Wedge zeichnen (keine zusätzliche Transformation nötig,
    # da die Achse jetzt ein festes 1:1-Verhältnis hat)
    wedge = Wedge(
        center,
        r=radius,  # Radius des Segments
        theta1=90 - angle_slider.value,  # Startwinkel in Grad
        theta2=90,  # Endwinkel in Grad
        facecolor='blue',  # Füllfarbe
        alpha=0.3,  # Transparenz
        edgecolor='blue',  # Randfarbe
        linewidth=1,
        label=f'Winkel {angle_slider.value:.1f}°'
    )

    # Wedge zum Axes-Objekt hinzufügen
    ax.add_patch(wedge)

    # Achsenbeschriftung und Titel
    ax.set_xlabel('X-Achse')
    ax.set_ylabel('Y-Achse')
    ax.legend()
    #plt.grid(True)
    plt.gca()
    return


@app.cell
def _(mo):
    angle_slider=mo.ui.slider(start=5, stop=68, step=0.2, label='Stelle den Winkel ein:')
    angle_slider
    return (angle_slider,)


@app.cell
def _(mo):
    mo.md(r"""
    $$\mathrm{Weglängenverhältnis} = \frac{\mathrm{Diagonale}}{\mathrm{Straße} + \mathrm{Gehweg}}$$
    """)
    return


@app.cell
def _(angle_slider, gehweg_length, np, plt):
    angle_arr = np.arange(0, 80, 0.1)
    gehweg_arr = gehweg_length(angle_arr)
    strasse_plus_gehweg = gehweg_arr + 1
    diagonale = np.sqrt(1**2 + gehweg_arr**2)

    ratio = diagonale / strasse_plus_gehweg * 100

    x_slider = angle_slider.value
    y_slider = np.sqrt(1**2 + gehweg_length(x_slider)**2) / (gehweg_length(x_slider) + 1) * 100


    plt.figure(figsize=(5,4))
    plt.plot(angle_arr, ratio)
    plt.plot([x_slider, x_slider], [100, y_slider], color='r')
    plt.text(x_slider+1, np.mean([100, y_slider]), s=f'Diagonale\n{100-y_slider:.4f}%\nkürzer', color='red', ha='left')
    plt.xlabel('Winkel in Grad')
    plt.ylabel('Weglängenverhältnis in %')
    plt.grid()
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Bei welchem Winkel ist die Diagonale am kürzesten?
    """)
    return


@app.cell
def _(mo):
    guess_input = mo.ui.number(start=0, stop=90, step=0.1, label="Deine Vermutung (in Grad):")
    guess_input
    return (guess_input,)


@app.cell
def _(guess_input, mo):
    if guess_input.value is None:
        feedback = mo.md("")
    elif abs(guess_input.value - 45) < 0.5:
        feedback = mo.md("✅ **Richtig!** Bei 45° ist die Diagonale am kürzesten.")
    else:
        feedback = mo.md("❌ Leider nicht richtig, versuch's nochmal!")
    feedback
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

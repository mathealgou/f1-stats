import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt

plotting.setup_mpl()
fastf1.Cache.enable_cache('./cache')
qualy = fastf1.get_session(2023, 'Bahrein Grand Prix', 'Q')
qualy.load(laps=True)

perez_lap = qualy.laps.pick_driver('PER').pick_fastest().get_telemetry()

verstappen_lap = qualy.laps.pick_driver('VER').pick_fastest().get_telemetry()


# Speed in km/h throughout the lap
fig, ax = plt.subplots()

plt.title('Perez vs Verstappen')

plt.xlabel('Distance [m]')

plt.ylabel('Speed [km/h]')

ax.plot(perez_lap['Distance'], perez_lap['Speed'], color='green')

ax.plot(verstappen_lap['Distance'], verstappen_lap['Speed'], color='red')


# Breakpoints in the lap
fig2, ax2 = plt.subplots()

fig2.suptitle('Perez vs Verstappen')


def on_press(event):
    if event.key == '1':
        ax2.lines[0].set_visible(not ax2.lines[0].get_visible())
        ax2.lines[1].set_visible(not ax2.lines[1].get_visible())
        fig2.canvas.draw()
    if event.key == '2':
        ax2.lines[2].set_visible(not ax2.lines[2].get_visible())
        ax2.lines[3].set_visible(not ax2.lines[3].get_visible())
        fig2.canvas.draw()


ax2.plot(perez_lap['Distance'], perez_lap['Brake']
         * 100, color='green', label='Perez Brake')
fig2.text(0.5, 0.04, 'Perez Brake', color='green', ha='center')

ax2.plot(perez_lap['Distance'], perez_lap['Throttle'], color='limegreen')
fig2.text(0.5, 0.02, 'Perez Throttle', color='limegreen', ha='center')

ax2.plot(verstappen_lap['Distance'],
         verstappen_lap['Brake'] * 100, color='red')
fig2.text(0.5, 0.06, 'Verstappen Brake', color='red', ha='center')

ax2.plot(verstappen_lap['Distance'],
         verstappen_lap['Throttle'], color='orangered')
fig2.text(0.5, 0.08, 'Verstappen Throttle', color='orangered', ha='center')

fig2.canvas.mpl_connect('key_press_event', on_press)
plt.show()

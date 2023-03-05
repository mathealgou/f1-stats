import fastf1
from fastf1 import plotting
import numpy as np

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
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


# Plot the speed on track
# Get telemetry data
x = perez_lap['X']              # values for x-axis
y = perez_lap['Y']              # values for y-axis
color = perez_lap['Speed']      # value to base color gradient on
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# We create a plot with title and adjust some setting to make it look good.
fig3, ax3 = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
# fig3.suptitle(f'{weekend.name} {year} - {driver} - Speed', size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax3.axis('off')


# After this, we plot the data itself.
# Create background track line
ax3.plot(perez_lap['X'], perez_lap['Y'],
         color='black', linestyle='-', linewidth=16, zorder=0)

# Create a continuous norm to map from data points to colors
norm = plt.Normalize(color.min(), color.max())

colormap = mpl.cm.plasma

lc = LineCollection(segments, cmap=colormap, norm=norm,
                    linestyle='-', linewidth=5)

# Set the values used for colormapping
lc.set_array(color)

# Merge all line segments together
line = ax3.add_collection(lc)


# Finally, we create a color bar as a legend.
cbaxes = fig3.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(
    cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")


plt.show()

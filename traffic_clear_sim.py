# Fixed signal vs Smart signal: how long does each side take to clear its cars?
# Works in Google Colab (pandas, openpyxl and matplotlib are already installed there).
#
# Excel sheet layout (first sheet, 4 rows):
#     Side                  | Cars per 15 min
#     Side 1 (South Ex I)   | 630
#     ...
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- SETTINGS (change these) ----------------
CLEAR_RATE  = 3.25   # cars that get through per second of green
TOTAL_GREEN = 180    # seconds of green shared by the 4 sides (smart signal)
FIXED_GREEN = 45     # seconds per side (fixed signal)
MIN_GREEN   = 20     # smart signal never gives less than this
MAX_GREEN   = 120    # smart signal never gives more than this
LOST_TIME   = 6      # yellow 4 s + all-red 2 s after each green
# ----------------------------------------------------------

# 1. Get the Excel file (upload box in Colab, local file otherwise)
try:
    from google.colab import files
    FILE = list(files.upload())[0]
except ImportError:
    FILE = "traffic_data.xlsx"

data = pd.read_excel(FILE)
sides = data.iloc[:, 0].tolist()        # column 1 = side names
cars = data.iloc[:, 1].tolist()         # column 2 = cars per 15 minutes


# 2. The cycle-time formula for the smart signal
def smart_green(waiting):
    """Green for a side = its cars / all cars x total green, kept between min and max."""
    total = sum(waiting)
    g = [w / total * TOTAL_GREEN if w > 0 else 0 for w in waiting]       # share
    g = [min(MAX_GREEN, max(MIN_GREEN, x)) if x > 0 else 0 for x in g]   # limits
    return [x * TOTAL_GREEN / sum(g) for x in g]                         # total = 180


# 3. Simulation: all the cars are waiting at the start; run the signal until each side is empty
def simulate(smart):
    queue = [float(c) for c in cars]
    clear_time = [None] * len(queue)      # second when each side became empty
    t = 0
    while None in clear_time:
        greens = smart_green(queue) if smart else [FIXED_GREEN] * len(queue)
        for side in range(len(queue)):
            if smart and queue[side] == 0:
                continue                                  # smart signal skips an empty side
            for _ in range(int(greens[side])):
                if queue[side] > 0:
                    n = min(queue[side], CLEAR_RATE)
                    queue[side] -= n
                    if queue[side] == 0:
                        clear_time[side] = t + n / CLEAR_RATE
                t += 1
                if smart and queue[side] == 0:
                    break                                 # smart signal ends green early
            t += LOST_TIME
    return clear_time


# 4. Show the working and the results
print("Cars per 15 min:", dict(zip(sides, cars)))
first = smart_green(cars)
print("\nSmart green times (cars / total cars x", TOTAL_GREEN, "s):")
for s, c, g in zip(sides, cars, first):
    print(f"  {s}: {c} / {sum(cars)} x {TOTAL_GREEN} = {c / sum(cars) * TOTAL_GREEN:.1f} s -> {g:.0f} s")
print(f"Fixed cycle = {FIXED_GREEN}x4 + {LOST_TIME}x4 = {FIXED_GREEN * 4 + LOST_TIME * 4} s")
print(f"Smart cycle = {TOTAL_GREEN} + {LOST_TIME}x4 = {TOTAL_GREEN + LOST_TIME * 4} s")

fixed, smart = simulate(False), simulate(True)

table = pd.DataFrame({
    "Side": sides,
    "Cars": cars,
    "Fixed: time to clear (min)": [round(x / 60, 1) for x in fixed],
    "Smart: time to clear (min)": [round(x / 60, 1) for x in smart],
    "Time saved (min)": [round((f - s) / 60, 1) for f, s in zip(fixed, smart)],
})
print("\n", table.to_string(index=False))
print(f"\nWhole intersection clear:  fixed {max(fixed) / 60:.1f} min,  smart {max(smart) / 60:.1f} min")

# 5. Bar chart
x = range(len(sides))
plt.bar([i - 0.2 for i in x], [v / 60 for v in fixed], 0.4, label="Fixed signal", color="#e74c3c")
plt.bar([i + 0.2 for i in x], [v / 60 for v in smart], 0.4, label="Smart signal", color="#2ecc71")
plt.xticks(list(x), [s.split(" (")[0] for s in sides])
plt.ylabel("Minutes to clear all cars")
plt.title("Time to clear each side")
plt.legend()
plt.show()

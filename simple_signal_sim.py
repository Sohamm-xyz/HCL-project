# Fixed timer vs Smart timer: South Extension intersection
# Run:  python simple_signal_sim.py

# ---------------- SETTINGS (change these) ----------------
CARS_PER_HOUR = [12000, 14000, 11000, 9500]  # peak counts for Side 1..4 (worksheet)
SCALE        = 0.21   # share of those cars that reach this signal
CLEAR_RATE   = 3.25   # cars that get through per second of green
TOTAL_GREEN  = 180    # seconds of green shared by 4 roads each cycle
FIXED_GREEN  = 45     # seconds per road on the old timer
MIN_GREEN    = 20     # smart timer never gives less than this
MAX_GREEN    = 120    # smart timer never gives more than this
LOST_TIME    = 6      # yellow 4 s + all-red 2 s after each road's green
HOURS        = 1
# ----------------------------------------------------------

arrive_per_sec = [c * SCALE / 3600 for c in CARS_PER_HOUR]


def smart_green(waiting):
    """Green time for each road = its share of the cars waiting."""
    total = sum(waiting)
    if total == 0:
        return [TOTAL_GREEN / 4] * 4
    g = [w / total * TOTAL_GREEN for w in waiting]          # 1. share
    g = [min(MAX_GREEN, max(MIN_GREEN, x)) for x in g]      # 2. apply limits
    g = [x * TOTAL_GREEN / sum(g) for x in g]               # 3. make total = 180
    return g


def simulate(smart):
    queue = [0.0] * 4        # cars waiting on each road
    cleared = 0.0
    car_seconds = 0.0        # total waiting, added up second by second
    longest = 0.0
    arrived = 0.0
    seconds = HOURS * 3600
    t = 0
    while t < seconds:
        greens = smart_green(queue) if smart else [FIXED_GREEN] * 4
        for road in range(4):
            # green, then yellow + all-red (no cars clear during the lost time)
            for s in range(int(greens[road]) + LOST_TIME):
                if t >= seconds:      # stop at exactly 1 hour
                    break
                is_green = s < int(greens[road])
                for r in range(4):                       # cars arrive
                    queue[r] += arrive_per_sec[r]
                    arrived += arrive_per_sec[r]
                if is_green:                             # cars leave
                    n = min(queue[road], CLEAR_RATE)
                    queue[road] -= n
                    cleared += n
                car_seconds += sum(queue)
                longest = max(longest, max(queue))
                t += 1
    return cleared / HOURS, car_seconds / arrived, longest


print("Smart green times:", [round(g) for g in smart_green(arrive_per_sec)], "seconds")
print(f"Fixed cycle = {FIXED_GREEN*4} + {LOST_TIME*4} = {FIXED_GREEN*4 + LOST_TIME*4} s")
print(f"Smart cycle = {TOTAL_GREEN} + {LOST_TIME*4} = {TOTAL_GREEN + LOST_TIME*4} s\n")

fixed, smart = simulate(False), simulate(True)
print(f"{'':28}{'Fixed':>9}{'Smart':>9}")
print(f"{'Cars cleared per hour':28}{fixed[0]:9.0f}{smart[0]:9.0f}")
print(f"{'Average waiting time (s)':28}{fixed[1]:9.0f}{smart[1]:9.0f}")
print(f"{'Longest queue (cars)':28}{fixed[2]:9.0f}{smart[2]:9.0f}")

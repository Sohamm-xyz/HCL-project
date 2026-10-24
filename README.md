# Traffic Signal Simulation: Fixed vs Smart (South Extension, Delhi)

**Live animation (no sign-in needed):** https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/

Compares an old fixed-timer signal with a smart signal that gives green time in proportion to the cars waiting:

    green for a side = cars on that side / total cars x total green (kept between 20 s and 120 s)

## Files
- `index.html` - animated simulation of one peak hour (runs in any browser)
- `simple_signal_sim.py` - same one-hour simulation as a Python script (prints results)
- `traffic_clear_sim.py` + `traffic_data.xlsx` - reads the Excel sheet and works out how long each side takes to clear its cars, fixed vs smart (runs in Google Colab)

Data: estimated peak-hour counts from the team worksheet, scaled to about 21% to match the 8,500-11,000 cars/hour that actually get through. The results are simulated, not measured.

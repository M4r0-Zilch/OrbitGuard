# OrbitGuard

#### Description:

OrbitGuard is a lightweight, minimal Flask web application designed for viewing near-Earth asteroids and their telemetry data. Instead of relying on static or hardcoded information, OrbitGuard fetches real-time orbital data directly from NASA's NeoWs (Near Earth Object Web Service) REST API. It also includes an interactive matrix powered by Chart.js displaying threat levels across tracked targets.

The application features a dashboard that represents complex deep-space data cleanly, utilizing a modern, "cyberpunk" inspired UI. It highlights the total number of tracked targets for the day, the highest calculated threat score, and detailed telemetry for every single target in range. 

Users can also interact with the data by pinning their favorite or most concerning targets to a personal Watchlist, backed by a relational database, allowing them to track specific asteroids and remove them whenever they choose.

### The Threat Score Algorithm

The NASA NeoWs API provides the web app with raw data about asteroid names, their unique NASA-assigned IDs, their maximum estimated diameter, relative velocity, and miss distance to Earth.

Using a custom mathematical formula, OrbitGuard calculates a normalized "Threat Score" to determine how dangerous an asteroid is relative to the others. The threat score is scaled strictly between 0.0 and 100.0.

The purely mathematical version of the algorithm is:
\[
\operatorname{round}_1\!\Bigl(
  \min\bigl(
    1000 \cdot \frac{d_{\max} \, v}{m}
    + 15 \cdot \mathbf{1}_{\{\text{hazardous}\}},
    \; 100
  \bigr)
\Bigr)
\]

Where:
* **$d_{\max}$**: Maximum estimated diameter (meters)
* **$v$**: Relative velocity (km/h)
* **$m$**: Miss distance (km)
* **$15$**: A flat penalty score applied if NASA has flagged the object as "Potentially Hazardous".

### Technologies Used
* **Backend:** Python, Flask
* **Database:** SQLite3 (CS50 SQL library)
* **Frontend:** HTML5, CSS3 (Custom CSS Grid/Flexbox), Jinja2 Templating
* **External APIs:** NASA NeoWs
**Chart.js** for charts!

### How to Run Locally

1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   flask run
   ```
5. Open the provided `localhost` (usually at port 5000) URL in your browser to view the dashboard.

### Acknowledgments & Academic Honesty

This project was built as my Final Project for Harvard's CS50x.
It was truly my honor to learn from this course, words alone can't describe how happy I feel after finishing it. Thanks for everything!

### This was CS50!


## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
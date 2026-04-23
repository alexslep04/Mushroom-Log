# Mushroom Log

**team 8 group group** — Aniya Frye, Christopher Ryan, Alex Sleptsov, Benjamin Wingfield, Khushi Patel, Sriya Botlaguduru

A web application for identifying and logging wild mushroom finds. Upload a photo, get AI-powered species suggestions with confidence scores, toxicity info, and taxonomy details, then save everything to a personal collection for future reference.

## Features

- **Photo-based identification** — Upload mushroom photos and receive the top 3 species candidates via the Kindwise mushroom.id API, each with a confidence probability, edibility rating, and taxonomic breakdown.
- **Safety disclaimers** — Clear warnings accompany all identification results to discourage risky consumption based solely on automated predictions.
- **Personal log** — Record the date, location, notes, and photos for each find. Entries are saved to browser localStorage and can be revisited from the Collections page.
- **Export** — Download any log entry as a `.txt` file.
- **Undo support** — The last action (adding/removing a photo, editing notes, toggling location) can be undone.

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18+ recommended)
- A Kindwise mushroom.id API key — sign up at [kindwise.com](https://www.kindwise.com/)

### Setup

1. Clone the repo and `cd` into it.
2. Create a `.env` file in the project root:
   ```
   MUSHROOM_API_KEY=your_api_key_here
   ```
3. Start the server:
   ```
   node server.js
   ```
4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

The server proxies identification requests to the Kindwise API so that your API key is never exposed to the browser.

## Running Tests

The test suite uses Python's `unittest` and runs the real JavaScript from `index.html` inside Node with lightweight DOM stubs:

```
python3 test_pm4_unit_tests.py -v
```

## Project Structure

- `index.html` — Single-file frontend (HTML, CSS, and JavaScript)
- `server.js` — Node.js HTTP server with static file serving and API proxy
- `test_pm4_unit_tests.py` — Unit and integration tests
- `IMPLEMENTATION.md` — Detailed implementation notes and AI usage disclosure

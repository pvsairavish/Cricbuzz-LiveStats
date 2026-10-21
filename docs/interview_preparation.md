# 🏏 Cricbuzz LiveStats — 50 Viva & Technical Interview Questions

A comprehensive compilation of 50 technical interview questions and expert answers categorized across Python/Streamlit, SQL Database Architecture, REST APIs, and Sports Analytics.

---

## 🐍 Section 1: Python, Architecture & Streamlit (15 Questions)

### Q1: What is the high-level architecture of Cricbuzz LiveStats?
**Answer:** It follows a decoupled multi-tier architecture:
1. **Presentation Layer**: Streamlit multi-page web application with custom CSS styling and Plotly visualizations.
2. **Business Service Layer**: Modular domain handlers (`MatchService`, `PlayerService`, `AnalyticsService`, `CRUDService`).
3. **Data / Storage Layer**: SQLite database (`cricbuzz.db`) with 3NF tables, virtual generated columns, and composite B-tree indexes.
4. **External API Layer**: Resilient HTTP client interacting with the Cricbuzz API on RapidAPI with connection pooling, TTL caching, and offline mock fallback.

### Q2: Why did you choose Streamlit over frameworks like Django or Flask?
**Answer:** Streamlit enables rapid development of reactive, data-centric dashboards directly in Python. It integrates natively with Pandas and Plotly, allows stateful component caching (`st.cache_data`), and eliminates boilerplate JavaScript while supporting custom CSS injection for modern dark-mode glassmorphism.

### Q3: How do you prevent blocking UI performance during live API calls?
**Answer:**
1. In-memory TTL caching in the API client (`CACHE_TTL_LIVE_MATCHES = 60s`, `CACHE_TTL_PLAYER_STATS = 24h`).
2. Streamlit spinner placeholders (`st.spinner`).
3. Short request timeouts (10 seconds) with fallback mechanisms to ensure the application never hangs.

### Q4: How is thread safety handled in the SQLite database connector?
**Answer:** In `utils/db_connection.py`, SQLite connections are opened using a context manager with `check_same_thread=False` and are immediately closed in a `finally` block upon query completion.

### Q5: How do virtual generated columns work in your SQLite schema?
**Answer:** Columns like `strike_rate` in `batting_stats` and `economy_rate` in `bowling_stats` are defined with `GENERATED ALWAYS AS (...) STORED`. SQLite automatically calculates these values upon row insertion/update without requiring redundant application code or triggers.

### Q6: What is the purpose of `sys.path` manipulation in your service modules?
**Answer:** To ensure that whether a file is executed as a standalone script (e.g. `python utils/db_connection.py`) or imported as a package module (e.g. `from services.match_service import match_service`), Python always resolves the project root directory without raising `ModuleNotFoundError`.

### Q7: How does your application handle environment variables securely?
**Answer:** Through `config.py` using `python-dotenv`. Sensitive credentials (such as `RAPIDAPI_KEY`) are stored in `.env` or Streamlit Secrets and excluded from Git commits via `.gitignore`.

### Q8: What design pattern is used in your Service Layer?
**Answer:** The **Singleton Pattern** combined with the **Service Facade Pattern**. Each service exposes a single shared instance (e.g., `crud_service = CRUDService()`) that abstracts database queries and API calls away from the Streamlit UI.

### Q9: How are CRUD input validation errors communicated to the user?
**Answer:** In `utils/validators.py`, custom `ValidationError` exceptions are raised whenever constraints are violated (e.g., Team 1 equals Team 2, negative runs, invalid formats). The Streamlit UI catches these and displays clean, informative `st.error()` alerts.

### Q10: How does Streamlit's multi-page directory routing work?
**Answer:** Files placed inside the `pages/` directory with numeric prefixes (e.g., `1_⚡_Live_Matches.py`, `2_📊_Top_Players.py`) are automatically detected and rendered by Streamlit in the sidebar navigation with formatted names and icons.

### Q11: How do you achieve dark glassmorphism in Streamlit?
**Answer:** By injecting CSS (`assets/styles.css`) using `st.markdown(..., unsafe_allow_html=True)`. We define CSS variables, linear gradient backgrounds (`rgba(30, 41, 59, 0.8)`), and `backdrop-filter: blur(10px)`.

### Q12: Why did you use `requests.Session` instead of plain `requests.get`?
**Answer:** `requests.Session` persists connection pools across multiple HTTP requests, drastically reducing TCP and TLS handshake overhead when querying RapidAPI repeatedly.

### Q13: How do you test Streamlit applications programmatically?
**Answer:** We separate UI logic from business logic. The service and database functions are tested via `pytest` (47 unit tests), and the rendered UI is validated end-to-end using browser subagent automation.

### Q14: How does data flow when a user requests a match scorecard?
**Answer:** Streamlit UI → `MatchService.get_detailed_scorecard(match_id)` → `CricbuzzAPIClient.get_match_scorecard()` → Checks TTL cache → RapidAPI endpoint (or mock fallback) → JSON parsed into clean innings lists → Returned to UI for tabular and chart rendering.

### Q15: How do you handle database migrations or seed resetting?
**Answer:** The `init_database(force_recreate=True)` function in `utils/db_connection.py` drops and re-executes `schema.sql`, `indexes.sql`, and `seed_data.sql` in an atomic script execution.

---

## 🗄️ Section 2: SQL, Database & Window Functions (15 Questions)

### Q16: What is a Common Table Expression (CTE) and where did you use it?
**Answer:** A CTE (`WITH cte_name AS (...)`) defines a temporary named result set within a single SQL statement. In Query 21 (Player MVP ranking), we used CTEs to isolate batting, bowling, and fielding aggregations before computing composite scores.

### Q17: What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`?
**Answer:**
- `ROW_NUMBER()`: Assigns a unique, consecutive integer to each row regardless of ties ($1, 2, 3, 4$).
- `RANK()`: Assigns the same rank to ties and skips subsequent numbers ($1, 2, 2, 4$).
- `DENSE_RANK()`: Assigns the same rank to ties without skipping ($1, 2, 2, 3$).

### Q18: How does the `LAG()` window function work in Query 25?
**Answer:** `LAG(qtr_avg_runs) OVER (PARTITION BY player_id ORDER BY year_quarter ASC)` retrieves the batting average from the *previous quarter* for that same player, allowing calculation of quarter-over-quarter net run changes (`qtr_avg_runs - prev_qtr_runs`).

### Q19: How did you compute population standard deviation in SQLite (Query 19)?
**Answer:** Since standard SQLite lacks a native `STDDEV()` aggregate, we implemented the algebraic variance identity:
$$\sigma = \sqrt{\text{AVG}(x^2) - (\text{AVG}(x))^2}$$
Expressed as: `SQRT(MAX(0.0, AVG(runs*runs) - (AVG(runs)*AVG(runs))))`.

### Q20: How are century batting partnerships identified in Query 13?
**Answer:** By self-joining `batting_stats b1` and `batting_stats b2` on matching `match_id` and `innings`, where `b2.batting_position = b1.batting_position + 1` and `(b1.runs_scored + b2.runs_scored) >= 100`.

### Q21: What database normalization form does your schema follow?
**Answer:** Third Normal Form (3NF). Every non-key attribute is dependent on the primary key, the whole primary key, and nothing but the primary key. Teams, venues, players, series, and matches are normalized into separate tables with foreign key constraints.

### Q22: What indexes were created and why?
**Answer:** 14 B-tree indexes were created in `indexes.sql` on foreign keys and frequently filtered columns:
- `idx_matches_date` for chronological lookups.
- `idx_batting_player` and `idx_bowling_player` for stats joins.
- `idx_batting_partnership` on `(match_id, innings, batting_position)` for fast partnership lookups.

### Q23: How do you prevent division by zero in SQL batting average calculations?
**Answer:** By using `NULLIF(dismissals, 0)`. If a batsman is never dismissed (`dismissals = 0`), `NULLIF` turns the denominator into `NULL`, preventing a divide-by-zero runtime error and resulting in `NULL` rather than a crash.

### Q24: How does SQLite enforce foreign keys?
**Answer:** Foreign key enforcement is disabled by default in SQLite for backward compatibility. It must be explicitly enabled per connection by running `PRAGMA foreign_keys = ON;`, which is automatically configured in `get_db_connection()`.

### Q25: How does Query 12 evaluate Home vs Away wins?
**Answer:** By comparing the team's country with the host venue's country:
`CASE WHEN v.country = t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END AS home_wins`.

### Q26: What is conditional aggregation? Give an example from your project.
**Answer:** Performing aggregate functions on a subset of data using `CASE WHEN` inside the aggregate. Example in Query 11:
`SUM(CASE WHEN b.format = 'Test' THEN b.runs_scored END) AS test_runs`.

### Q27: How does Query 22 normalize rival team pairs for head-to-head records?
**Answer:** To group both IND vs AUS and AUS vs IND matches together, we use symmetric pair ordering:
`CASE WHEN team1_id < team2_id THEN team1_id ELSE team2_id END AS tA_id`.

### Q28: How is the Custom SQL Console secured against SQL injection and destructive queries?
**Answer:** In `AnalyticsService.execute_custom_sql()`, queries are inspected against a blacklist of DDL/DML keywords (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`). Only read-only queries are executed.

### Q29: What is the difference between `WHERE` and `HAVING` in SQL?
**Answer:** `WHERE` filters rows *before* any grouping or aggregation takes place. `HAVING` filters aggregated group results *after* `GROUP BY` (e.g. `HAVING COUNT(DISTINCT format) >= 2`).

### Q30: Why is `strftime('%Y', match_date)` used instead of `YEAR(match_date)`?
**Answer:** SQLite does not have a dedicated `YEAR()` function. Date and time manipulations are performed using `strftime(format, timestring)` where `'%Y'` extracts the four-digit year.

---

## 🌐 Section 3: REST APIs, Caching & Resilience (10 Questions)

### Q31: What headers are required to authenticate with RapidAPI Cricbuzz?
**Answer:**
- `x-rapidapi-key`: The subscriber's unique authentication token.
- `x-rapidapi-host`: `cricbuzz-cricket.p.rapidapi.com`.
- Optional locale headers: `CB-Loc: IN` and `CB-TZ: +0530`.

### Q32: What happens if your RapidAPI subscription quota is exceeded (HTTP 429)?
**Answer:** The `CricbuzzAPIClient` intercepts the non-200 HTTP status code, logs a warning, and immediately returns high-fidelity fallback data from `api/mock_data.py`. The dashboard remains completely functional without crashing.

### Q33: How does the in-memory cache operate in `CricbuzzAPIClient`?
**Answer:** It stores responses in a Python dictionary keyed by `endpoint:params` mapped to a tuple `(timestamp, data)`. When a request is made, if `current_time - timestamp < ttl`, the cached data is returned immediately without hitting the network.

### Q34: Why do live matches and player stats have different Cache TTLs?
**Answer:**
- **Live matches** change ball-by-ball, so they use a short TTL of **60 seconds** (`CACHE_TTL_LIVE_MATCHES`).
- **Player career stats** rarely change during a session, so they use a long TTL of **24 hours** (`CACHE_TTL_PLAYER_STATS`).

### Q35: What is the difference between the mini-scorecard and full scorecard endpoints?
**Answer:**
- **Mini-scorecard (`/hsc`)**: Lightweight endpoint returning current runs, wickets, overs, and match summary status for dashboard cards.
- **Full scorecard (`/scard`)**: Heavy endpoint containing every batting innings, individual batsman balls, 4s, 6s, strike rates, dismissals, and bowler spell figures.

### Q36: How do you mock external APIs during automated testing?
**Answer:** By utilizing `api/mock_data.py` as default payloads and testing both with and without API keys using `pytest` fixtures.

### Q37: How did you test that the API key was valid from the command line?
**Answer:** By sending an authenticated `GET` request using `requests` or `curl` to `https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live` and verifying a `200 OK` response with a valid JSON payload.

### Q38: How does the application detect whether live mode or mock mode is active?
**Answer:** `config.py` evaluates:
`IS_LIVE_API_ENABLED = bool(RAPIDAPI_KEY and RAPIDAPI_KEY.strip() != "")`.
The UI displays a green badge `● API Connected` or yellow badge `● Mock Mode` accordingly.

### Q39: What error codes can the Cricbuzz API return and how are they handled?
**Answer:**
- `401 Unauthorized / 403 Forbidden`: Invalid key → Fallback to mock data.
- `429 Too Many Requests`: Rate limit reached → Fallback to mock data.
- `500 Internal Server Error`: RapidAPI service glitch → Fallback to mock data.
- `requests.Timeout`: Network slow → Handled cleanly after 10 seconds.

### Q40: How would you scale the caching mechanism for hundreds of concurrent users?
**Answer:** By replacing the in-memory dictionary cache with an external distributed cache like **Redis** or using Streamlit's distributed cache primitives (`@st.cache_data(ttl=60)`).

---

## 📊 Section 4: Sports Analytics & Domain Knowledge (10 Questions)

### Q41: How is a batsman's strike rate defined and calculated?
**Answer:** Strike rate is the average number of runs scored per 100 balls faced:
$$\text{Strike Rate} = \left(\frac{\text{Runs Scored}}{\text{Balls Faced}}\right) \times 100$$

### Q42: How is a bowler's economy rate calculated?
**Answer:** Economy rate is the average number of runs conceded per over (6 legal balls):
$$\text{Economy Rate} = \frac{\text{Runs Conceded}}{\text{Overs Bowled}}$$

### Q43: How is a bowler's bowling average defined?
**Answer:** Bowling average is the average number of runs conceded per wicket taken:
$$\text{Bowling Average} = \frac{\text{Runs Conceded}}{\text{Wickets Taken}}$$
A lower bowling average indicates a more effective bowler.

### Q44: What constitutes a "close match" in your analytical model (Query 15)?
**Answer:** A match decided by **less than 50 runs** (for matches won by runs) OR **less than 5 wickets** (for matches won by chasing wickets).

### Q45: Explain the Weighted MVP Composite Ranking Formula used in Query 21.
**Answer:**
$$\text{Batting Pts} = (\text{Runs} \times 0.01) + (\text{BatAvg} \times 0.5) + (\text{SR} \times 0.3)$$
$$\text{Bowling Pts} = (\text{Wkts} \times 2) + ((50 - \text{BowlAvg}) \times 0.5) + ((6 - \text{Econ}) \times 2)$$
$$\text{Fielding Pts} = (\text{Catches} \times 3) + (\text{Stumpings} \times 5)$$
It balances batting volume/efficiency, bowling penetration/thrift, and fielding dismissals into a standardized score.

### Q46: How does toss winning influence match victory probability (Query 17)?
**Answer:** By aggregating matches where `toss_winner_id = winner_id` and grouping by `toss_decision` (batting first vs fielding first), determining whether modern teams gain a statistical edge by fielding first under dew or batting first on deteriorating pitches.

### Q47: Why is standard deviation used to assess batting consistency (Query 19)?
**Answer:** A batsman with high average runs but high standard deviation is volatile (alternating between centuries and ducks). A low standard deviation reflects reliable run contributions innings after innings.

### Q48: How are player momentum and form categorized in Query 23?
**Answer:** By comparing performance in the last 5 innings versus the last 10 innings along with 50+ scores:
- **Excellent Form**: Average $\ge 60$ runs or $\ge 3$ half-centuries in last 5 matches.
- **Good Form**: Average $\ge 40$ runs.
- **Average Form**: Average $\ge 25$ runs.
- **Poor Form**: Average $< 25$ runs.

### Q49: What is the significance of the "home advantage" metric in cricket (Query 12)?
**Answer:** Teams play on pitches tailored to their domestic strengths (e.g. spin in India, bounce in Australia, swing in England). Comparing home wins to away wins quantifies team adaptability across conditions.

### Q50: How does time-series career trajectory classification work in Query 25?
**Answer:** By comparing consecutive quarters with `LAG()`, players with positive run differentials ($> +10$ runs) are classified as **Performance Improving**, while quarterly averages $\ge 60$ runs categorize a cricketer as **Career Ascending / Prime**.

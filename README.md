# SauceDemo Selenium Test Suite

An automated test suite for [saucedemo.com](https://www.saucedemo.com), built with Selenium WebDriver, pytest, and the Page Object Model, with CI running on GitHub Actions.

## What this covers

- Login flows for all four SauceDemo users (`standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`)
- Full checkout flow (add to cart → checkout → order confirmation)
- Assertions against `problem_user`'s known application bugs (broken sort, swapped images, wrong item navigation)
- A timing-based performance assertion for `performance_glitch_user`
- Headless CI execution on every push/PR to `main`, with branch protection requiring tests to pass before merge

## Project structure

```
.
├── .github/workflows/tests.yml   # CI workflow
├── conftest.py                    # pytest fixtures (driver, login_as)
├── requirements.txt
├── pages/                         # Page Object Model
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── checkout_page.py
│   └── navbar.py
└── test_saucedemo.py              # test cases
```

## Setup

```bash
pip install -r requirements.txt
```

Selenium Manager handles the local geckodriver install automatically — no manual driver setup needed to run tests on your own machine.

## Running the tests

```bash
pytest test_saucedemo.py -v
```

## Design notes

- **Page Object Model** — locators and page interactions live in `pages/`, kept out of test logic. Each page object owns the waits for its own elements becoming ready, so tests don't need to manually wait between steps.
- **Fixtures over manual setup** — `conftest.py` defines a `driver` fixture (headless Firefox, with automatic teardown via `yield`) and a `login_as` factory fixture, so each test gets a fully isolated browser session and can log in as whichever user it needs with one line.
- **One test function per user**, not a shared loop — each user exercises different behavior (checkout vs. error message vs. known bugs vs. timing), so separate test functions give independent pass/fail reporting instead of one monolithic test masking failures.
- **`problem_user`'s assertions check for the *known* broken behavior** (`assert prices != sorted(prices)`, etc.) rather than logging a warning, so the test correctly fails if the site's bugs are ever fixed rather than silently passing forever.
- **`performance_glitch_user`'s delay lives inside the login button's `click()` call itself** (confirmed by instrumenting each step with timestamps), so it's asserted with a `time.time()` bracket around the click rather than a `WebDriverWait`, since a wait can't observe anything that happens *inside* a single blocking command.

## CI

GitHub Actions runs the full suite in headless Firefox on every push and PR to `main` (`.github/workflows/tests.yml`). Branch protection on `main` requires this check to pass before merging.

## Possible next steps

- API testing layer alongside the UI tests
- `pytest-html` or Allure for shareable HTML reports
- Parallel/cross-browser execution via `pytest-xdist`

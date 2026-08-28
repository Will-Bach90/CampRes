## 1. Confirm Python is on your PATH

Open **Command Prompt** (press the Windows key, type `cmd`, hit Enter) and type:

```
python --version
```

- If you see something like `Python 3.12.4`, you're good — skip to step 2.
- If instead you get `'python' is not recognized as an internal or external
  command...`, Python wasn't added to PATH during install. Re-run the Python installer (find it in your Downloads, or download it
  again from [python.org/downloads](https://www.python.org/downloads/)),
  choosing **"Modify"**, and on the **Optional Features/Advanced Options**
  screen checking the box for **"Add python.exe to PATH"** (or "Add Python
  to environment variables"), then finishing the install. Close and reopen
  Command Prompt and try `python --version` again.

## 2. Get project onto your computer

Download this project onto your computer, into a place you'll remember,
like your Desktop (e.g. as a ZIP from GitHub — click **Code → Download
ZIP**, then extract it). You should end up with a `CampRes` folder.

Then open Command Prompt and navigate into it. For example, if it's on your
Desktop:

```
cd Desktop\CampRes
```

## 3. Set up the project (one-time only)

Copy and paste these commands into Command Prompt **one at a time**, inside
the `CampRes` folder:

```
python -m venv .venv
```

This creates an isolated environment for the project so it doesn't
interfere with anything else on your computer.

```
.venv\Scripts\activate
```

Your prompt should now start with `(.venv)`. You'll need to run this
`activate` command every time you open a new Command Prompt window to work
on this project.

```
pip install playwright
```

This installs the automation library the script uses to control a browser.

```
playwright install chromium
```

This downloads the actual browser (Chrome) that the script will drive.
It's a one-time download.

## 4. About the dates (for testing)

This script is already set up for a specific booking — you shouldn't need
to change anything to use it as-is. The one thing you might want to adjust
while testing is the timing, in `explore.py`:

| What | Where | Notes |
|---|---|---|
| Reservation dates | `START_DATE` / `END_DATE` (top of file) | `"April 28,"` |
| Exact moment to snipe the reservation | `OPEN_YEAR` / `OPEN_MONTH` / `OPEN_DAY` / `OPEN_HOUR` / `OPEN_MINUTE` / `OPEN_SECOND` (top of file) | hour is 24-hr |

**The `target` time is in Pacific Time** (`America/Los_Angeles`) — this
matches the park's own clock on the booking site, not your local time
zone, so you generally don't need to convert it. Set `target` a minute or
two in the future to do a dry-run test.

## 5. Run it

Every time you want to run the script, open Command Prompt, go to the
project folder, activate the environment, then run the script:

```
cd Desktop\CampRes
.venv\Scripts\activate
python explore.py
```

A Chrome window will pop up and you'll see it navigate the site on its own.
Don't close it or click inside it — just watch. The script prints progress
in the Command Prompt window, including a countdown to the target time.

At the very end, the script stops at the site's **log-in page**. This is where you take over - log in and complete the purchase yourself. You have
**15 minutes** from this point to finish checkout before the reservation
site releases the site back into the pool, so don't walk away. 

**Do not go on to step 6 below until you've completed the purchase - the chrome window will close and you'll lose your cart**

## 6. Stopping the script

If you need to stop it early, click into the Command Prompt window and
press `Ctrl + C`. You can also just close the Chrome window it opened.

---

## Troubleshooting

- **`'python' is not recognized...`** — Python wasn't added to PATH.
  Reinstall Python and make sure to check "Add python.exe to PATH."
- **`'.venv\Scripts\activate' is not recognized` or a permissions error**
  — In Command Prompt (not PowerShell) this should just work. If you're
  using PowerShell and get a script-execution error, either switch to
  Command Prompt, or run PowerShell as Administrator and execute:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- **The script errors out on a `page.get_by_...` line** — the campsite
  booking website likely changed its layout/wording since this script was
  written. The corresponding line will need to be updated to match the new
  page.
- **"Target time has already passed"** — the `target` value in
  `explore.py` is set to a specific date and time. Update it to a future
  time before running.


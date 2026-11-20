# Job Search Robot

Job Search Robot is an RPA application that searches several Finnish job portals for job listings using keywords and locations defined by the user. The robot collects the listings, removes duplicates, combines the results into a single Excel file and sends the file by email to the address given by the user.

## Features

- Searches for jobs on three portals:
  - [Työmarkkinatori](https://tyomarkkinatori.fi)
  - [Jobly](https://www.jobly.fi)
  - [Duunitori](https://duunitori.fi)
- Keywords and locations are defined in a single JSON file
- Removes duplicates (same listing URL, or same title + company + location)
- If one portal fails, the others still run
- Saves the results into a single Excel file (`output/Jobs.xlsx`)
- Sends the Excel file as an attachment to the user's email

## Excel File Contents

The file `output/Jobs.xlsx` contains one job per row with the following columns:

| Column       | Description                              |
|--------------|------------------------------------------|
| Title        | Job title                                |
| Company      | Employer                                 |
| Location     | Location                                 |
| URL          | Link to the job listing                  |
| Job portal   | The portal where the listing was found   |

## Project Structure

```
.
├── tasks.py               # Main program: runs the searches, merges results, writes the Excel file and sends the email
├── tyomarkkinatori.py     # Työmarkkinatori search
├── jobly.py               # Jobly search
├── duunitori.py           # Duunitori search
├── search_criteria.json   # Keywords, locations and email recipient
├── robot.yaml             # Robocorp robot configuration
├── conda.yaml             # Dependencies and Python environment
├── .env                   # Email credentials (do not commit to version control!)
└── output/                # Output files (Jobs.xlsx)
```

## Requirements

- [Robocorp / Sema4.ai RCC](https://github.com/robocorp/rcc), or alternatively Python 3.13 and the dependencies listed below
- A Gmail account for sending email

Dependencies (defined in `conda.yaml`):

- `python=3.13.15`
- `uv=0.10.9`
- `python-dotenv`
- `rpaframework==33.0.2`
- `robocorp==3.1.6`
- `robocorp-browser==2.4.0`
- `requests`

## Installation and Setup

1. **Clone the project**

   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Edit the search criteria** in `search_criteria.json`:

   ```json
   {
     "keywords": [
       "ohjelmistokehittäjä",
       "software developer"
     ],
     "location": ["Helsinki", "Espoo", "Vantaa"],
     "email_recipient": "name@example.com"
   }
   ```

   | Field             | Required | Description                                                                  |
   |-------------------|----------|------------------------------------------------------------------------------|
   | `keywords`        | Yes      | List of keywords. Each keyword is searched separately.                       |
   | `location`        | Yes      | List of cities. The search is run for all listed locations.                  |
   | `email_recipient` | Yes      | Email address the Excel file is sent to.                                     |
   | `job_type`        | No       | With the value `"full-time"`, the Duunitori search is limited to full-time jobs. |

3. **Create a `.env` file** in the project root and add the email credentials:

   ```
   EMAIL_ACCOUNT=your.address@gmail.com
   EMAIL_PASSWORD=app-specific-password
   ```

   > **Note:** Gmail usually requires an [app password](https://support.google.com/accounts/answer/185833); your regular account password will not work. Never commit the `.env` file to version control – add it to `.gitignore`.

## Running

- Install [Sema4.ai SDK](https://marketplace.visualstudio.com/items?itemName=sema4ai.sema4ai) extension to your VSCode.  
- Press Ctrl + Shift + P
- Select Sema4.ai: Run Task Package

During a run, the robot:

1. Loads the search criteria from `search_criteria.json`
2. Opens a browser (visible by default) and searches Työmarkkinatori, Jobly and Duunitori
3. Merges the results and removes duplicates
4. Writes the results to `output/Jobs.xlsx`
5. Sends the file by email to the recipient

If no listings are found on any portal, the robot does not create the Excel file or send an email.

## Configuration

- **Browser visibility and speed:** In `tasks.py`, the call `browser.configure(headless=False, slowmo=500)`. Set `headless=True` to run the robot without a visible browser window, and lower the `slowmo` value to speed up the run.
- **Duunitori page count:** The constant `PAGES_PER_SEARCH` in `duunitori.py` determines how many result pages (20 listings per page) are fetched per search. The default is 2.
- **Email server:** By default, Gmail's SMTP server (`smtp.gmail.com:587`) is used. You can change the server in the `send_excel_by_email` function in `tasks.py`.

## How It Works

```
search_criteria.json
        │
        ▼
 ┌──────────────────┬─────────┬───────────┐
 │ Työmarkkinatori  │  Jobly  │ Duunitori │   (browser automation, Playwright)
 └──────────────────┴─────────┴───────────┘
        │
        ▼
 Merge results + remove duplicates
        │
        ▼
 output/Jobs.xlsx
        │
        ▼
 Send by email (SMTP)
```

## Troubleshooting

- **A portal fails:** An error message is printed to the console (`ERROR: <portal> failed`), and the robot continues with the other portals. Portal page structures change from time to time, in which case the selectors for that portal need to be updated.
- **Email is not sent:** Check that the `.env` file contains the correct `EMAIL_ACCOUNT` and `EMAIL_PASSWORD` values and that the Gmail account uses an app password.
- **`KeyError: 'EMAIL_ACCOUNT'`:** The `.env` file is missing or the variables have not been set.

## Author

Atte Liikanen, Saara Orvas, Jiro Pärnänen

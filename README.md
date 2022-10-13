# MPR Size
A simple Python tool to extract object sizes from Mendix MPR files and export them into Excel reports.

## Setup
    pip install git+https://github.com/richardburleigh/mpr-size.git

## Command-line usage

```
mprsize -i project.mpr -o report.xlsx

Command-line arguments:
  -i INPUT, --input INPUT,  MPR file to analyze
  -o OUTPUT, --output OUTPUT,  Excel file to write to
  -l LIMIT, --limit LIMIT,  Limit final report to N rows per sheet (Optional)
```

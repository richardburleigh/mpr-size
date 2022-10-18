# MPR Size
A simple Python tool to extract object sizes from Mendix MPR files and export them into Excel reports.

## Binary Downloads
Binaries are available on the [Releases](https://github.com/richardburleigh/mpr-size/releases/) page

## Python Setup
As an alternative to pre-compiled binaries, you can install MPR Size from the master branch via pip:

    pip install git+https://github.com/richardburleigh/mpr-size.git

## Command-line usage

```
mprsize -i project.mpr -o report.xlsx

Command-line arguments:
  -i INPUT, --input INPUT,  MPR file to analyze
  -o OUTPUT, --output OUTPUT,  Excel file to write to
  -l LIMIT, --limit LIMIT,  Limit final report to N rows per sheet (Optional)
  --csv,  Export to CSV files (Optional)
```

## Example output

|   |        **Type**        |           **Name**           | **Size** |
|---|:----------------------:|:----------------------------:|:--------:|
| 0 | Images$ImageCollection | Content                      | 2M       |
| 1 | Forms$PageTemplate     | Tablet_Dashboard_User_Detail | 1M       |
| 2 | Forms$PageTemplate     | Dashboard_User_Detail        | 1M       |
| 3 | Forms$PageTemplate     | Dashboard_Charts2            | 1020K    |
| 4 | Forms$PageTemplate     | Dashboard_Charts3            | 863K     |
| 5 | Forms$PageTemplate     | Dashboard_Charts             | 829K     |
| 6 | Forms$PageTemplate     | Tablet_Dashboard_Metrics     | 786K     |
| 7 | Forms$PageTemplate     | Dashboard_Metrics            | 786K     |
| 8 | Forms$PageTemplate     | Dashboard_Expenses           | 616K     |

|          |        |          |               |
|----------|:------:|:--------:|:-------------:|
| <ins>**Overview**</ins> | _Images_ | _Entities_ | _Uncategorized_ |


_Please note that this tool is not developed, supported, or endorsed by Siemens / Mendix and no claims are made to the validity of results._

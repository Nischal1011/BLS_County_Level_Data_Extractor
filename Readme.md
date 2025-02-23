# BLS County-Level Unemployment Data Extractor

## Overview

This project provides a streamlined way to pull county-level Local Area Unemployment Statistics (LAUS) data from the Bureau of Labor Statistics (BLS) public API. With a simple setup, users can fetch, process, and export the latest unemployment rates for U.S. counties.

## Features

- **Automated Data Retrieval**: Fetch LAUS data for multiple counties using their FIPS codes
- **Efficient Batching**: Handles BLS API's 50-series limit per request
- **Data Processing**: Converts raw JSON responses into a clean Pandas DataFrame
- **Customizable Queries**: Supports flexible year ranges and county selections
- **CSV Export**: Outputs processed data to a CSV file

## Repository Structure

```bash
📦 BLS County-Level Unemployment Data Extractor
├── 📄 BLS_LAU_County.py        # Main script to pull and process BLS data
├── 📁 data/                    # Data directory
│   └── 📄 county_geoid.csv     # Sample county FIPS codes (GEOID)
├── 📄 requirements.txt         # Required packages
├── 📄 .env.example            # Example for storing BLS API key
└── 📄 README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.7+
- BLS API key (register at https://data.bls.gov/registrationEngine/)
- County FIPS codes list

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/BLS-County-Level-Unemployment-Data-Extractor.git
cd BLS-County-Level-Unemployment-Data-Extractor
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your BLS API key:
```bash
cp .env.example .env
# Edit .Env and Add Your BLS API Key
```

5. Prepare county FIPS codes:
   - Place your county_geoid.csv file in the data/ directory
   - Ensure it contains a column named 'GEOID' with county FIPS codes
   - You can download county FIPS codes from the [Census Bureau](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html)

## Usage

Run the main script to fetch unemployment data:

```bash
python BLS_LAU_County.py
```

### Sample Output

The script generates a CSV file with county-level unemployment data:

```bash
$ head -n 5 output/unemployment_data.csv
fips,unemployment_rate,year,month
17031,4.5,2023,09
17037,3.8,2023,09
06037,5.1,2023,09
```

## Configuration

Edit `.env` file to customize:
- `BLS_API_KEY`: Your BLS API key
- `START_YEAR`: Beginning year for data extraction (default: 2019)
- `END_YEAR`: End year for data extraction (default: current year)

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/new-feature
```
3. Commit your changes:
```bash
git commit -am 'Add new feature'
```
4. Push to the branch:
```bash
git push origin feature/new-feature
```
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bureau of Labor Statistics for providing the API
- U.S. Census Bureau for county FIPS codes data
```
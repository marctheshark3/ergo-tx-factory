Certainly! I'll update the README.md file with the PostgreSQL setup instructions and add more relevant information. Here's an expanded version of the README:

```markdown
# Sigmanauts Mining Core - Payment Mechanism

This codebase performs the needed execution of payments to miners when balances are over the minimum payout threshold. Additionally, this code supports the swapping of native tokens from the pool's wallet to the miners' wallets based on Spectrum prices as well as looking for changes in minimum payouts.

One can look at the token swap as "a dollar cost averaging" approach into Ergo's Native Tokens of choice.

## Prerequisites

- Python 3.x
- PostgreSQL 13 or higher
- `python-dotenv` package
- `ergpy` package
- `psycopg2` package
- `Flask` package (for API)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/marctheshark3/ergo-tx-factory
   cd ergo-tx-factory
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL:
   - Install PostgreSQL if not already installed
   - Start the PostgreSQL service
   - Create a new user and database:
     ```bash
     sudo -u postgres psql
     ```
     Then in the PostgreSQL prompt:
     ```sql
     CREATE USER sigs_user WITH PASSWORD 'your_password_here';
     CREATE DATABASE "SIGS-CORE" OWNER sigs_user;
     \q
     ```

4. Create a .env file in the root directory of the project with the following content:
   ```
   DB_NAME=SIGS-CORE
   DB_USER=sigs_user
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432
   SWAP_MNEMONIC=Your_SEED_PHRASE
   ```

## Usage

### Database Setup

To set up the database and create necessary tables:

```python
from src.database import PostgresDB

db = PostgresDB()
db.create_db()
db.create_table('miners', {
    'address': 'TEXT PRIMARY KEY',
    'balance': 'NUMERIC',
    'min_payout': 'NUMERIC'
})
```

### Running the Payment Mechanism

To execute the payment mechanism:

```python
from src.core import SigsCore

robot = SigsCore()
df = robot.execute(debug=False)
```

This will:
1. Check for miners with balances over their minimum payout threshold
2. Execute payments for eligible miners
3. Perform token swaps if necessary
4. Return a DataFrame with the results of the operations

### API Usage

To start the API server:

```bash
python src/api.py
```

Then you can access the API at `http://localhost:5000/api/<table_name>` to retrieve data from the specified table.

## Docker Support

This project also supports Docker for easier deployment and testing. To use Docker:

1. Ensure Docker and Docker Compose are installed on your system.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

This will start both the PostgreSQL database and the application in separate containers.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


"""Generate sample Excel data files for the RAG system."""

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

# Seed for reproducibility
random.seed(42)

DATA_DIR = Path(__file__).parent.parent / "data"


def generate_clients() -> pd.DataFrame:
    """Generate sample client data."""
    clients = [
        {
            "client_id": "C001",
            "name": "Acme Corp",
            "industry": "Technology",
            "country": "UK",
            "contact_email": "contact@acmecorp.com",
        },
        {
            "client_id": "C002",
            "name": "Bright Legal",
            "industry": "Legal Services",
            "country": "UK",
            "contact_email": "info@brightlegal.co.uk",
        },
        {
            "client_id": "C003",
            "name": "Global Finance Ltd",
            "industry": "Finance",
            "country": "US",
            "contact_email": "contact@globalfinance.com",
        },
        {
            "client_id": "C004",
            "name": "Tech Innovations GmbH",
            "industry": "Technology",
            "country": "Germany",
            "contact_email": "info@techinnovations.de",
        },
        {
            "client_id": "C005",
            "name": "Paris Consulting",
            "industry": "Consulting",
            "country": "France",
            "contact_email": "contact@parisconsulting.fr",
        },
        {
            "client_id": "C006",
            "name": "Nordic Solutions",
            "industry": "Technology",
            "country": "Sweden",
            "contact_email": "info@nordicsolutions.se",
        },
        {
            "client_id": "C007",
            "name": "Madrid Partners",
            "industry": "Legal Services",
            "country": "Spain",
            "contact_email": "contact@madridpartners.es",
        },
        {
            "client_id": "C008",
            "name": "Sydney Enterprises",
            "industry": "Manufacturing",
            "country": "Australia",
            "contact_email": "info@sydneyent.com.au",
        },
        {
            "client_id": "C009",
            "name": "Tokyo Tech",
            "industry": "Technology",
            "country": "Japan",
            "contact_email": "contact@tokyotech.jp",
        },
        {
            "client_id": "C010",
            "name": "Amsterdam Analytics",
            "industry": "Consulting",
            "country": "Netherlands",
            "contact_email": "info@amsterdamanalytics.nl",
        },
    ]
    return pd.DataFrame(clients)


def generate_invoices(clients_df: pd.DataFrame) -> pd.DataFrame:
    """Generate sample invoice data."""
    invoices = []
    invoice_id = 1001

    # Generate invoices throughout 2024
    client_ids = clients_df["client_id"].tolist()
    currencies = {
        "UK": "GBP",
        "US": "USD",
        "Germany": "EUR",
        "France": "EUR",
        "Sweden": "SEK",
        "Spain": "EUR",
        "Australia": "AUD",
        "Japan": "JPY",
        "Netherlands": "EUR",
    }

    client_countries = dict(zip(clients_df["client_id"], clients_df["country"], strict=True))

    # Generate 30+ invoices across 2024
    for month in range(1, 13):
        # 2-4 invoices per month
        num_invoices = random.randint(2, 4)
        for _ in range(num_invoices):
            client_id = random.choice(client_ids)
            country = client_countries[client_id]
            currency = currencies.get(country, "USD")

            # Random day in the month
            day = random.randint(1, 28)
            invoice_date = date(2024, month, day)
            due_date = invoice_date + timedelta(days=30)

            # Determine status based on date and randomness
            if due_date < date(2024, 12, 31):
                status = random.choice(["Paid", "Paid", "Paid", "Overdue"])
            else:
                status = random.choice(["Paid", "Pending", "Pending"])

            invoices.append(
                {
                    "invoice_id": f"I{invoice_id}",
                    "client_id": client_id,
                    "invoice_date": invoice_date,
                    "due_date": due_date,
                    "status": status,
                    "currency": currency,
                }
            )
            invoice_id += 1

    return pd.DataFrame(invoices)


def generate_line_items(invoices_df: pd.DataFrame) -> pd.DataFrame:
    """Generate sample line item data."""
    services = [
        ("Contract Review", 200.0, 350.0),
        ("Legal Consultation", 150.0, 300.0),
        ("Document Drafting", 100.0, 250.0),
        ("Compliance Audit", 300.0, 500.0),
        ("IP Assessment", 250.0, 400.0),
        ("Due Diligence", 350.0, 600.0),
        ("Litigation Support", 400.0, 700.0),
        ("Tax Advisory", 200.0, 400.0),
    ]

    tax_rates = [0.0, 0.10, 0.15, 0.20, 0.21, 0.25]

    line_items = []
    line_item_id = 1

    for _, invoice in invoices_df.iterrows():
        # 1-5 line items per invoice
        num_items = random.randint(1, 5)
        selected_services = random.sample(services, min(num_items, len(services)))

        for service_name, min_price, max_price in selected_services:
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(min_price, max_price), 2)
            tax_rate = random.choice(tax_rates)

            line_items.append(
                {
                    "line_item_id": f"L{line_item_id:04d}",
                    "invoice_id": invoice["invoice_id"],
                    "service_name": service_name,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "tax_rate": tax_rate,
                }
            )
            line_item_id += 1

    return pd.DataFrame(line_items)


def main():
    """Generate all sample data files."""
    DATA_DIR.mkdir(exist_ok=True)

    print("Generating sample data...")

    # Generate data
    clients_df = generate_clients()
    invoices_df = generate_invoices(clients_df)
    line_items_df = generate_line_items(invoices_df)

    # Save to Excel
    clients_df.to_excel(DATA_DIR / "Clients.xlsx", index=False)
    invoices_df.to_excel(DATA_DIR / "Invoices.xlsx", index=False)
    line_items_df.to_excel(DATA_DIR / "InvoiceLineItems.xlsx", index=False)

    print(f"Generated {len(clients_df)} clients")
    print(f"Generated {len(invoices_df)} invoices")
    print(f"Generated {len(line_items_df)} line items")
    print(f"Data saved to {DATA_DIR}")


if __name__ == "__main__":
    main()

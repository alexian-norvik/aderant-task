# Test Results

Results from running the sample questions through the RAG pipeline.

| Question | Answer |
|----------|--------|
| List all clients with their industries. | *To be filled after testing* |
| Which clients are based in the UK? | *To be filled after testing* |
| List all invoices issued in March 2024 with their statuses. | *To be filled after testing* |
| Which invoices are currently marked as "Overdue"? | *To be filled after testing* |
| For each service_name in InvoiceLineItems, how many line items are there? | *To be filled after testing* |
| List all invoices for Acme Corp with their invoice IDs, invoice dates, due dates, and statuses. | *To be filled after testing* |
| Show all invoices issued to Bright Legal in February 2024, including their status and currency. | *To be filled after testing* |
| For invoice I1001, list all line items with service name, quantity, unit price, tax rate, and compute the line total (including tax) for each. | *To be filled after testing* |
| For each client, compute the total amount billed in 2024 (including tax) across all their invoices. | *To be filled after testing* |
| Which client has the highest total billed amount in 2024, and what is that total? | *To be filled after testing* |

## Optional Questions

| Question | Answer |
|----------|--------|
| Across all clients, which three services generated the most revenue in 2024? | *To be filled after testing* |
| Which invoices are overdue as of 2024-12-31? | *To be filled after testing* |
| Group revenue by client country: for each country, compute the total billed amount in 2024 (including tax). | *To be filled after testing* |
| For the service "Contract Review", list all clients who purchased it and the total amount they paid. | *To be filled after testing* |
| Considering only European clients, what are the top 3 services by total revenue in H2 2024? | *To be filled after testing* |

---

*Note: Run `uv run streamlit run app.py` and test each question to fill in the answers.*

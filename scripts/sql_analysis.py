import pandas as pd
import sqlite3

# 1. Φόρτωση του αρχείου
df = pd.read_excel('sales_enriched.xlsx')

# 2. Δημιουργία σύνδεσης με SQL βάση στη μνήμη
conn = sqlite3.connect(':memory:')

# 3. Μεταφορά των δεδομένων από το Pandas στην SQL
df.to_sql('sales', conn, index=False, if_exists='replace')

# Ποια πόλη φέρνει το μεγαλύτερο ΚΑΘΑΡΟ ΚΕΡΔΟΣ (Net Profit);
query = """
SELECT 
    city, 
    SUM(net_profit) as total_profit,
    AVG(reward_points) as avg_points
FROM sales
GROUP BY city
ORDER BY total_profit DESC;
"""

result = pd.read_sql_query(query, conn)
print("--- Ανάλυση Κέρδους ανά Πόλη ---")
print(result)

# Η επίδραση των Προσφορών (Promotions)
query_promo = """
SELECT 
    is_promotion,
    COUNT(*) as total_orders,
    AVG(net_profit) as avg_profit_per_order
FROM sales
GROUP BY is_promotion;
"""

result_promo = pd.read_sql_query(query_promo, conn)
print("\n--- Απόδοση Προσφορών ---")
print(result_promo)
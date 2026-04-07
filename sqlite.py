from webscrapping import scrap, extract_max_price, clean_search_text, get_connection


def handle_sql_query(query):
    """Handle product search queries"""

    try:
        max_price = extract_max_price(query)
        search_text = clean_search_text(query)

        products_found = scrap(search_text, max_price=max_price, pages=2)

        if products_found == 0:
            if max_price:
                return f" No products found for {search_text} under ₹{max_price}. Try raising the budget or using different keywords!"
            return f" No products found for {search_text}. Try different keywords!"

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT name, price, url FROM products LIMIT 10")
        results = c.fetchall()
        conn.close()

        response = f" HERE ARE THE RESULTS FOR {search_text}:\n\n"
        for name, price, url in results:
            response += f"**{name}**\n- Price: ₹{price}\n-  [View Product]({url})\n\n"

        return response

    except Exception as e:
        return f" Error searching products: {str(e)}\nPlease try again with different keywords."
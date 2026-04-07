# 🛍️ E-commerce Chatbot

An intelligent chatbot for e-commerce platforms that helps users with product searches and answers frequently asked questions using RAG (Retrieval Augmented Generation) and web scraping.

## 🌟 Features

- **Smart Query Routing**: Automatically detects whether user wants product search or FAQ
- **Product Search**: Real-time product search from Flipkart with price filtering
- **FAQ System**: Answers policy questions using RAG with ChromaDB and Groq LLM
- **Interactive UI**: Built with Streamlit for easy conversation

## 🛠️ Technologies Used

- **Python 3.10+**
- **Streamlit** - Web interface
- **ChromaDB** - Vector database for FAQ retrieval
- **Groq API** - LLM for generating answers
- **BeautifulSoup4** - Web scraping
- **Semantic Router** - Intent classification
- **SQLite** - Product storage

## 📁 Project Structure

```
ecommerce-chatbot/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and paths
├── faq.py                 # FAQ handling with RAG
├── sqlite.py              # Product search handler
├── webscrapping.py        # Flipkart web scraper
├── router.py              # Query routing logic
├── data/
│   ├── faq.csv           # FAQ questions and answers
│   └── products.db       # SQLite database (auto-created)
├── .env                   # Environment variables
└── pyproject.toml        # Dependencies
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ecommerce-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
Or if using `uv`:
```bash
uv sync
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com

4. **Prepare FAQ data**

Make sure `data/faq.csv` exists with your FAQ content.

## 💻 Usage

Run the chatbot:
```bash
streamlit run app.py
```

Or with `uv`:
```bash
uv run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📝 Example Queries

**Product Search:**
- "laptops under 50000"
- "bellavita perfume"
- "gaming keyboards under 3000"

**FAQ Questions:**
- "What is your return policy?"
- "How can I track my order?"
- "Do you offer cash on delivery?"

## 🎯 How It Works

1. **Query Routing**: Semantic Router classifies user query as either "faq" or "sql"
2. **FAQ Path**: 
   - Searches ChromaDB for similar questions
   - Retrieves relevant answers
   - Uses Groq LLM to generate natural response
3. **Product Search Path**:
   - Scrapes Flipkart for products
   - Filters by price if specified
   - Stores in SQLite and displays results

## ⚠️ Important Notes

- Web scraping may violate Flipkart's terms of service
- This is a learning project - use official APIs in production
- Requires active internet connection for product search
- FAQ data needs to be updated regularly for accuracy

## 🔮 Future Improvements

- [ ] Add more e-commerce platforms
- [ ] Implement caching for faster responses
- [ ] Add user authentication
- [ ] Include product recommendations
- [ ] Add order tracking integration
- [ ] Multi-language support

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📧 Contact

Abhijith J- abhijithj2811@gmail.com

Project Link: https://github.com/abhijithj12/E-commerce-Chatbot

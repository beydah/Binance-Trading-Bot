# Installation Guide

## Prerequisites

-   **Python 3.10+**: Ensure Python is installed and added to your PATH.
-   **Binance Account**: You need an account with API keys enabled for **Spot & Margin Trading**.
-   **Telegram Account**: You need a Bot Token (from @BotFather) and your User ID (from @userinfobot).

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/beydah/Binance-Trading-Bot.git
cd Binance-Trading-Bot
```

### 2. Set Up Virtual Environment (Recommended)

Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    # On Windows: copy .env.example .env
    ```

2.  Open `.env` in a text editor and fill in your details:
    ```ini
    BINANCE_KEY=your_binance_api_key
    BINANCE_SECRET=your_binance_secret_key
    TELEGRAM_TOKEN=your_telegram_bot_token
    TELEGRAM_USER_ID=your_telegram_user_id
    ```

### 5. Verify Installation

Run the bot to check if it connects successfully:

```bash
python src/main.py
```

If successful, you should see a "Trade Bot Start" message in your Telegram.

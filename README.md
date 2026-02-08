# SkyShare

<div align="center">
  <img src="Images\SkyShare1.png" alt="SkyShare Dashboard" width="100%" />
</div>

## Share Files Instantly, Securely, and Without Friction.

**SkyShare** is a next-generation file-sharing platform designed for the modern web. Built with **Django**, it eliminates the barriers of traditional file sharing—no accounts, no complex permissions, just a secure 6-digit code. Whether you're a developer transferring code snippets or a designer sharing assets, SkyShare offers an **instant**, **anonymous**, and **ephemeral** way to move data.

---

## 🚀 Key Features

-   **Anonymous Sharing**: Upload files instantly without creating an account or logging in.
-   **6-Digit Secure Codes**: Every upload generates a unique, short 6-digit code for easy sharing.
-   **Automatic Expiration**: Files are automatically deleted after **7 days**, ensuring your data doesn't linger online.
-   **Responsive & Modern UI**: A clean, "Inter"-font based interface that works perfectly on desktop and mobile.
-   **Real-time Progress**: Visual upload progress bars for a seamless user experience.
-   **Secure Downloads**: Force-download headers ensure files are saved correctly, not just opened in the browser.
-   **Authentication System**: Optional user accounts with email verification and password reset for managing uploads (future-proofing).

---

## 🛠 Tech Stack

-   **Backend**: Python, Django 5.1
-   **Database**: SQLite (Development) / PostgreSQL (Production ready)
-   **Frontend**: HTML5, CSS3 (Custom Variables), JavaScript (Vanilla)
-   **Styling**: Custom CSS with a focus on Glassmorphism and Gradients
-   **Fonts**: Inter (Google Fonts)

---

## 🔍 Technical Deep Dive

### 1. The 6-Digit Code Generation Logic
At the heart of SkyShare is the `FileTransfer` model. We strictly avoid long, ugly URLs. Instead, we use a custom save method to generate a unique 6-digit numerical code for every file.

```python
# transfers/models.py

def save(self, *args, **kwargs):
    if not self.code:
        while True:
            # Generate a random 6-digit code
            code = ''.join(random.choices(string.digits, k=6))
            # Ensure uniqueness
            if not FileTransfer.objects.filter(code=code).exists():
                self.code = code
                break
    super().save(*args, **kwargs)
```

This ensures that every file is easily accessible via a simple code like `123456`, while maintaining a collision-free namespace.

### 2. Smart Expiration & Cleanup
Security and storage management are automated. Every file is assigned an `expires_at` timestamp upon creation (defaulting to 7 days).

```python
# transfers/models.py

if not self.expires_at:
    self.expires_at = timezone.now() + timedelta(days=7)
```

The `is_expired()` checks against the current server time to prevent access to stale files, and a background task (or cron job) can be set up to physically delete these files to free up space.

---

## 📸 Visuals

| Upload Page | Download Page |
| :---: | :---: |
| <img src="Images\SkyShare2.png" alt="Upload Page" /> | <img src="Images\SkyShare3.png" /> |

---

## ⚡ Installation

Get SkyShare running locally in minutes.

### Prerequisites
-   Python 3.10+
-   pip

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/SkyShare.git
    cd SkyShare
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

6.  **Access the App**
    Open your browser and navigate to `http://127.0.0.1:8000`.



# 🏠 UK Real Estate Scraper (Technical Challenge)

![License](https://img.shields.io/badge/License-MIT-green)
![Repo Size](https://img.shields.io/github/repo-size/reory/UK-Real-Estate-Scraper?cacheSeconds=60)
![Last Commit](https://img.shields.io/github/last-commit/reory/UK-Real-Estate-Scraper?cacheSeconds=60)

<p align="center">

  <!-- Core Language -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />

  <!-- Web Scraping & Automation -->
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" />
  <img src="https://img.shields.io/badge/BeautifulSoup-4B8BBE?style=for-the-badge&logo=python&logoColor=white" />

  <!-- Data Validation -->
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white" />

</p>

## 🎯 Project Overview
A specialized web scraping tool built to extract property data from highly secured UK real estate platforms. This project was a deep dive into bypassing modern anti-bot measures and handling dynamic JavaScript rendering using browser automation.

## 🛠️ Tech Stack
* **Language:** Python 3.13.7
* **Automation:** Selenium WebDriver
* **Parsing:** BeautifulSoup4 (lxml)
* **Environment:** Virtual Environments (venv)

---

<details>
  <summary>🚀 The Journey: Overcoming Technical Hurdles</summary>
  
This project was significantly more challenging than any other standard scraping tasks due to the target's security layers. It was rewarding to finally get some data.

### The Scrapy vs. JS Wall
Initially attempted using **Scrapy**, which failed to capture data because the property listings were injected via Asynchronous JavaScript. The site returned a 200 OK but with a nearly empty HTML body (4KB).

### Selenium Pivot
Switched to **Selenium** to simulate a real user environment. 
* **Custom Binary Pathing:** Configured the script to point directly to the Chrome binary to resolve environment-specific conflicts.
* **Stealth Configuration:** Implemented `AutomationControlled` flags and custom User-Agents to reduce the bot fingerprint.

### Handling Dynamic Content
* **Explicit Waits:** Used `WebDriverWait` to ensure elements were present before extraction.
* **Scroll-to-View:** Implemented a JavaScript scroll trigger to bypass "lazy-loading" mechanisms that hide property data until user interaction is detected.

### Bypassing Interstitials
Handled complex cookie consent banners that visually obstructed the data layer, using XPath selectors to clear the UI "fog."

## 📊 Data Output
The scraper successfully extracted property titles and pricing into a structured JSON format: Below is one of them.

```json
[
    {
        "title": "Church Gate",
        "price": "£290,000"
    }
]
```

</details>

---

## ⚙️ Prerequisites

Before running the scraper, ensure you have the following installed:

1. **Google Chrome**: This scraper uses the Chrome browser to render JavaScript. [Download Google Chrome here](https://www.google.com/chrome/).
2. **Python 3.10+**: Developed and tested on Python 3.13.7.
3. **Chrome Driver**: Automatically managed via `webdriver-manager`, but requires Chrome to be installed in the default system path.

---

## 🚀 How to Run

1. **Clone the repository**:
```bash
git clone [https://github.com/yourusername/real_estate_web_scraper.git](https://github.com/reory/real_estate_web_scraper.git)
cd real_estate_web_scraper
```

---

2. **set up virtual environment**
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
```

---

2. **Install dependences**
```bash
pip install selenium beautifulsoup4 lxml webdriver-manager
```

---

3. **Configuration**:

Open crack_uk_property.py and ensure the chrome_options.binary_location points 
to your chrome.exe

---

4. **Execute the scraper**:
python crack_uk_property.py

---

## 🛡️Ethical Note
To ensure compliance with the target's Terms of Service and to prevent IP blacklisting, the project was concluded once the Proof of Concept (PoC) was achieved. Extensive crawling was intentionally avoided to respect server resources.

---

## 📈 Key Learnings
Difference between static HTML scraping and dynamic DOM interaction.

Debugging Selenium TimeoutExceptions.

Managing Python virtual environments and interpreter paths in VS Code

---

## 🛠️ Detailed Tech Stack Logic
* **Selenium & WebDriver-Manager**: Leveraged for browser automation to handle dynamic DOM updates and JavaScript execution.
* **BeautifulSoup4 (lxml)**: Utilized for high-speed parsing of rendered HTML strings.
* **Pydantic Models**: (Planned/Implemented) For strict data typing and validation of scraped property objects.
* **Loguru/Logging**: For real-time monitoring of scraper health and error tracking.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

---
<details>
  <summary>📢 Potential Improvements</summary>

Since this project was a Proof of Concept (PoC), there are several areas for growth:
* **Pagination Logic**: Automating the "Next" button click to crawl multiple pages.
* **Data Cleaning**: Implementing Pydantic models to cast prices as integers and validate addresses.
* **Headless Mode**: Optimizing the Selenium configuration to run without a visible browser window.
* **Proxy Integration**: Adding rotating proxies to further reduce the risk of IP rate-limiting.
* **Integration**: Adding Playwright - behaves like a real user and can scrape more
effectively.

</details>

---

<details>
  <summary>💖 Acknowledgments</summary>

* **Future Contributors**: A huge thank you in advance to anyone who forks this repo. Your insights help turn small scripts into robust tools.
* **The Real Estate Tech Community**: Gratitude for the documentation and forums that help navigate the complex landscape of property data.
* **Open Source Community**: For providing powerful tools like Selenium and BeautifulSoup that make "cracking" these challenges possible.

</details>

---

* **NOTE**: This project was built for educational purposes to demonstrate advanced web automation techniques. Respect robots.txt and stay ethical!* ✌️

**Built By Roy Peters** [Click here for contact details 😁](https://www.linkedin.com/in/roy-p-74980b382/)

# Sales App Project Report

## 1. Introduction

The Sales App is a small web application designed to help shop owners record and monitor daily sales. The application allows a user to enter a product name, quantity, and price. It calculates the value of each sale, displays the day's transactions, and provides summary information such as total sales, number of transactions, total units sold, and the best-selling product. Users can also edit or delete individual records, reset the day's transactions, and download an HTML report.

The project was developed with Python and Flask for the backend, HTML and JavaScript for the user interface, CSS for presentation, and JSON for simple file-based data storage. It was also prepared for deployment using GitHub and Render.

## 2. Steps Followed to Develop the Application

### Planning the application

The first step was identifying the main problem to solve: small businesses need a simple way to record sales without relying on paper records or complicated business software. The essential data for each transaction was identified as the product name, quantity, price, calculated total, and an ID. The application was planned around a single daily sales page so that the main workflow would remain easy to understand.

### Creating the Flask application

A Flask application was created in `app.py`. Flask was selected because it is a lightweight Python web framework and is suitable for learning how web applications work. The application creates a Flask instance and defines routes for the main page, adding sales, deleting sales, editing sales, resetting the list, viewing summary data, and downloading a report.

The root route, `/`, loads the sales page. The `/add` route receives form data and creates a new sale record. The `/edit/<sale_id>` route updates an existing record, while `/delete/<sale_id>` removes a record. The `/api/summary` route returns summary information in JSON format, and `/api/report` creates an HTML report that the user can download. A `PORT` environment variable is also used when the application is started directly, allowing it to work both locally and on a hosting platform.

### Designing the data structure

Each sale is stored as a Python dictionary. For example, a record contains an `id`, `product`, `quantity`, `price`, and `total`. All records are stored in a Python list. This structure is simple but effective for a small demonstration application because it makes it easy to loop through transactions, calculate totals, and render table rows.

The list is saved to `sales_data.json` using Python's `json` module. A `load_sales()` function reads the file when the application starts, and a `save_sales()` function writes the current list after a sale is added, edited, deleted, or reset. Error handling was included when loading the file so that invalid or missing JSON data results in an empty list instead of stopping the application immediately.

### Implementing calculations and summaries

Separate functions were created for repeated calculations. `calculate_total()` multiplies the quantity by the price for one sale. `calculate_day_total()` adds the totals from all records. `summarize_sales()` calculates the number of transactions, total units, total sales, and best-selling item. Keeping these calculations in functions makes the program easier to read, test, and maintain.

The best-selling product is found by creating a dictionary of product names and accumulating the number of units sold for each product. The product with the highest quantity is selected and displayed in the summary cards on the page.

### Building the user interface

The interface was created in `templates/index.html`. It contains a form for entering sales, summary cards, an HTML report button, a reset button, and a table for displaying the day's records. JavaScript updates the table and summary information in the browser, validates user input, and supports inline editing and deletion.

The stylesheet in `static/style.css` provides the application's visual design. The page includes responsive layout rules so that the form, summary cards, and table remain usable on smaller screens. Icons and visual states are used to make actions such as adding, editing, saving, cancelling, and deleting records easier to identify.

### Testing the application locally

The application was tested by starting it with Python and opening the local address in a browser. The main page and summary endpoint were also tested with Flask's test client. Additional checks confirmed that adding a transaction, calculating totals, editing a record, deleting a record, resetting the day, and generating the report worked as expected. Python compilation was used to detect syntax errors before deployment.

### Preparing for deployment

The project was uploaded to GitHub and configured for Render. A `requirements.txt` file lists Flask and Gunicorn. The `Procfile` tells Render how to start the application:

```text
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

The `--bind` option is important because Render provides the port through the `PORT` environment variable and checks whether the application is listening on that port. The Python version was also specified using `runtime.txt` and `.python-version`.

During deployment troubleshooting, several issues were found. Some deployment files had been saved in UTF-16 encoding, which caused parsing and application-import problems. They were converted to normal UTF-8 text. An older Gunicorn version also attempted to import the removed `pkg_resources` module, so Gunicorn was upgraded to a newer compatible version. Finally, the Render root directory and start command had to point to the repository root, where `app.py` is located.

## 3. Python Concepts Used

The project demonstrates several important Python concepts:

- **Variables and data types:** Strings store product names, integers store quantities and IDs, and floating-point numbers store prices and totals.
- **Lists:** The `sales` list stores all transaction dictionaries.
- **Dictionaries:** Each sale is represented by key-value pairs, and another dictionary is used to total units for each product.
- **Functions:** Functions such as `load_sales()`, `save_sales()`, `calculate_total()`, and `summarize_sales()` divide the program into reusable parts.
- **Conditional statements:** `if` statements validate input, handle empty lists, and respond to missing or invalid data.
- **Loops:** `for` loops process sales records when calculating totals, generating report rows, and finding the best-selling product.
- **Exception handling:** `try` and `except` blocks handle invalid numeric input, malformed JSON, and file errors.
- **File handling:** The `pathlib` module is used to locate the JSON file, while the `json` module reads and writes structured data.
- **List comprehensions and generator expressions:** These are used to filter records and calculate totals in a concise way.
- **Modules and libraries:** The application imports Python's standard library modules and Flask components for routing, templates, forms, JSON responses, and HTTP responses.
- **Environment variables:** The `PORT` variable allows the same application to run on different systems and hosting platforms.

## 4. Reflection

This project taught me how Python can be used beyond simple console programs to create a complete web application. I learned that a web application has several connected parts: the backend receives requests and performs calculations, the frontend collects input and displays results, and a storage method preserves information. Flask helped me understand how URLs are connected to Python functions through routes and how HTML templates are returned to a browser.

The assignment improved my understanding of Python because I had to apply basic concepts in a practical situation. Lists and dictionaries became more meaningful when they represented real sales records. Functions helped me organize the application into smaller sections instead of putting every instruction in one large block. I also gained experience with conditions, loops, exception handling, file operations, and JSON serialization. Input validation showed me why programs must not assume that users will always enter correct data. For example, quantity and price need to be converted from form strings into numbers before calculations can be performed.

I also learned that web development includes more than writing application code. Testing the routes helped me find problems before deployment. Preparing the project for Render introduced me to dependency files, Gunicorn, environment variables, ports, GitHub commits, and deployment logs. The deployment errors were useful because they showed how file encoding, package compatibility, and an incorrect working directory can prevent a correct-looking application from starting. Solving those errors improved my debugging skills and taught me to read logs carefully instead of guessing.

This type of application could benefit small businesses by giving them a quick and affordable way to track daily transactions. A shop owner could see total revenue, the number of items sold, and which products are most popular. This information could support decisions about restocking, pricing, and planning. A digital record can also be easier to search and summarize than handwritten notes. The current version is suitable as a simple prototype; a production version could be improved with user accounts, a real database, backups, reports by date, authentication, and stronger validation. Overall, the project showed me how Python fundamentals can be combined with web technologies to solve a practical business problem.

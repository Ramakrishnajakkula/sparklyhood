# HumanChain AI Safety Incident Log API

## Setup & Run Instructions (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ramakrishnajakkula/sparklyhood.git
   cd sparklyhood
   ```

2. **Install dependencies**  
   Make sure you have Python 3.8+ installed.  
   In your project directory, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   Create a `.env` file in the project root with your MongoDB URI:

   ```
   MONGODB_URI="your-mongodb-uri-here"
   ```

   (Replace with your actual URI.)

4. **Run the Flask app**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`.

## Deployed in Vercel

1. **You can access through this link**

   ```https://sparklyhood.vercel.app/
   ```


## API Endpoints

- `GET /incidents` — List all incidents
- `POST /incidents` — Create a new incident
- `GET /incidents/<id>` — Get incident by ID
- `DELETE /incidents/<id>` — Delete incident by ID

## How to Test All Endpoints

You can verify that all endpoints are working correctly by running the automated test suite:

1. **Install test dependencies** (if not already):

   ```bash
   pip install pytest
   ```

2. **Run the tests**:
   ```bash
   pytest test_app.py
   ```

If all tests pass, all endpoints and edge cases are working as expected.

## Notes

- All requests/responses use JSON.
- See code comments for more details.
- For deployment, ensure your `vercel.json` and `requirements.txt` are correct and do not include the `bson` package.

# sparklyhood

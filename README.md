# ChavrutAI - Sefaria Text Formatter

A web application for retrieving Talmud from Sefaria with custom formatting options for scholarly and educational use. This tool helps you quickly access Talmud text and format it for seamless integration into documents, presentations, and study materials.

## Features

- **Clean text formatting** for Google Docs and other word processors
- **Split into lines** based on punctuation (period, colon, question mark, exclamation point [.:?!])
- **Generate numbered section headers**
- **Remove nikud** (Hebrew vowel marks) while preserving punctuation
- **Standardize terminology** according to scholarly preferences
- **Convert spelled-out numbers** to Arabic numerals for numbers above ten
- **Copy-paste ready output** with consistent font styling

## Usage

Visit [https://chavrutai.com](https://chavrutai.com) to use the application online.

## Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.9 or higher (if running without Docker)

### Running with Docker
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/chavrutai-app.git
   cd chavrutai-app
   ```

2. Build and run the application with Docker Compose:
   ```
   docker-compose up --build
   ```

3. Access the application at [http://localhost:8080](http://localhost:8080)

### Running without Docker
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/chavrutai-app.git
   cd chavrutai-app
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```
   flask run
   ```

4. Access the application at [http://localhost:5000](http://localhost:5000)

## Terminology Preferences

The tool standardizes terminology according to these preferences:

| Original Term | Preferred Term |
|---------------|----------------|
| Gemara | Talmud |
| Rabbi | R' |
| The Sages taught | A baraita states |
| Divine Voice | bat kol |
| Divine Presence | Shekhina |
| divine inspiration | Holy Spirit |
| the Lord | YHWH |
| leper | metzora |
| leprosy | tzara'at |
| phylacteries | tefillin |
| gentile | non-Jew |
| ignoramus | am ha'aretz |
| maidservant | female slave |
| barrel | jug |

You can customize the terminology preferences in `utils/formatter.py`.

## Deployment

The application can be deployed to various platforms:

### GitHub Pages (Static Frontend Only)
If you want to deploy just the frontend and have the API hosted elsewhere:

1. Create a static version of the frontend
2. Deploy to GitHub Pages

### Cloud Platforms
The Docker container can be deployed to:
- Google Cloud Run
- AWS Elastic Container Service
- Azure Container Instances
- Heroku

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Sefaria](https://www.sefaria.org/) for their incredible digital library and API

---

*This project is not officially affiliated with Sefaria. It is an independent tool that utilizes the Sefaria API.*
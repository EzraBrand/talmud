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

Visit [https://chavrutai.com](https://chavrutai.com) to use the application online. (Work in progress, currently only placeholder)

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

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Sefaria](https://www.sefaria.org/) for their incredible digital library and API

---

*This project is not officially affiliated with Sefaria. It is an independent tool that utilizes the Sefaria API.*

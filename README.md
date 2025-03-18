# Sefaria Talmud Text Formatter

A Python tool for retrieving Talmud from Sefaria with custom formatting options for scholarly and educational use. This tool helps you quickly access Talmud text and format it for seamless integration into documents, presentations, and study materials.

## Features

- **Clean text formatting** for Google Docs and other word processors
- **Remove nikud** (Hebrew vowel marks) while preserving punctuation
- **Standardize terminology** according to scholarly preferences
- **Convert spelled-out numbers** to Arabic numerals for numbers above ten
- **GUI interface** via Google Colab notebook
- **Copy-paste ready output** with consistent font styling

## Usage

The easiest way to use this tool is through the Google Colab notebook:

1. Open the [Sefaria Text Formatter Notebook](https://github.com/EzraBrand/talmud/blob/main/Custom_Formatter_of_Sefaria_Talmud_Text_Via_API.ipynb)
2. Run each cell in sequence
3. Use the form to enter a reference (e.g., "Sotah.35a")
4. Select your preferred options
5. Click "Get Text" to retrieve the formatted text
6. Copy and paste the result directly into your document


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
| the Lord | God |
| leper | metzora |
| leprosy | tzara'at |
| phylacteries | tefillin |
| gentile | non-Jew |
| ignoramus | am ha'aretz |
| maidservant | female slave |
| barrel | jug |

You can customize for your own custom terminology preferences in the notebook.

## Customization

The script can be customized in several ways:

1. **Terminology Preferences**: Edit the `TERMINOLOGY_PREFERENCES` dictionary
2. **Number Formatting**: Modify the `NUMBER_PATTERNS` dictionary
3. **Font and Styling**: Adjust the HTML formatting in `display_sefaria_text()`

## Project Background

This tool was created to solve the practical challenge of working with Sefaria texts in academic and educational contexts. It streamlines the process of retrieving, formatting, and preparing Jewish texts for documents, presentations, and study materials.

For more details, check out my upcoming blogpost at [my blog](https://www.ezrabrand.com/) explaining the development process and use cases.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Sefaria](https://www.sefaria.org/) for their incredible digital library and API
- [Google Colab](https://colab.research.google.com/) for making interactive Python notebooks accessible

## Contact

If you have any questions or suggestions, please open an issue or contact me at [ezrabrand@gmail.com].

---

*This project is not officially affiliated with Sefaria. It is an independent tool that utilizes the Sefaria API.*

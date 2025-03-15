# Sefaria Text Formatter

A Python tool for retrieving texts from Sefaria with custom formatting options for scholarly and educational use. This tool helps you quickly access Jewish texts and format them for seamless integration into documents, presentations, and study materials.

## Features

- **Clean text formatting** for Google Docs and other word processors
- **Remove nikud** (Hebrew vowel marks) while preserving punctuation
- **Standardize terminology** according to scholarly preferences
- **Convert spelled-out numbers** to Arabic numerals for numbers above ten
- **User-friendly interface** via Google Colab notebook
- **Copy-paste ready output** with consistent font styling

## Usage

The easiest way to use this tool is through the Google Colab notebook:

1. Open the [Sefaria Text Formatter Notebook](https://github.com/EzraBrand/talmud/blob/main/Custom_Formatter_of_Sefaria_Talmud_Text_Via_API.ipynb)
2. Run each cell in sequence
3. Use the form to enter a reference (e.g., "Sotah.35a.7")
4. Select your preferred options
5. Click "Get Text" to retrieve the formatted text
6. Copy and paste the result directly into your document

## Example References

- **Talmud**: Berakhot.2a.1, Sotah.35a.7, Sanhedrin.90b.3
- **Torah**: Genesis.1.1, Exodus.20.1, Leviticus.19.18
- **Prophets**: Isaiah.40.1, Jeremiah.29.11, Ezekiel.37.1
- **Writings**: Psalms.23.1, Proverbs.3.5, Job.1.1
- **Mishnah**: Avot.1.1, Berakhot.1.1, Sukkah.1.1

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

You can add your own custom terminology preferences using the form in the notebook.


## API Reference

### `get_sefaria_text()`

```python
get_sefaria_text(reference, language="all", context=1, 
                remove_nikud_marks=True, standardize_terms=True, silent=True)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `reference` | str | The text reference in the format "Book.Chapter.Verse" |
| `language` | str | Language code - "en" for English, "he" for Hebrew, "all" for both |
| `context` | int | Number of context verses to include |
| `remove_nikud_marks` | bool | Whether to remove nikud from Hebrew text |
| `standardize_terms` | bool | Whether to standardize terminology in English text |
| `silent` | bool | Whether to suppress output messages about querying the API |

Returns: `dict` - The JSON response from the Sefaria API

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Sefaria](https://www.sefaria.org/) for their incredible digital library and API
- [Google Colab](https://colab.research.google.com/) for making interactive Python notebooks accessible

## Contact

If you have any questions or suggestions, please open an issue or contact me at [ezrabrand@gmail.com].

---

*This project is not officially affiliated with Sefaria. It is an independent tool that utilizes the Sefaria API.*

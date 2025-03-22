document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const submitBtn = document.getElementById('submitBtn');
    const submitSpinner = document.getElementById('submitSpinner');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsContent = document.getElementById('resultsContent');
    const copyAllBtn = document.getElementById('copyAllBtn');
    const includeAdjacentCheckbox = document.getElementById('includeAdjacent');
    const adjacentPagesInput = document.getElementById('adjacentPages');

    // API URL - replace with your serverless function URL when deployed
    const API_URL = '/api/get_text';
    
    // Toggle adjacent pages input based on checkbox
    includeAdjacentCheckbox.addEventListener('change', function() {
        adjacentPagesInput.disabled = !this.checked;
        if (!this.checked) {
            adjacentPagesInput.value = 0;
        } else {
            adjacentPagesInput.value = 1;
        }
    });

    // Initialize - adjacent pages disabled by default
    adjacentPagesInput.disabled = !includeAdjacentCheckbox.checked;

    // Handle form submission
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        fetchText();
    });

    // Copy all text
    copyAllBtn.addEventListener('click', function() {
        const allText = resultsContent.innerText;
        navigator.clipboard.writeText(allText)
            .then(() => {
                showCopyFeedback(copyAllBtn);
            })
            .catch(err => {
                console.error('Failed to copy text:', err);
                alert('Failed to copy text. Please try selecting and copying manually.');
            });
    });

    // Handle section-specific copy buttons
    resultsContent.addEventListener('click', function(event) {
        if (event.target.classList.contains('copy-section-btn')) {
            const sectionId = event.target.getAttribute('data-section-id');
            const section = document.getElementById(sectionId);
            if (section) {
                const sectionText = section.innerText;
                navigator.clipboard.writeText(sectionText)
                    .then(() => {
                        showCopyFeedback(event.target);
                    })
                    .catch(err => {
                        console.error('Failed to copy section:', err);
                        alert('Failed to copy text. Please try selecting and copying manually.');
                    });
            }
        }
    });

    function showCopyFeedback(button) {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('btn-success');
        button.classList.remove('btn-outline-secondary');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('btn-success');
            button.classList.add('btn-outline-secondary');
        }, 2000);
    }

    function fetchText() {
        // Show loading state
        submitBtn.disabled = true;
        submitSpinner.classList.remove('d-none');
        resultsContent.innerHTML = `
            <div class="spinner-container">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <span class="ms-2">Loading text from Sefaria...</span>
            </div>
        `;
        resultsContainer.classList.remove('d-none');

        // Get form values
        const reference = document.getElementById('reference').value;
        const language = document.getElementById('language').value;
        const removeNikud = document.getElementById('removeNikud').checked;
        const standardizeTerms = document.getElementById('standardizeTerms').checked;
        const splitSentences = document.getElementById('splitSentences').checked;
        const includeAdjacent = document.getElementById('includeAdjacent').checked;
        const adjacentPages = includeAdjacent ? parseInt(document.getElementById('adjacentPages').value, 10) : 0;

        // Make API request to the serverless function
        fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                reference: reference,
                language: language,
                remove_nikud: removeNikud,
                standardize_terms: standardizeTerms,
                split_sentences: splitSentences,
                include_adjacent: includeAdjacent,
                adjacent_pages: adjacentPages
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Reset loading state
            submitBtn.disabled = false;
            submitSpinner.classList.add('d-none');

            // Display results or error
            if (data.success) {
                displayResults(data.content);
            } else {
                resultsContent.innerHTML = `
                    <div class="alert alert-danger">
                        Error: ${data.message || 'Failed to retrieve text from Sefaria.'}
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            submitBtn.disabled = false;
            submitSpinner.classList.add('d-none');
            resultsContent.innerHTML = `
                <div class="alert alert-danger">
                    Error: Failed to connect to the API. Please try again later.
                    <br><small>${error.message}</small>
                </div>
            `;
        });
    }

    function displayResults(content) {
        if (!content || content.length === 0) {
            resultsContent.innerHTML = `
                <div class="alert alert-warning">
                    No content found for the specified reference.
                </div>
            `;
            return;
        }

        let htmlContent = '';

        // Generate content for each page
        content.forEach((page, pageIndex) => {
            // Page title
            htmlContent += `
                <div class="page-section mb-4">
                    <h4 class="section-title">${page.title}</h4>
            `;

            // Add copy button for this page
            const pageId = `page-${pageIndex}`;
            htmlContent += `
                <div class="d-flex justify-content-end mb-2">
                    <button class="btn btn-sm btn-outline-secondary copy-section-btn" data-section-id="${pageId}">
                        Copy Page
                    </button>
                </div>
                <div id="${pageId}">
            `;

            // Process each section
            if (page.sections && page.sections.length > 0) {
                page.sections.forEach((section, sectionIndex) => {
                    htmlContent += `
                        <div class="text-section">
                            <h5>Section ${section.number}</h5>
                    `;

                    // Hebrew text
                    if (section.hebrew && section.hebrew.length > 0) {
                        htmlContent += '<div class="hebrew-text">';
                        section.hebrew.forEach(line => {
                            htmlContent += `<p>${line}</p>`;
                        });
                        htmlContent += '</div>';
                    }

                    // English text
                    if (section.english && section.english.length > 0) {
                        htmlContent += '<div class="english-text">';
                        section.english.forEach(line => {
                            htmlContent += `<p>${line}</p>`;
                        });
                        htmlContent += '</div>';
                    }

                    htmlContent += '</div>'; // Close text-section
                });
            } else {
                htmlContent += `
                    <div class="alert alert-info">
                        No sections found for this page.
                    </div>
                `;
            }

            htmlContent += '</div></div>'; // Close page-section and pageId div
        });

        resultsContent.innerHTML = htmlContent;
    }
});

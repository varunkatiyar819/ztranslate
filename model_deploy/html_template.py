def create_template():

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Translation App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            form {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
            }
            input[type="text"] {
                width: 100%;
                padding: 8px;
                margin-bottom: 10px;
            }
            input[type="submit"] {
                padding: 10px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            .response {
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>Translation App</h1>
        <form id="translationForm">
            <label for="sentence">Enter a corpus of data you want to translate</label>
            <textarea id="sentence" name="sentence" rows="20" style="width: 100%;" required></textarea>
            <input type="submit" value="Translate">
        </form>

        <div id="response" class="response" style="display:none;"></div>

        <script>
            document.getElementById('translationForm').addEventListener('submit', function(event) {
                event.preventDefault();
                const sentence = document.getElementById('sentence').value;
                fetch('/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ input: sentence })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("data = ", data)
                    const responseDiv = document.getElementById('response');
                    responseDiv.style.display = 'block';
                    if (data.message.status === 'success') {
                        let translationsHtml = '';

                        data.translations.forEach((pair) => {
                            translationsHtml += `<strong>Translation:</strong> {"source" : ${pair.source}, "translate" : ${pair.translation}}<br>`;
                        });

                        responseDiv.innerHTML = `
                            <strong>Status:</strong> ${data.message.status}<br>
                            <strong>Status_code:</strong> ${data.message.status_code}<br>
                            ${translationsHtml}
                        `;
                    

                    } else {
                        responseDiv.innerHTML = `<strong>Error:</strong> ${data.message}`;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    """

    return html_template

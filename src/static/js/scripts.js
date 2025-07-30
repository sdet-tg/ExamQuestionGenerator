document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("questionForm");
    const resultSection = document.getElementById("questionsList");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const className = document.getElementById("className").value;
        const topic = document.getElementById("topic").value;
        const gradeLevel = parseInt(document.getElementById("gradeLevel").value, 10);
        const numQuestions = parseInt(document.getElementById("numQuestions").value, 10);
        const difficulty = document.getElementById("difficulty").value;
        const aiModel = document.getElementById("aiModel").value;

        resultSection.innerHTML = "<p>Generating questions...</p>";

        fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                className: className,
                topic: topic,
                gradeLevel: gradeLevel,
                numQuestions: numQuestions,
                difficulty: difficulty,
                aiModel: aiModel,
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Server returned an error");
                }
                return response.json();
            })
            .then((data) => {
                resultSection.innerHTML = ""; // Clear previous results

                const header = document.createElement("div");
                header.classList.add("questions-header");
                header.innerHTML = `
                    <h2>${className} - ${topic} - Grade ${gradeLevel} ${difficulty}</h2>
                `;
                resultSection.appendChild(header);

                if (Array.isArray(data) && data.length > 0) {
                    data.forEach((item, index) => {
                        const container = document.createElement("div");
                        container.classList.add("question-section");

                        const questionBlock = document.createElement("div");
                        questionBlock.classList.add("question-block");

                        const qText = document.createElement("p");
                        qText.classList.add("question-title");
                        qText.innerHTML = `<strong>Q${index + 1}:</strong> ${item.question}`;
                        questionBlock.appendChild(qText);

                        if (item.type === "multiple_choice" && Array.isArray(item.options)) {
                            const optionsBlock = document.createElement("div");
                            optionsBlock.classList.add("options-section");

                            const ul = document.createElement("ul");
                            item.options.forEach((opt) => {
                                const li = document.createElement("li");
                                li.textContent = opt;
                                ul.appendChild(li);
                            });
                            optionsBlock.appendChild(ul);
                            questionBlock.appendChild(optionsBlock);
                        }

                        const answerBlock = document.createElement("div");
                        answerBlock.classList.add("answer-section");
                        const answer = document.createElement("p");
                        answer.classList.add("correct-answer");
                        answer.innerHTML = `<em>Correct Answer: ${item.correct_answer}</em>`;
                        answerBlock.appendChild(answer);

                        container.appendChild(questionBlock);
                        container.appendChild(answerBlock);
                        resultSection.appendChild(container);
                    });

                    // Add Print Button if not already present
                    if (!document.getElementById("printBtn")) {
                        const printBtn = document.createElement("button");
                        printBtn.id = "printBtn";
                        printBtn.textContent = "Print Questions";
                        printBtn.style.position = "fixed";
                        printBtn.style.left = "20px";
                        printBtn.style.bottom = "20px";
                        printBtn.addEventListener("click", () => {
                            const printContent = document.getElementById("questionsList").innerHTML;
                            const printWindow = window.open("", "_blank");
                            printWindow.document.write(`
                                <html>
                                    <head>
                                        <title>Print Questions</title>
                                        <style>
                                            body {
                                                font-family: Arial, sans-serif;
                                                padding: 20px;
                                            }
                                            .questionBlock {
                                                margin-bottom: 20px;
                                            }
                                            em {
                                                display: none; /* Hide answers */
                                            }
                                        </style>
                                    </head>
                                    <body>
                                        ${printContent}
                                        <script>
                                            window.onload = function() {
                                                window.print();
                                                window.onafterprint = function() { window.close(); };
                                            };
                                        </script>
                                    </body>
                                </html>
                            `);
                            printWindow.document.close();
                        });
                        document.body.appendChild(printBtn);
                    }

                    // Add Download as HTML Button if not already present
                    if (!document.getElementById("downloadHtmlBtn")) {
                        const downloadHtmlBtn = document.createElement("button");
                        downloadHtmlBtn.id = "downloadHtmlBtn";
                        downloadHtmlBtn.textContent = "Download Questions (HTML)";
                        downloadHtmlBtn.style.position = "fixed";
                        downloadHtmlBtn.style.right = "20px";
                        downloadHtmlBtn.style.bottom = "20px";
                        downloadHtmlBtn.addEventListener("click", () => {
                            const content = document.getElementById("questionsList").cloneNode(true); // Only clone this

                            // Remove answers if needed
                            content.querySelectorAll("em").forEach((em) => em.remove());

                            const htmlContent = `
                                <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>Questions</title>
                                    <style>
                                        body {
                                            font-family: Arial, sans-serif;
                                            margin: 20px;
                                        }
                                        .questionBlock {
                                            margin-bottom: 20px;
                                        }
                                    </style>
                                </head>
                                <body>
                                    ${content.innerHTML}
                                </body>
                                </html>
                            `;

                            const blob = new Blob([htmlContent], {
                                type: "text/html",
                            });

                            const url = URL.createObjectURL(blob);
                            const link = document.createElement("a");
                            link.href = url;
                            link.download = "questions.html";
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                            URL.revokeObjectURL(url);
                        });
                        document.body.appendChild(downloadHtmlBtn);
                    }
                } else {
                    resultSection.innerHTML = "<p>No questions generated. Please try again.</p>";
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                resultSection.innerHTML = "<p>An error occurred while generating questions. Please try again.</p>";
            });
    });
});
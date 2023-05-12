const addMarkdownButton = () => {
    console.log('addMarkdownButton()');
    const buttonArea = document.querySelector('div#title-container');
    const markdownButton = document.createElement('button');
    markdownButton.id = 'markdown-button';
    markdownButton.className = 'button';
    markdownButton.textContent = 'Copy Clip Links';
    markdownButton.style.backgroundColor = '#4CAF50';
    markdownButton.style.marginLeft = '3px';
    markdownButton.style.color = 'white';
    markdownButton.style.border = 'none';
    markdownButton.style.cursor = 'pointer';
    markdownButton.style.borderRadius = '5px';
    markdownButton.style.textAlign = 'center';
    markdownButton.style.textDecoration = 'none';
    markdownButton.style.display = 'inline-block';

    // add button to buttonArea
    buttonArea.appendChild(markdownButton);
}

function exportToMarkdown() {
    // Get all the checked checkboxes
    const checkedCheckboxes = Array.from(document.querySelectorAll('input.check-mark:checked'));
    
    // Process the checked clips and generate Markdown representation
    const markdownContent = checkedCheckboxes.map((checkbox) => {
        const thumbnail = checkbox.closest('a#thumbnail');
        const videoUrl = thumbnail.href;
        const clipTitle = thumbnail.getAttribute('aria-label');
        return videoUrl;
    }).join(' ');

    // Copy the generated Markdown content to the clipboard
    navigator.clipboard.writeText(markdownContent);
    
    // Perform your desired action with the generated Markdown content
    // For example, you can log it or copy it to the clipboard
    console.log(markdownContent);
    // ... other export logic ...
    
    // You can also open a new window with the generated Markdown content
    // for the user to save or copy it directly
    // window.open().document.write('<pre>' + markdownContent + '</pre>');
}

// Event listener for the export button
console.log("export.js loaded");
window.addEventListener("load", () => {
    setTimeout(function() {
        addMarkdownButton();
    }, 2000)
});

const exportButton = document.getElementById('markdwon-button');
window.addEventListener('click', function() {
    exportToMarkdown();
});
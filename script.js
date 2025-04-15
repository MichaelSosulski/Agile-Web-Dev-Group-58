function dropForm(formId) {
    const dropdown = document.getElementById(formId);

    
    document.querySelectorAll('.form-container').forEach(container => {
        if (container.id !== formId) {
            container.style.display = 'none';
        }
    });

    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

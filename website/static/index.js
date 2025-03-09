// Automatically hide alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.remove(); // Completely remove the alert from the DOM
    });
}, 5000); // Time in milliseconds



function handleAssign(button) {
    // Accessing attributes of the button using 'this'
    const teacherId = button.getAttribute('data-teacher-id');
    const subjectId = button.getAttribute('data-subject-id');
    
    // Logging or performing further actions
    console.log('Teacher ID:', teacherId);
    console.log('Subject ID:', subjectId);

    // Call your original function
    assignSubject(teacherId, subjectId);
}


function assignSubject(teacherId) {
    const subjectId = document.getElementById(`subject-${teacherId}`).value;
    if (!subjectId) {
        alert('Please select a subject.');
        return;
    }

    fetch('/assign_subject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ teacher_id: teacherId, subject_id: subjectId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                location.reload(); // Reload to reflect changes
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}


function handleUnassign(button) {
    const teacherId = button.getAttribute('data-teacher-id');
    const subjectId = button.getAttribute('data-subject-id');
    unassignSubject(teacherId, subjectId);
}


function unassignSubject(teacherId, subjectId) {
    fetch('/unassign_subject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ teacher_id: teacherId, subject_id: subjectId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                location.reload(); // Reload to reflect changes
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}



function confirmRemoveSub(subjectId) {
    var confirmation = confirm("Are you sure you want to remove this subject?");
    if (confirmation) {
        // If user confirms, submit the form
        document.getElementById('remove-form-' + subjectId).submit();
    }
}



function confirmRemoveUser(userId) {
    var confirmation = confirm("Are you sure you want to remove this teacher?");
    if (confirmation) {
        // If user confirms, submit the form
        document.getElementById('remove-form-' + userId).submit();
    }
}


document.addEventListener('DOMContentLoaded', function() {
    let moduleCount = 1;

    document.getElementById('add-module').addEventListener('click', function () {
        moduleCount++;

        console.log(`Adding module ${moduleCount}`); // Debugging

        // Clone the first module-group (initial template) to maintain the same structure
        const originalModuleGroup = document.querySelector('.module-group');
        const moduleGroup = originalModuleGroup.cloneNode(true);

        // Update the IDs and "for" attributes to make them unique
        const moduleSelect = moduleGroup.querySelector('select');
        const numQuestionsInput = moduleGroup.querySelector('input');
        const moduleLabel = moduleGroup.querySelector('label[for="module-1"]');
        const numQuestionsLabel = moduleGroup.querySelector('label[for="num_questions-1"]');
        const marksInput = moduleGroup.querySelector('input[name="module_max_marks[]"]'); // Corrected selector here
        const marksLabel = moduleGroup.querySelector('label[for="marks-1"]'); // Corrected selector here

        // Update the 'id' and 'for' attributes to be unique based on moduleCount
        moduleSelect.setAttribute('id', `module-${moduleCount}`);
        moduleSelect.setAttribute('name', 'modules[]');
        moduleSelect.querySelector('option').value = ''; // Reset default value

        numQuestionsInput.setAttribute('id', `num_questions-${moduleCount}`);
        numQuestionsInput.setAttribute('name', 'num_questions[]');
        numQuestionsInput.value = ''; // Reset the number of questions input value

        marksInput.setAttribute('id', `marks-${moduleCount}`);
        marksInput.setAttribute('name', 'module_max_marks[]');
        marksInput.value = ''; // Reset the marks input value

        // Update the labels to reference the new IDs
        moduleLabel.setAttribute('for', `module-${moduleCount}`);
        numQuestionsLabel.setAttribute('for', `num_questions-${moduleCount}`);
        marksLabel.setAttribute('for', `marks-${moduleCount}`);

        // Append the cloned module group to the module section
        document.getElementById('module-section').appendChild(moduleGroup);
    });
});





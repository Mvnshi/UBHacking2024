// Load notes from local storage or initialize an empty array
let notes = JSON.parse(localStorage.getItem('notes')) || [];
let editingIndex = null;

// Function to save or update a note
function saveOrUpdateNote() {
    const noteInput = document.getElementById('note-input').value.trim();
    if (!noteInput) {
        alert("Note cannot be empty!");
        return;
    }

    if (editingIndex !== null) {
        // Update existing note
        notes[editingIndex].content = noteInput;
        notes[editingIndex].keyTopics = extractKeyTopics(noteInput);
        editingIndex = null;
        document.getElementById('save-btn').textContent = 'Save Note';
    } else {
        // Add new note
        notes.push({
            content: noteInput,
            keyTopics: extractKeyTopics(noteInput)
        });
    }

    saveNotes();
    renderNotes();
    document.getElementById('note-input').value = ''; // Clear the input field
}

// Function to extract key topics from the note content
function extractKeyTopics(note) {
    const words = note.split(/\s+/);
    const keywordCounts = {};
    words.forEach(word => {
        word = word.toLowerCase().replace(/[^a-z]/g, ''); // Simple cleaning
        if (word && word.length > 3) {
            keywordCounts[word] = (keywordCounts[word] || 0) + 1;
        }
    });

    // Return the top 5 keywords
    return Object.entries(keywordCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(entry => entry[0]);
}

// Function to save notes to local storage
function saveNotes() {
    localStorage.setItem('notes', JSON.stringify(notes));
    console.log('Notes saved:', notes); // Debugging message
}

// Function to render notes
function renderNotes() {
    const notesList = document.getElementById('notes-list');
    notesList.innerHTML = ''; // Clear the current list

    if (notes.length === 0) {
        console.log('No notes to display'); // Debugging message
        return;
    }

    notes.forEach((note, index) => {
        const noteItem = document.createElement('li');
        noteItem.innerHTML = `
            <p>${note.content}</p>
            <small>Key Topics: ${note.keyTopics.join(', ')}</small>
            <button onclick="editNote(${index})">Edit</button>
            <button onclick="deleteNote(${index})">Delete</button>
        `;
        notesList.appendChild(noteItem);
    });

    console.log('Notes rendered:', notes); // Debugging message
}

// Function to edit a note
function editNote(index) {
    document.getElementById('note-input').value = notes[index].content;
    editingIndex = index;
    document.getElementById('save-btn').textContent = 'Update Note';
}

// Function to delete a note
function deleteNote(index) {
    notes.splice(index, 1);
    saveNotes();
    renderNotes();
}

// Initial render
renderNotes();

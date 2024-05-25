document.getElementById('search-button').addEventListener('click', async () => {
    const query = document.getElementById('search-input').value;
    const patientInfoContainer = document.getElementById('patient-info');

    // Clear previous search results
    patientInfoContainer.innerHTML = '';

    // Send search request to the server
    try {
        const response = await fetch(`/search_patient?name=${encodeURIComponent(query)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Server response:", data);

        // Display search results
        if (data.length === 0) {
            patientInfoContainer.textContent = 'No records found.';
        } else {
            data.forEach(record => {
                const recordElement = document.createElement('div');
                recordElement.className = 'patient-record';

                const detailsElement = document.createElement('div');
                detailsElement.className = 'patient-details';
                detailsElement.innerHTML = `Name: ${record.name}`;
                recordElement.appendChild(detailsElement);

                const ageElement = document.createElement('div');
                ageElement.className = 'patient-age';
                ageElement.innerHTML = `Age: ${record.age}`;
                recordElement.appendChild(ageElement);

                const conditionElement = document.createElement('div');
                conditionElement.className = 'patient-condition';
                conditionElement.innerHTML = `Condition: ${record.condition}`;
                recordElement.appendChild(conditionElement);

                patientInfoContainer.appendChild(recordElement);
            });
        }
    } catch (error) {
        console.error('Error:', error);
        patientInfoContainer.textContent = `Error: ${error.message}`;
    }
});

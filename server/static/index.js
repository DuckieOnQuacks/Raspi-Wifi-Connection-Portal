const networkStatusParagraph = document.getElementById('network-status'); // For status updates

// Handle network configuration submission
function submitNetworkConfig() {
    var ssid = document.getElementById('ssid').value;
    var password = document.getElementById('password').value;

    // Prepare data to send to the backend
    var networkConfig = {
        ssid: ssid,
        password: password
    };

    fetch('/api/connect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(networkConfig),
    })
    .then(response => {
        // Log the response status to see what error occurred
        console.log('Response status:', response.status);
        
        if (!response.ok) {  // Non-2xx status code
            throw new Error(`Network request failed with status ${response.status}`);
        }
        
        return response.json();
    })
    .then(result => {
        document.getElementById('network-status').innerText = 'Connected to network successfully!';
    })
    .catch(error => {
        document.getElementById('network-status').innerText = 'Failed to submit network configuration.';
        console.error('Error:', error);
    });
}

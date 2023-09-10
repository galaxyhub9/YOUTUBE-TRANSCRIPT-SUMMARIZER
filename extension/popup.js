document.addEventListener('DOMContentLoaded', function () {
    const summarizeBtn = document.getElementById('summarizeBtn');
    const summaryDiv = document.getElementById('summary');

    summarizeBtn.addEventListener('click', function () {
        console.log("Content script loaded.");

        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const videoId = extractVideoIdFromUrl(tabs[0].url);

            // Send a message to the content script to initiate the request
            chrome.tabs.sendMessage(tabs[0].id, { action: 'summarizeTranscript', videoId: videoId }, function (response) {
                console.log("msg sent");

                if (response && response.error) {
                    summaryDiv.textContent = response.error;
                } else if (response && response.summarized_transcript) {
                    let arr = response.summarized_transcript;
                    for (let a=0; a<arr.length; a++){
                        console.log(arr[a]);
                        // summaryDiv.textContent += "<li>" + arr[a] +"<li>";
                    }                    
                    summaryDiv.textContent = response.summarized_transcript
                    
                } else {
                    summaryDiv.textContent = 'An error occurred while summarizing the transcript.';
                }
            });
        });
    });

    // Helper function to extract video ID from the YouTube URL
    function extractVideoIdFromUrl(url) {
        const match = url.match(/v=([a-zA-Z0-9_-]+)/);
        if (match && match[1]) {
            return match[1];
        } else {
            return null;
        }
    }
});

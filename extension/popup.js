// alert("popup.js")
console.log("loaded popup.js")
document.addEventListener('DOMContentLoaded', function () {
    const summarizeBtn = document.getElementById('summarizeBtn');
    const summaryDiv = document.getElementById('summary');
    const sentenceLimitInput = document.getElementById('sentenceLimit');

    summarizeBtn.addEventListener('click', function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const videoId = extractVideoIdFromUrl(tabs[0].url);
            const sentenceLimit = sentenceLimitInput.value;

            // Send a message to the content script to initiate the request
            chrome.tabs.sendMessage(tabs[0].id, { action: 'summarizeTranscript', videoId: videoId, sentenceLimit: sentenceLimit }, function (response) {
                if (response && response.error) {
                    summaryDiv.textContent = response.error;
                } else if (response && response.summarized_transcript) {
                    summaryDiv.textContent = response.summarized_transcript.join('\n');
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

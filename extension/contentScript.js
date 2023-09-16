// content.js
console.log("Content script loaded.");

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === 'summarizeTranscript') {
        const videoId = request.videoId;
        const sentenceLimit = request.sentenceLimit; // Retrieve the sentence limit from the message
        console.log("cs.js"+sentenceLimit)

        // Make the request to your Flask server from the content script
        fetch(`http://localhost:5000/summarize_transcript?video_id=${videoId}&summarize=true&sentence_limit=${sentenceLimit}`)
            .then(response => response.json())
            .then(data => sendResponse(data))
            .catch(error => {
                console.error(error);
                sendResponse({ error: 'An error occurred while summarizing the transcript.' });
            });

        // Indicate that we will send a response asynchronously
        return true;
    }
});

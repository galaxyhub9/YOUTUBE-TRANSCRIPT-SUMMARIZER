// chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
//   if (request.action === 'summarizeTranscript') {
//     // Extract video ID from the current tab URL
//     chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//       const url = tabs[0].url;
//       const videoId = extractVideoId(url);

//       // Send a message to content script with the video ID
//       chrome.scripting.executeScript({
//         target: { tabId: tabs[0].id },
//         function: function (videoId) {
//           chrome.runtime.sendMessage({ action: 'summarizeTranscript', videoId: videoId });
//         },
//         args: [videoId],
//       });
//     });
//   }
// });

// function extractVideoId(url) {
//   const videoIdMatch = url.match(/v=([^&]+)/);
//   if (videoIdMatch) {
//     return videoIdMatch[1];
//   }
//   return null;
// }

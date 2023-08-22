from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join([entry['text'] for entry in transcript])
        summarized_transcript = summarize_text(full_transcript)
        return jsonify({'summarized_transcript': summarized_transcript})
    except Exception as e:
        return jsonify({'error': 'Transcript not available or invalid video ID.'}), 400

# model_name = "t5-base"
# model = T5ForConditionalGeneration.from_pretrained(model_name)
# tokenizer = T5Tokenizer.from_pretrained(model_name)


model_name = "facebook/bart-base"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

def summarize_text(text):
    # Prefix the input text with "summarize: " as required by the T5 model
    input_text = "summarize: " + text
    print("length------",len(input_text))
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)

    # Generate the summary
    summary_ids = model.generate(input_ids, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print(summary)
    return summary


if __name__ == '__main__':
    app.run(debug=True)
    

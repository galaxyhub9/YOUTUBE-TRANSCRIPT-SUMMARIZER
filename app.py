from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer
from summarizer import Summarizer
import spacy
import pytextrank 
from flask_cors import CORS  


nlp = spacy.load("en_core_web_lg") #INSTALL IT USING COMMAND pythom -m spacy download en_core_web_lg
nlp.add_pipe("textrank")

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


        

@app.route('/summarize_transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    should_summarize = request.args.get('summarize')

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join([entry['text'] for entry in transcript])
        # print("full_trascript____________-----", full_transcript)

        if should_summarize == 'true':
            summarized_transcript = summarize_text(full_transcript)
            print("i am here")
            # print("SUMMARIZED_SCRIPT=\n",summarized_transcript)
            return jsonify({'summarized_transcript': summarized_transcript})
        else:
            return jsonify({'full_transcript': full_transcript})
    except Exception as e:
        return jsonify({'error': 'Transcript not available or invalid video ID.'}), 400
    
    
def summarize_text(text):
    print("called summary fun")    
    summary1= []
    doc = nlp(text)
    for sent in doc._.textrank.summary(limit_phrases=2, limit_sentences=5):
        print(sent)
        summary1.append(str(sent))
    # print(summary1)
    # summary = " ".join(summary1)
    print("done with summ fun")
    return summary1

# model_name = "t5-base"
# model = T5ForConditionalGeneration.from_pretrained(model_name)
# tokenizer = T5Tokenizer.from_pretrained(model_name)


# model_name = "facebook/bart-base"
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)



# def summarize_text(text):
#     # Initialize the summarizer
#     model = Summarizer()

#     # Use extractive summarization to generate the summary
#     summary = model(text, ratio=0.5)  # You can adjust the ratio as needed
#     return summary

# def summarize_text(text):
#     # Prefix the input text with "summarize: " as required by the T5 model
#     input_text = "summarize: " + text
#     print("length------",len(input_text))
#     input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)

#     # Generate the summary
#     summary_ids = model.generate(input_ids, max_length=500, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
#     # summary_ids = model.generate(input_ids, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary


if __name__ == '__main__':
    app.run(debug=True)
    

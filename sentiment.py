import sys
sys.path.append('Text-Analytics')
from credentials import client
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Initialize the Text Analytics client
client = client()

# Read the documents from the Excel file using pandas
data = pd.read_excel('google.xlsx')
documents = data['Review'].tolist()

# Lists to store the results
sentences_list = []
sentiment_list = []
target_list = []

# Split the documents into batches of 10
batch_size = 10
num_batches = (len(documents) - 1) // batch_size + 1

for i in range(num_batches):
    # Select a batch of documents
    start_idx = i * batch_size
    end_idx = (i + 1) * batch_size
    batch_documents = documents[start_idx:end_idx]

    # Perform sentiment analysis on the batch
    response = client.analyze_sentiment(
        documents=batch_documents,
        language='en-US',
        show_opinion_mining=True
    )

    # Process the sentiment analysis results for each document in the batch
    for doc in response:
        # Result
        # Predicted sentiment for document
        print('Sentiment Analysis Outcome: {0}'.format(doc.sentiment))

        # Document level sentiment confidence scores between 0 and 1 for each sentiment label.
        print('Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f}'.format(
            doc.confidence_scores.positive,
            doc.confidence_scores.neutral,
            doc.confidence_scores.negative
        ))
        print('-' * 75)

        # To break down the analysis by each sentence, we can reference the sentences attribute
        sentences = doc.sentences
        for indx, sentence in enumerate(sentences):
            print('Sentence #{0}'.format(indx + 1))
            print('Sentence Text: {0}'.format(sentence.text))
            print('Sentence scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f}'.format(
                sentence.confidence_scores.positive,
                sentence.confidence_scores.neutral,
                sentence.confidence_scores.negative
            ))

            # Opinion analysis
            for mined_opinion in sentence.mined_opinions:
                target = mined_opinion.target
                print("......'{}' target '{}'".format(target.sentiment, target.text))
                print("......Target score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                    target.confidence_scores.positive,
                    target.confidence_scores.negative,
                ))
                for assessment in mined_opinion.assessments:
                    print("......'{}' assessment '{}'".format(assessment.sentiment, assessment.text))
                    print("......Assessment score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                        assessment.confidence_scores.positive,
                        assessment.confidence_scores.negative,
                    ))
            print()

        # Extract sentence-level data and store it in the lists
        for sentence in doc.sentences:
            sentences_list.append(sentence.text)
            sentiment_list.append(sentence.sentiment)

            # Check if there are mined_opinions in the sentence
            if sentence.mined_opinions:
                target_list.append(", ".join([mined_opinion.target.text for mined_opinion in sentence.mined_opinions]))
            else:
                # If there are no target words, use a placeholder value (e.g., 'N/A')
                target_list.append("N/A")

# Create a DataFrame
data = pd.DataFrame({'Sentence': sentences_list, 'Sentiment': sentiment_list, 'Target Text': target_list})

# Save the DataFrame to a CSV file
data.to_csv('sentiments_data.csv', index=False)


# Generate a word cloud for the sentiments
sentiments_text = ' '.join(data['Target Text'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(sentiments_text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Sentiments')
plt.show()
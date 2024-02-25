import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Extract keywords from the text
def extract_keywords(text):
    # Download NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

    # Initialize WordNet Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize each sentence into words and remove stopwords, punctuation, and colons
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    tokens = [word_tokenize(sentence) for sentence in sentences]
    tokens = [[word.lower() for word in sentence if word.lower() not in stop_words and word not in punctuation and word != ':'] for sentence in tokens]

    # Lemmatize tokens
    lemmatized_tokens = []
    for sentence_tokens in tokens:
        lemmatized_sentence = [lemmatizer.lemmatize(word) for word in sentence_tokens]
        lemmatized_tokens.append(lemmatized_sentence)

    # Perform part-of-speech tagging
    pos_tagged_tokens = [nltk.pos_tag(sentence_tokens) for sentence_tokens in lemmatized_tokens]

    # Extract adjectives and verbs
    keywords = []
    for sentence_pos_tags in pos_tagged_tokens:
        for word, pos_tag in sentence_pos_tags:
            if pos_tag.startswith('J') or pos_tag.startswith('V'):
                keywords.append(word)

    # Remove duplicates
    keywords = list(set(keywords))

    # Named Entity Recognition (NER)
    named_entities = named_entities = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))

    # Extract named entities
    named_entity_list = []
    for named_entity in named_entities:
        if isinstance(named_entity, nltk.Tree):
            named_entity_list.append(' '.join([word for word, _ in named_entity.leaves()]).lower())
        elif named_entity[1] in ['NNP', 'NNPS'] and named_entity[0] not in stop_words and named_entity[0] not in punctuation:  # Proper Nouns
            named_entity_list.append(named_entity[0].lower())

    # Remove duplicate named entities
    named_entity_list = list(set(named_entity_list))

    # Combine keywords and named entities
    keywords_and_entities = list(set(keywords + named_entity_list))

    # Generate synonyms for each keyword and named entity using WordNet
    keyword_synonyms_map = {}
    for keyword in keywords_and_entities:
        synonyms = set()
        for synset in wordnet.synsets(keyword):
            synonyms.update(set(synset.lemma_names()))
        synonyms.add(keyword)
        keyword_synonyms_map[keyword] = synonyms

    return keyword_synonyms_map


# Generate a query from the extracted keywords
def generate_query(keyword_map):
    # Generate subqueries for each keyword and its synonyms
    subqueries = []
    for _, synonyms in keyword_map.items():
        subquery = " OR ".join(f"candiate_profile_text = '{synonym}'" for synonym in synonyms)
        subqueries.append(f"({subquery})")

    # Combine the subqueries using the AND operator
    query = " AND ".join(subqueries)

    return query

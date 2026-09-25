# NLP and indicators

Text normalization preserves punctuation that carries security meaning. Regex extraction handles IPs, URLs/domains, hashes, emails, CVEs, MITRE IDs, ports, usernames, filenames, and selected suspicious terms. spaCy entity recognition is optional and requires an installed language model. Text model features use scikit-learn TF-IDF over incident text with unigram and bigram terms. No embeddings, transformers, or vector database are used.

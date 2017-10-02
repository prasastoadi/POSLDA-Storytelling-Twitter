from collections import Counter
import random

class LdaModel:
    """
    class lda
    """
    def __init__(self, documents=None, K=5, alpha=0.1, beta=0.1):
        """
        `documents` is the documents which used to find the topics
        `k` is the number of topics
        `alpha` is the
        `beta` is the
        """
        self.alpha = alpha
        self.beta = beta
        if documents is not None:
            self.initProcess(documents, K)
            self.assigning_topics()
            self.gibbs_sampling()

    def p_topic_given_document(self, topic, d, alpha):
        """the fraction of words in document _d_
        that are assigned to _topic_ (plus some smoothing)"""

        return ((document_topic_counts[d][topic] + alpha) /
                (document_lengths[d] + K * alpha))

    def p_word_given_topic(self, word, topic, beta):
        """the fration of words assigned to _topic_
        that equal _word_ (plus some smoothing)"""

        return ((topic_word_counts[topic][word] + beta) /
                (topic_counts[topic] + W * beta))

    def topic_weight(self, d, word, k):
        """given a document and a word in that document,
        return the weight for the k-th topic"""

        return p_word_given_topic(word, k) * p_topic_given_document(k, d)

    def sample_from(self, weights):
        """returns i with probability weights[i] / sum(weights)"""
        total = sum(weights)
        rnd = total * random.random()     # uniform between 0 and total
        for i, w in enumerate(weights):
            rnd -= w                      # return the smallest i such that
            if rnd <= 0: return i         # weights[0] + ... + weights[i] >= rnd

    def choose_new_topic(self, d, word):
        """blablabla"""
        return sample_from([topic_weight(d, word, k)
                            for k in range(K)])

    def initProcess(self, documents, K):
        """blablabla"""
        # a list of Counters, one for each document in documents
        document_topic_counts = [Counter() for _ in documents]

        # a list of Counters, one for each topic
        topic_word_counts = [Counter() for _ in range(K)]

        # a list of numbers, one for each topic
        topic_counts = [0 for _ in range(K)]

        # a list of numbers, one for each document
        document_lengths = [len(d) for d in documents]

        # the number of distinct words
        distinct_words = set(word for document in documents for word in document)
        W = len(distinct_words)

        # the number of documents
        D = len(documents)

    def assigning_topics(self):
        """blablabla"""
        random.seed(0)
        document_topics = [[random.randrange(K) for word in document]
                           for document in documents]

        for d in range(D):
            for word, topic, in zip(documents[d], document_topics[d]):
                document_topic_counts[d][topic] += 1
                topic_word_counts[topic][word] += 1
                topic_counts[topic] += 1

    def gibbs_sampling(self):
        """blablabla"""
        for iter in range(1000):
            for d in range(D):
                for i, (word, topic) in enumerate(zip(documents[d],
                                                      document_topics[d])):

                    # remove this word / topic from counts
                    # so that it doesn't influence the weights
                    document_topic_counts[d][topic] -= 1
                    topic_word_counts[topic][word] -= 1
                    topic_counts[topic] -= 1
                    document_lengths[d] -= 1

                    # choose a new topic based on the weights
                    new_topic = choose_new_topic(d, word)
                    document_topics[d][i] = new_topic

                    # and now add it back to the counts
                    document_topic_counts[d][new_topic] += 1
                    topic_word_counts[new_topic][word] += 1
                    topic_counts[new_topic] += 1
                    document_lengths[d] += 1

    def print_topics(self):
        for k, word_counts in enumerate(topic_word_counts):
            for word, count in word_counts.most_common():
                if count > 0: print (k, word, count)

if __name__ == "__main__":
    print("start")

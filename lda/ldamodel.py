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
        self.K = K
        if documents is not None:
            # a list of Counters, one for each document in documents
            self.document_topic_counts = [Counter() for _ in documents]

            # a list of Counters, one for each topic
            self.topic_word_counts = [Counter() for _ in range(K)]

            # a list of numbers, one for each topic
            self.topic_counts = [0 for _ in range(K)]

            # a list of numbers, one for each document
            self.document_lengths = [len(d) for d in documents]

            # the number of distinct words
            distinct_words = set(word for document in documents for word in document)
            self.W = len(distinct_words)

            # the number of documents
            D = len(documents)

            random.seed(0)
            self.document_topics = [[random.randrange(K) for word in document]
                               for document in documents]

            for d in range(D):
                for word, topic, in zip(documents[d], self.document_topics[d]):
                    self.document_topic_counts[d][topic] += 1
                    self.topic_word_counts[topic][word] += 1
                    self.topic_counts[topic] += 1

            for iter in range(1000):
                for d in range(D):
                    for i, (word, topic) in enumerate(zip(documents[d],
                                                          self.document_topics[d])):

                        # remove this word / topic from counts
                        # so that it doesn't influence the weights
                        self.document_topic_counts[d][topic] -= 1
                        self.topic_word_counts[topic][word] -= 1
                        self.topic_counts[topic] -= 1
                        self.document_lengths[d] -= 1

                        # choose a new topic based on the weights
                        new_topic = self.choose_new_topic(d, word, K)
                        self.document_topics[d][i] = new_topic

                        # and now add it back to the counts
                        self.document_topic_counts[d][new_topic] += 1
                        self.topic_word_counts[new_topic][word] += 1
                        self.topic_counts[new_topic] += 1
                        self.document_lengths[d] += 1

    def print_topics(self):
        for k, word_counts in enumerate(self.topic_word_counts):
            for word, count in word_counts.most_common():
                if count > 0: print (k, word, count)

    def p_topic_given_document(self, topic, d, alpha):
        """the fraction of words in document _d_
        that are assigned to _topic_ (plus some smoothing)"""

        return ((self.document_topic_counts[d][topic] + alpha) /
                (self.document_lengths[d] + self.K * alpha))

    def p_word_given_topic(self, word, topic, beta):
        """the fration of words assigned to _topic_
        that equal _word_ (plus some smoothing)"""

        return ((self.topic_word_counts[topic][word] + beta) /
                (self.topic_counts[topic] + self.W * beta))

    def topic_weight(self, d, word, k):
        """given a document and a word in that document,
        return the weight for the k-th topic"""

        return self.p_word_given_topic(word, k, self.beta) * self.p_topic_given_document(k, d, self.alpha)

    def sample_from(self, weights):
        """returns i with probability weights[i] / sum(weights)"""

        total = sum(weights)
        rnd = total * random.random()     # uniform between 0 and total
        for i, w in enumerate(weights):
            rnd -= w                      # return the smallest i such that
            if rnd <= 0: return i         # weights[0] + ... + weights[i] >= rnd

    def choose_new_topic(self, d, word, K):
        """blablabla"""

        return self.sample_from([self.topic_weight(d, word, k)
                            for k in range(K)])

if __name__ == "__main__":
    print("start")

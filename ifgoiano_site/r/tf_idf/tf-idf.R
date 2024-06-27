# install.packages(c("ggplot2", "e1071", "caret", "quanteda"))
library(quanteda)
library(ggplot2)

data.raw <- read.csv("../pubs_text_2023_02_13_23_22_05_4_05_04.csv")

length(which(!complete.cases(data.raw)))  # See how many incomplete rows.

data.tokens <- tokens(data.raw$text, what = "word", remove_numbers = TRUE,
                      remove_punct = TRUE, remove_symbols = TRUE, 
                      remove_separators = TRUE)

data.tokens <- tokens_tolower(data.tokens)

data.tokens <- tokens_select(data.tokens, stopwords(kind = "pt"), selection = "remove")

data.tokens <- tokens_ngrams(data.tokens, n = 2)

# data.tokens <- tokens_wordstem(data.tokens, language = "portuguese")

data.dfm <- dfm(data.tokens, tolower = FALSE)

data.matrix <- as.matrix(data.dfm)

data.df <- cbind(text = data.raw$text, convert(data.dfm, to = "data.frame"))

names(data.df) <- make.names(names(data.df))

term.frequency <- function(row) {
  row / sum(row)
}

inverse.doc.freq <- function(col) {
  corpus.size <- length(col)
  doc.count <- length(which(col > 0))
  log10(corpus.size / doc.count)
}

tf.idf <- function(x, idf) {
  x * idf
}

data.df <- apply(data.matrix, 1, term.frequency)

data.idf <- apply(data.matrix, 2, inverse.doc.freq)

data.tfidf <- apply(data.df, 2, tf.idf, idf = data.idf)

data.tfidf <- t(data.tfidf)

incomplete.cases <- which(!complete.cases(data.tfidf))

data.raw$text[incomplete.cases]

data.tfidf[incomplete.cases] <- rep(0.0, ncol(data.tfidf))

sum(which(!complete.cases(data.tfidf)))

data.dtframe <- cbind(text = data.raw$text, data.frame(data.tfidf))

write.csv(data.dtframe, "bigrams-tf-idf.csv")

result.df <- data.frame(text = data.dtframe$text)  # Copy the 'text' column to the new data frame

result.df$term <- ""

result.df$tfidf <- 0.0

tot.cols <- ncol(data.dtframe)

name.cols <- names(data.dtframe)

for (i in 1:nrow(result.df)) {
  the.max <- which.max(data.dtframe[i, 2:tot.cols])
  result.df$term[i] <- name.cols[the.max + 1]
  result.df$tfidf[i] <- data.dtframe[i, the.max + 1]
}

write.csv(result.df, "bigrams-max-tf-idf-term.csv")

max.values <- 10

term.counts <- table(result.df[["term"]])

sorted.counts <- sort(term.counts, decreasing = TRUE)

top.terms <- names(sorted.counts)[1:max.values]

top.counts <- sorted.counts[1:max.values]

counts.dtframe <- data.frame(term = top.terms, count = top.counts)

counts.dtframe <- subset(counts.dtframe, select = -count.Var1)

ggplot(counts.dtframe, aes(x = term, y = count.Freq, fill = term)) +
  geom_bar(stat = "identity") +
  labs(title = "Count of each term occurrence as max tf-idf",
       x = "term", y = "count.Freq")

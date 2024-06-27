# install.packages(c("topicmodels", "tidytext"))
# install.packages("tm")

library(topicmodels)
library(tidytext)
library(ggplot2)
library(dplyr)
library(tidyr)
library(quanteda)
library(tm)

# data("AssociatedPress")
# ap.lda <- LDA(AssociatedPress, k = 2, control = list(seed = 1234))
# ap.topics <- tidy(ap.lda, matrix = "beta")
# ap.top.terms <- ap.topics %>%
#   group_by(topic) %>%
#   slice_max(beta, n = 10) %>% 
#   ungroup() %>%
#   arrange(topic, -beta)
# ap.top.terms %>%
#   mutate(term = reorder_within(term, beta, topic)) %>%
#   ggplot(aes(beta, term, fill = factor(topic))) +
#   geom_col(show.legend = FALSE) +
#   facet_wrap(~ topic, scales = "free") +
#   scale_y_reordered()
# beta.wide <- ap.topics %>%
#   mutate(topic = paste0("topic", topic)) %>%
#   pivot_wider(names_from = topic, values_from = beta) %>% 
#   filter(topic1 > .001 | topic2 > .001) %>%
#   mutate(log_ratio = log2(topic2 / topic1))
# ap.documents <- tidy(ap.lda, matrix = "gamma")
# tidy(AssociatedPress) %>%
#   filter(document == 6) %>%
#   arrange(desc(count))

delete.words <- c(
  "dia", "dias", "ser", "podem", "confira", "final", "rio", "goiano", "verde", 
  "janeiro", "fevereiro", "marco", "março", "abril", "maio", "junho", "julho", 
  "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "ano", "sobre", 
  "hidrolândia", "morrinhos", "servidores", "reitoria", "realizado", "realiza",
  "realizados", "realizadas", "lançado", "nacional", "ept", "lista", "ciclo", 
  "prorrogadas", "faz", "horas", "devem", "veja")

data.raw <- read.csv("../pubs_text_2023_02_13_23_22_05_4_05_04.csv")

data.tokens <- tokens(data.raw$text, what = "word", remove_numbers = TRUE,
                      remove_punct = TRUE, remove_symbols = TRUE, 
                      remove_separators = TRUE)

data.tokens <- tokens_tolower(data.tokens)

data.tokens <- tokens_select(data.tokens, stopwords(kind = "pt"), selection = "remove")

data.tokens <- tokens_select(data.tokens, delete.words, selection = "remove")

data.tokens <- tokens_ngrams(data.tokens, n = 2)

# data.tokens <- tokens_wordstem(data.tokens, language = "portuguese")

data.dtm <- DocumentTermMatrix(Corpus(VectorSource(data.tokens)))

data.dtm <- data.dtm[1:length(data.tokens),]  # Cut off the rows beyond the size of the dataset.

data.dtm <- data.dtm[-which(apply(as.matrix(data.dtm), 1, function(row) all(row == 0)) == TRUE), ]  # Cut off the rows with only zeros.

data.lda <- LDA(data.dtm, k = 8, control = list(seed = 1234))

data.td <- tidy(data.lda)

data.top.terms <- data.td %>%
  group_by(topic) %>%
  slice_max(beta, n = 1) %>% 
  ungroup() %>%
  arrange(topic, -beta)

data.top.terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  scale_y_reordered()

data.documents <- tidy(data.lda, matrix = "gamma")

# tidy(data.dtm) %>%  # What are the most common words in that document filtered. 
#   filter(document == 1000)
#   arrange(desc(count))

data.classification <- slice(group_by(data.documents, document), which.max(gamma))

data.classification$document <- as.numeric(data.classification$document)

data.classification <- data.classification[order(data.classification$document), ]

write.csv(data.classification, "documents-classification.csv", row.names = FALSE)

# View(
#   data.documents %>%
#   group_by(document) %>%
#   slice(which.max(gamma)) %>%
#   arrange()
# )

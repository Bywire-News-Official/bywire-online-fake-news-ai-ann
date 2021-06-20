# Wirebit-Fake-News
Wirebit-Fake-News is the inception of a large project to automatically fake news in articles on the internet. The project was created on the 10th of June 2021 as part of the DevPost-ExpertAI hackathon. It is part of the [bywire.news](https://bywire.news) ecosystem to allow readers to gain trust in the news published, but there is wide interest in the project. In particular from education as it will allow us to teach pupils to be better aware of the mechanism used to spread fake news, publishing as it will create greater trust in established newspapers and social media. The project uses neuro-linguistic-programming (nlp), in particular expertai to turn an article into a feature vector. This feature vector is tranformed and uniformly scaled using heuristics, where a focus is placed on statistical anomalies (e.g. an article provokes more fear than usual), this will allows is to combine the features into an artificial neural network (ann) and a common sense model. Both the neural network and common sense model enhance eachother. For the neural network to be trained properly we will need manually flagged data, which is something we lack at the moment but the solution we build has a process in place so users can flag when they disagree with results of the algorithm. In this way we can build up training data over time and improve the model.
Since bywire.news stores all articles on ipfs and timestamps them on the blockchain in order to allow independent verification of the veracity, we integrated the server and webfrontend to allow retreiving directly the article associated with an ipfs document. One can go to the wirebittoken eos account (https://www.bloks.io/account/wirebittoken) and copy the article that is part of wirebittoken-publish into the web page and obtain a trust score.
One will notice that the main obstacle in the project was until now the severe lack of time, lack of staff and our corona.

## Technology
The core of the algorithms were written in python. We used python-flask to create a rest-api to interface with the algorithm and integrate it with the bywire.news platform. Machine learning was performed in Keras together with TensorFlow. For nlp we used expertai, nltk and nrclex. Access to expertai was done using the standard python bindings. As a database we employed mongodb. Trained anns were flushed to disk using json and the hd5 formats. For the webfrontend we used html5, javascript and php. For integration with the bywire.news platform we used angular, javascript and php. Integration with ipfs was done using an in house developed ipfs adapter together with the go-ipfs server. Finally the algorithms were developed using ubuntu 20.04. In theory they are programmed os independent, but this was not tested. Since it was not critical for the prototype user management was excluded. It is however very easy to add user management with jwt authentication in flask. The whitepaper is typeset using Latex.

## ExpertAI
ExpertAI is a nlp library that improves significantly over standard python libraries like nltk. Due to the need to parse the 150k articles currently published by bywire.news with an average length of around 1930 characters, to develop the concepts properly we introduced a switch to allow processing of the bulk of the articles without expertai until the algorithm is developed into a more mature stage. However ExpertAI already forms an essential part of the algorithms used. At the moment we are using the sentiment as calculated by ExpertAI, in particular to construct an euphoria indicator that points to extremely positive or negative sentiment and to detect when different nlp libraries give widely different results. We suspect the latter anomaly is a strong indication there is something suspect with the sentiment of the article. Furthermore ExpertAI is used to detect the lexical complexity of an article. The use of ExpertAI is only limited by the severe lack of time, but the possible uses are limitless as any statistical anomalies that one can detect is worth investigating and using. Apart from the measures already used we expect especially benefit in the short term future from the person/entity/concept densities (i.e. nr persons, nr relevant persons divided by article length).

## Algorithm
To describe the algorithm in the briefest of terms: we use a relatively standard setup machine learning. First we turn the text of an article, together with it's context (where was it published, who was the author) into a feature vector. This is scaled to a uniform range as it benefits gradient descent methods used in the learning algorithms for anns to have eigen values of similar magnitude. Then it is fed into a neural network. At the same time we tried to construct a heuristic model as this allows both to displays results for a wider range of articles while we are gathering data from users on which articles are falsified and it allows us a better understanding of how the ann and fake news detections works when properly trained by investigating the cases where both models give significantly different predictions. The Keras and Tensorflow already automatizes a lot of complexity with learning, overfitting and parameter instability away. So in short for the heuristic model we have the following flow: Text -> NLP Indicators -> Features -> Scaled Features -> Scores -> Trust. Plan to model using a convoluted neural network (cnn) so we can determine intermediate scores using the machine learning algorithm as understanding why something is fake news is probably more important than knowing if something is fake news.
The most interesting features we are looking at, based on domain knowledge. Sentiment, both extremely positive and negative as fake news needs to trigger an emotional reaction to be spread further and convince people. We have enhanced this with nrc sentiment to identify the top angry/fearful articles, since theory dictates that anger, fear and joy are emotions that spread better online while sadness and trust are emotions that hardly spread online. In short we are looking for articles that were engineered to spread maximally online. Further we look at lexical complexity: we expect that fake news is easier to read as it does not make sense to make an article that is hard to be read by the target audience and it would trigger thinking using the critical thinking system as defined by Daniel Kahnemann. Additionally we look for anomalies in the layout of the article: is it shorter than expected or uses shorter sentences to be more comprehensible.
For more details on how the algorithm was implemented and which features are actively developing a whitepaper (included in this github repository) that describes the finer details of the theory behind fake news detections.

### Features
At the moment we use nlp to turn the text into the following features. They are described in more detail in the [draft whitepaper](/whitepaper/whitepaper_trust.pdf) and it's references. The whitepaper is included in this repository as it explains some fundamental concepts necessary for understanding the theory why the prototype works but it definitely needs more word before publishing and is under active development. At the moment we have the following features. It must be remembered that this is a rough draft, where shortcuts where taken to get a working prototype. Any statements made are hypotheses and we are not sure if they are true, but they form a suspicion why a feature may be worth investigation. Please remember that many features can be refined upon (e.g. mapping sinonyms), but due to a lack of time. 
* Sentiment
  * sentiment1. This is the anger minus sadness score from the nrc sentiment as calculated by nrclex, normalized by the spread (10% - 90% confidence interval). The idea that the aim of fake news is to spread. On the internet anger and joy spread while sadness inhibits the spread ([as described in one of the first interviews from trendfollowing](https://www.trendfollowing.com/podcast/). Additionally anger has the benefit that it induces us to action [a better explanation can be found here](https://www.smithsonianmag.com/science-nature/what-emotion-goes-viral-fastest-180950182/)
  * sentiment2. This is a more elaborate version of sentiment1 by using the anger + fear - sadness - trust scores.
  * euphoria. This is maximum of positive euphoria and negative euphoria (depression). These are the positive and negative sentiment scores as calculated by expertai normalized to 1 for the top 10% (90% confidence interval) and a linear increase from the top 50% (median) to the top 10%.
* Complexity
  * word_length. This is the ratio of length of the clean text (removing punctuation, html and stop words) to the number of words. It was calculated using the nltk library. We suspect that having longer words might make a text harder to read and therefor harder to spread. 
  * complexity. This is the ratio between the clean text and the length of stemmed words. It was calculated using the nltk library. When stemmed words are signficantly shorter the text is likely more complex to read and therefore harder to spread.
  * duplication. This is the ratio between the number of tokens and the number of stemmed tokens. Indicating that certain terms were repeated often enhancing the chance people remember the message. It was calculated using the nltk library.
* Layout
  * text_length. The raw number of characters. The idea is that longer text have a harder time to reach a large audience. This is calculated using standard python.
  * punctuation. This is the ratio between the raw text and the clean text. The idea is that it is a rough measure for the length of individual phrases. Longer phrase length makes an article harder to read and therefore harder to spread.

In the calibration step confidence intervals were calculated using the database of bywire (150k articles from various professional new services) including for each feature only those articles where valid data was available. These confidence intervals are then used to construct a mapping to map all features to the interval \[0, 1\] and to have a non-zero slope in the areas of interest. These confidence intervals are calculated for each platform and for all data. This was done as some features are highly platform dependend (e.g. a median of 1900 characters per article makes no sence for twitter), the total data values are a fallback when no or little data is available for a platform. The advantage is that in this way we don't need to recalculate the features when more data becomes available and we can change the mapping without changing the underlying features.

## Endpoints
The server is implemented as an rest-api. However since analysis might take a while and in order to allow asynchonous processing of text we introduced endpoints to post an article and an endpoint to query whether the article was processed and the results are ready. Additionally for convenients of the developers there are endpoints to recalibrate parameters, models and to recalculate scores. Due to a lack of time no pacing restrictions were implemented, but it would be high on our priorities list to not allow querying the results, or submitting too many requests too often. However there is code in place to submit a request only once and if a text or ipfs hash was already submitted it's results are retrieved from the database instead of being recalculated again.

* /analyze/text - Submits an article to the server
  *  input: {"content":  "Text Goes Here",
    "title":     "Title of the article",
    "author":    "Author of the article",
    "publisher": "Publisher of the article"
    "platform":  "Platform that published the article"}
  *  output: {"id": "id to identify request", "new": true}
* /analyze/ipfs - Submits an ipfs hash to the server. The corresponding document is retrieved.
  * input: {"ipfs-hash": "IPFS hash"}
  *output: {"id": "id to identify request",
    "new": true}
* /analyze/flag - Flags an article as fake news
  * input: {"id":       "id identifying the article",
    "is_expert": "identifies if the user flagging the article was a regular reader or an expert",
    "strength":  "flags how fake the news is: 100 is super fake, -100 is very real"}
  * output {"status": "Status of request",
    "done": true if done}
* /analyze/query - Queries the status of a request using it's id.
  * input: {"id":       "id identifying the article"}
  * ouptut: {"id": "id to identify request",
    "status": "Status of processing the request",
    "done": "Whether the reuqest was parsed.",
    "data": json object containing the trust scores,
    "text": "if the request was from ipfs the ipfs text is returned"}


The following are very much for development purposes.
* /parameters/calibrate - Calculates the scaling factors and trains the ann.
  * input: {}
* /parameters/clean - Removes old models and scores from the database
  * input: {}
* /parameters/recalculate - Recalculates the feature set.
  * input: {}
* /brew/coffee - Makes it rfc2324 compliant

## Output
{"trust_score": 99, "sentiment_score": 80, "layout_score": 100, "complexity_score": 100, "divergence_score": 100, "platform_score": 100, "author_score": 100, "reasons": ["Provokes Anger"]}

## Team
Jetze Sikkema (Implementation, Algorithm Development & Prosecco Programming)
Michael O'Sullivan (Frontend & Drinking Beer with Fried Chicken on the side)


## Examples
Here are some examples of fake news stories and real news stories. The ipfs hashes you can use to load the stories into the Bywire Disinformation Detector are added. The fake news stories were the first ones to appear on a google search for fake news. The real news stories were the first stories that appeared in the guardian and bbc on the 18th of June. However we expect the algorithm to not always work this good as these were our first trials.
* Fake News
  * "Pope Franciscus endorses Donald trump". **Bywire Trust 1 - ipfs: **. A discussion of this article can be found [here](https://www.buzzfeednews.com/article/craigsilverman/the-strangest-fake-news-empire) and [here](https://www.snopes.com/fact-check/pope-francis-donald-trump-endorsement/)
  * "Biden Calls Trump and Supporters “Dregs of Society”". **Bywire Trust: 22 - ipfs: . The aricle can be found [here](https://twincitiesbusinessradio.com/content/all/biden-calls-trump-and-supporters-dregs-of-society )
  * "Nancy Pelosi’s Son Was Exec At Gas Company That Did Business In Ukraine". **Bywire Trust: 14 - ipfs: **

* Real News
  * Juneteenth: After decades, Opal Lee finally gets her day off.  **Bywire Trust: 76 - ipfs: **. The article can be found [here](https://www.bbc.com/news/world-us-canada-57536944)
  * HSBC offers sub-1% mortgage as interest rate war intensifies. **Bywire Trust: 86 - ipfs: **. The article can be found [here](https://www.theguardian.com/money/2021/jun/18/hsbc-mortgage-interest-rate-banks-building-societies-house-prices)
  * Praise and condemnation for Iran's new hardline president. **Bywire Trust: 61 - ipfs **. The article can be found [here](https://www.reuters.com/world/middle-east/praise-disdain-irans-new-hardline-president-2021-06-19/)



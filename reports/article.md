---
bibliography: [../references/bib.bib]
csl: ../references/chicago-notes-bibliography-classic.csl
header-includes:
  - \usepackage{titling}
  - \usepackage{fontspec}
  - \setmainfont[500]{Times New Roman}
  - \usepackage[margin=1in]{geometry}
  - \usepackage{caption}
  - \usepackage{booktabs}
  - \usepackage{tabularx}
  - \usepackage{array}
  - \usepackage{indentfirst}
  - \raggedright
  - \setlength{\parindent}{0.5in}
  - \makeatletter\let\@afterindentfalse\@afterindenttrue\makeatother
  - \usepackage{lscape}
  - \usepackage{etoolbox}
  - \usepackage{setspace}
  - \setstretch{2.0}
  - \apptocmd{\CSLReferences}{\setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}}{}{}
  - \fontsize{12pt}{14pt}\selectfont
  - \usepackage[hyphens]{url}
  - \sloppy
  - \usepackage{hyperref}
  - \hypersetup{breaklinks=true}
  - \setlength{\parindent}{0.5in}
  - \setlength{\parskip}{0pt}
  - \usepackage{titlesec}
  - \titleformat{\section}{\normalsize\bfseries}{}{0em}{}
  - \titleformat{\subsection}{\normalsize\bfseries}{}{0em}{}
  - \titlespacing*{\section}{0pt}{*0}{0pt}
  - \titlespacing*{\subsection}{0pt}{*0}{0pt}
  - \titleformat{\subsubsection}{\normalsize\bfseries}{}{0em}{}
  - \titlespacing*{\subsubsection}{0pt}{*2}{0pt}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyfoot[C]{\thepage}
  - \renewcommand{\headrulewidth}{0pt}
---
\begin{titlepage}

    \centering

    \vspace*{\fill}

    {\LARGE\bfseries State Supreme Court Selection Mechanisms and Dissent\par}

    \vspace{1.5cm}

    {\large Alexandria Nagy\par}

    \vspace{0.5cm}

    {\large \today\par}

    \vspace*{\fill}

\end{titlepage}
 
\newpage

\pagenumbering{gobble}

## Abstract

The present study examines the extent to which state supreme court selection mechanisms shape judicial opinion-writing behavior and reassesses dissent rates as a proxy for judicial independence. A mixed-methods design combines synthetic control analysis of transitions in selection mechanisms (2012–2024) with computational text analysis of 2.6 million opinions from all 50 state supreme courts (1970–2019). Synthetic control estimates of shifts between partisan and nonpartisan elections on the North Carolina Supreme Court reveal substantial measurement sensitivity, covariate imbalance, and counterfactual instability, yielding no reliable evidence that electoral reform systematically alters dissent frequency and raising concerns about dissent rates as a valid or reproducible measure of independence. Textual analysis employs a Wordscores framework anchored in PAJID-based seed dictionaries and expanded through Word2Vec embeddings to produce rhetoric scores reflecting the balance of ideological and conventional language in each opinion. Although pooled models show no statistically significant differences in rhetoric scores across selection regimes, event studies reveal directionally consistent rhetorical shifts following institutional change, suggesting that linguistic content is a more behaviorally sensitive indicator of institutional effects than dissent frequency.

\newpage

\pagenumbering{arabic}
\setcounter{page}{1}

## Introduction

The United States is undergoing a profound transformation in its judicial landscape. In the current millieu marked by rising polarization and a more openly majoritarian conservative constitutional order, the Supreme Court of the United States has delegated responsibility for resolving many contentious national issues to the states by narrowing federal oversight in areas such as campaign finance, partisan gerrymandering, abortion, and voting rights. As the stakes of state-level adjudication have increased, the expected policy payoff of controlling state supreme courts has risen as well. State legislatures and partisan actors have responded by restructuring judicial selection systems to allow for greater direct political influence, most prominently by replacing nonpartisan judicial elections with explicitly partisan contests through the inclusion of party affiliations on ballots. Although these measures were ultimately defeated in Montana in 2025, North Carolina passed a bill requiring judicial candidates to list party affiliation on both primary and general election ballots in 2017, followed by Ohio in 2021 and West Virginia in 2025.^[See Ohio S.B. 80 (2021); N.C. Sess. Law 2016-125 (2016); W. Va. S.B. 521 (2025).] These transformations raise concerns that states are aiming to use judiciary as a mouthpiece for their reforms.

Against this backdrop, scholars remain divided over whether the shift toward partisan judicial selection effectively balances judicial independence and accountability, two principles that are inherently in tension.^[See @Hall2001 for an overview of the scholars involved in this debate] Judicial independence allows courts to decide cases based on law and free from external pressures, while accountability requires them to remain responsive to public values and societal needs. Reform advocates tend to argue that partisan elections place too much emphasis on party loyalty and electoral considerations, undermining independence and risking decisions driven more by politics than by legal reasoning. Moreover, partisan elections may homogenize courts such that substantive disagreements that protect independence are reduced. Reformers thus generally favor nonpartisan elections or merit-based retention systems, such as the Missouri Plan, to prioritize professional qualifications and preserve judicial autonomy. In contrast, opponents of reform contend that partisan elections enhance democratic accountability without necessarily eroding independence, as electoral competition incentivizes judges to remain attentive to voter concerns. This debate highlights how different selection mechanisms structure judicial incentives and shape the potential for systematic bias in judicial decision-making.

This study extends scholarship on judicial independence in state supreme courts by examining the institutional shift from nonpartisan to partisan judicial elections. Prior research has employed a range of empirical strategies to estimate how selection mechanisms influence dissent rates, which are frequently used as a behavioral proxy for judicial independence [@Canon1970; @HallAndWindett2013; @Renberg2020]. These approaches include manual data collection, automated web scraping using Python, and quasi-experimental techniques such as the synthetic control method (SCM). Despite these advances, dissent rates remain an imperfect measure and are vulnerable to concerns about data completeness, reproducibility, and construct validity. As language modeling techniques advance, computational textual analysis of judicial opinions offers a more complete understanding of judicial behavior than dissent rates alone. By distinguishing ideological from conventional language, this approach provides insight into how institutional design shapes judicial rhetoric. This study therefore evaluates whether partisan and nonpartisan selection mechanisms influence patterns of opinion-writing and considers what these differences imply for the measurement of judicial independence in state supreme courts.

## Literature Review

Scholarship is divided on whether dissent strengthens or undermines courts. Some scholars characterize the decision to write separately a destabilizing force that fosters division, undermines the authority of the majority, and generates uncertainty in the law [@Entrikin2017]. Extending this argument, Hall and Windett contend that chief justices have incentives to discourage dissent because it imposes reputational costs, weakens precedent, and invites additional appeals [@HallAndWindett2013]. Moreover, contributors to the Harvard Law Review argue that the presence of dissenting opinions can introduce political and doctrinal uncertainty into judicial deliberations, thereby complicating the Court’s ability to project doctrinal clarity and institutional unity [@HarvardLawReview2011]. By contrast, other scholars view dissent as an essential mechanism of judicial independence. From this perspective, justices have a duty to articulate independent judgments, particularly in cases involving profound disagreement. Dissents preserve alternative interpretive frameworks, foster constitutional dialogue, and lay foundations for future doctrinal change [@Brennan1986; @Urofsky2015]. Doctrinal uncertainty within dissents may even enhance deliberation by surfacing disagreements that would otherwise remain obscured [@HarvardLawReview2011]. Empirically, dissent is frequently interpreted as a behavioral signal of independence—a justice’s willingness to challenge prevailing doctrine, advance alternative reasoning, and resist external pressures [@Renberg2020].

On the other hand, proponents of dissent argue that Justices have a duty to articulate their independent judgments, particularly in cases involving profound disagreement. From this perspective, dissents are crucial mechanisms for fostering constitutional dialogue, preserving alternative interpretive frameworks, and laying the foundation for future doctrinal development [@Brennan1986; @Urofsky2015]. Scholars further suggest that doctrinal uncertainty within dissents can be beneficial, bringing to light issues that might otherwise remain hidden within the Court’s deliberations and enhancing the quality of the decision-making process [@HarvardLawReview2011]. Additionally, scholars find that dissent signals behavioral independence, reflecting a Justice’s willingness to challenge the doctrinal status quo articulated in majority opinions, advance alternative legal interpretations, and resist political pressures [@Renberg2020]. 

Accordingly, scholars examine the frequency of dissent as a meaningful indicator of judicial independence. One strand of literature operates at the interpersonal level, emphasizing the internal dynamics that promote consensus and discourage dissent. Jaros and Canon identify the role of strong chief justice leadership, high levels of social integration, and a prevailing norm of unanimity as forces that cultivate consensus [@Canon1970]. Related research supports that chief justices actively discourage dissent to preserve collegiality, reinforce precedent, and bolster public confidence. Consistent with this account, dissent rates tend to be lower on courts where the chief justice exercises greater formal authority and where members possess fewer institutional resources. By contrast, abundant institutional resources can dilute hierarchical control and facilitate separate opinion writing [@HallAndWindett2013]. Epstein, Landes, and Posner extend this line of inquiry by introducing the concept of “dissent aversion,” arguing that judges may strategically suppress disagreement to avoid its institutional costs. However, they find that this tendency weakens as ideological polarization intensifies and panel sizes expand, conditions that render consensus more difficult to sustain [@EpsteinLandesPosner2011].

Yet interpersonal dynamics alone cannot explain variation in dissent rates across courts. At the environmental level, Brace and Hall find that higher urbanization, greater political competition, and increased state spending are each associated with elevated dissent rates [@Brace1990]. Courts operating in such contexts confront a more diverse array of regulatory, commercial, civil rights, and criminal legal disputes that implicate competing interests and normative commitments. At the institutional level, Brace and Hall contend that court structure accounts for substantially greater explanatory power than these environmental factors [@Brace1990]. For example, the presence of intermediate appellate courts filters out routine cases, concentrating complex and high-conflict disputes at courts of last resort, thereby increasing the likelihood of dissent in these jurisdictions.^["Court of last resort" is used interchangeably with "state supreme court."] Random assignment of opinions further facilitates dissent by limiting the chief justice’s ability to allocate authorship strategically as a reward or sanction. Conversely, conference procedures organized around seniority norms encourage consensus by creating reputational and hierarchical incentives against open disagreement. Jaros and Canon additionally find that dissent rises with court size, where coordination costs are higher and ideological dispersion more likely, and declines with longer judicial tenure, which reinforces norms of collegiality and institutional cohesion [@Canon1970].

The scholarship most directly relevant to the present study investigates how judicial selection mechanisms influence dissent rates. Brace and Hall find that appointed judges tend to foster consensus, whereas elected judges display higher levels of dissent [@Brace1990]. Jaros and Canon report a comparable pattern, noting that popularly elected courts dissent more frequently than their appointed counterparts [@Canon1970]. Hall and Windett offer a systematic comparison across four selection systems, including gubernatorial or legislative appointment systems, the Missouri Plan, nonpartisan elections, and partisan elections. They conclude that longer tenures, greater professionalization, and insulation from electoral pressures enable appointed and Missouri Plan courts to sustain consistently low dissent rates [@HallAndWindett2016]. By contrast, courts selected through nonpartisan elections exhibit consistently higher dissent rates, indicating that electoral incentives shape judicial behavior even in the absence of party labels. Partisan election courts display the most pronounced and unstable dissent patterns, which the authors attribute to the distinct reelection pressures inherent in partisan selection systems. Extending this line of inquiry, Renberg employs synthetic control methods to assess how changes in judicial selection mechanisms affect dissent rates on state supreme courts. She finds that removing partisan labels from ballots increases dissent, indicating that justices strategically constrain their jurisprudential reasoning under partisan pressures and exercise greater independence when party identifiers are absent [@Renberg2020].

However, this literature examining the effects of judicial selection mechanisms on dissent rates faces two primary challenges. The first challenge concerns data availability. The FAIR principles emphasize that scientific data should be findable, accessible, interoperable, and reusable [@WilkinsonFAIR2016], yet data on dissent rates remain sparse and difficult to access. The State Supreme Court Data Project, often described as the premier database for state supreme court research, covers only four years (1995–1998) [@StateSupremeCourtProject]. Hall and Windett attempted to address this by releasing a dataset of state supreme court opinions, but their data is currently inaccessible and their accompanying code relies on web scraping methods prohibited under LexisNexis' terms of service [@HallAndWindett2013]. While LexisNexis offers comprehensive access to published opinions, its proprietary structure limits transparency for researchers without bulk-access subscriptions. Open-source alternatives, such as CourtListener, provide greater accessibility but feature substantially less comprehensive case coverage. The second challenge is reproducibility. Scholars frequently present dissent rate data through graphical depictions without clearly documenting the measurement conventions, inclusion criteria, or database parameters underlying their estimates [@Renberg2020]. Because multiple operationalizations of dissent are plausible, varying by query construction, opinion type, and database, estimated rates are highly sensitive to methodological choices.^[Replications of Renberg (2020) and Hall and Windett (2013) were attempted using both CourtListener and LexisNexis. In CourtListener, searches were limited by court and refined with advanced opinion-type operators (e.g., combined, unanimous, lead, plurality, concurrence, in-part, dissent, addendum, remittitur, rehearing, on-the-merits, and on-motion-to-strike). LexisNexis queries employed the OpinionBy and DissentBy fields and the “find by source” function. Multiple approaches were tested to collect dissent rates, including querying all justices serving between 1995 and 2010 and restricting results to full merits opinions by excluding terms such as “dismiss!,” “petition for review,” and “motion for” using AND NOT operators. Across databases and query configurations, estimated dissent rates failed to replicate Renberg’s graphs or Hall and Windett’s reported figures.] Without detailed documentation of coding rules and data provenance, baseline dissent rates cannot be independently verified, limiting the field's ability to build cumulatively on prior work.

Beyond these limitations, examining dissent frequency alone offers only a partial understanding of the ideological and strategic considerations that shape judicial opinion-writing (Bailey and Maltzman, 2011; Hinkle, 2015; Songer and Lindquist, 1996). The type of rhetoric employed in crafting dissents mediates whether disagreement is perceived as principled independence or as conduct that undermines the Court’s integrity and legitimacy. Scholarship in the Harvard Law Review provides a framework for understanding the “respectful dissent,” emphasizing how collegial rhetoric signals acknowledgment of the majority’s legitimacy while preserving the dissenter’s independence as a reasoned and impartial jurist [@HarvardLawReview2011]. Conversely, scholars show that justices at the appellate level who employ respectful rhetoric often anticipate the preferences of their colleagues, moderate their positions, tailor their opinion language, or withholding dissent when doing so would be futile or costly. This suggests that collegial tone may instead function as a behavioral constraint that undermines judicial independence in an effort to preserving institutional legitimacy [@HettingerLindquistMartinek2006].

For much of the early history of the United States, dissenting opinions were exceedingly rare. Norms of institutional unity were so entrenched that Justices on the U.S. Supreme Court who chose to write separately often felt compelled to preface their dissent with an apology for departing from the majority. Even after dissenting became more common, justices adhered to a cordial tone. By the late nineteenth century, justices increasingly used dissents to articulate their individual jurisprudential commitments, and some dissents were later vindicated by doctrinal change and effectively became law. These political outcomes strengthened incentives for minority justices to preserve their positions through separate writing. The contentious disputes of the New Deal era produced increased ideological dissonance, yet the norm of dissenting "respectfully" persisted for the next three decades, until openly critical dissents began to signal a broader transformation in the tenor of judicial opinion-writing [@Entrikin2017]. 

This tension between respectful and assertive rhetoric in dissenting opinions, and its implications for judicial independence among the transforming tenor of judicial opinion-writing, is exemplified by the dialogue between Justice Scalia and Chief Justice Hughes. Known for his frequent, confrontational, and "acerbic" dissents, Scalia argued that assertive dissents are the product of “independent and thoughtful minds” rather than judges who prioritize consensus merely to advance institutional ends. By contrast, Chief Justice Hughes emphasized that judicial independence is inseparable from the Court’s reputation, which rests fundamentally on the character of its judges. He cautioned that independence is threatened by “cantankerousness," or persistent ill temper, argumentativeness, or uncooperativeness. Instead, he advocated for norms of civility and collegiality in dissent, viewing them as expressions of a deeper appreciation for the Court’s democratic role, and maintaining that public confidence in the Court’s institutional integrity is itself essential to sustaining judicial independence. Accordingly, while Scalia’s assertive and confrontational rhetoric may seek to signal judicial independence, Hughes underscores that such challenges to the majority’s authority can ultimately jeopardize the very institutional legitimacy the dissenter purports to defend [@Entrikin2017].

A growing body of scholarship has adopted computational textual analysis to examine rhetoric in legislative texts. The intellectual premise for these approaches is articulated by Truscott and Romano (2025), who argue that terminology functions as a deliberate expression of ideology. For instance, the terms “healthcare provider” and “abortionist” both refer to the same category of medical professional, yet each conveys markedly different ideological valences and signals alignment with competing moral, political, or policy perspectives. Three foundational scaling approaches have been particularly influential. First, Wordscores is an unsupervised method that relies on reference documents to compare word frequencies between texts. A primary advantage of Wordscores is that it minimizes human error and the need for intensive hand-coding (Laver, Benoit, and Garry, 2003). Second, Wordfish estimates actor positions from word frequencies using a Poisson distribution, removing the requirement for predefined reference documents (Slapin and Proksch, 2008). Third, Wordshoal is a two-stage hierarchical extension of Wordfish designed to estimate latent preferences from expressed positions in legislative speech (Lauderdale and Herzog, 2016). Despite the sophistication of these methods in legislative research, their application to judicial behavior has lagged, partly due to the distinctive structural features of judicial text production. Unlike legislative speeches, which are directly attributable to individual members, judicial opinions are collaborative products authored by one justice but joined by several others, complicating the attribution of textual content to individual ideological positions. 

Nonetheless, the literature has made substantial progress. Hauslauden, Schubert, and Ash use a 5% hand-coded sample of cases from U.S. Circuit Courts to predict liberal and conservative ideological directions in judicial decisions. Bailey and Maltzman (2011) investigate the use of ideologically loaded terms in dissenting opinions, demonstrating that certain word choices correlate with more assertive or confrontational dissents. Moreover, Songer and Lindquist (1996) examine language patterns to identify how justices signal disagreement subtly, adjusting rhetoric based on anticipated reactions from colleagues or the broader public. Lauderdale and Clark integrated topic modeling into the scaling of judicial preferences, demonstrating that incorporating LDA-derived issue dimensions alongside voting data enables multidimensional mapping of justice-level ideal points that purely vote-based models cannot achieve. Hausladen et al. trained classification models on Courts of Appeals opinions, demonstrating that ideological direction is predictable from opinion language alone. An expert-elicitation-text hybrid developed by Cope (2024) uses a hierarchical n-gram analysis of lawyer assessments to recover dynamic ideology scores by treating practitioner language as a structured ideological signal rather than relying on the opinions themselves. Truscott and Romano (2025) adapt the Wordshoal approach from legislative speech to judicial opinions. Altogether, this literature has demonstrated that ideological signals are recoverable from the written text of judicial opinions.

Despite these advances, significant gaps in the literature remain. Renberg contends that the SCM provides a robust causal measure of the effects of selection mechanisms on dissent rates. However, her findings have not been independently validated. Moreover, scholars have yet to examine the inverse transition from nonpartisan to partisan selection mechanisms. Additionally, the body of scholarship employing computational text analysis to study the rhetoric within texts has been overwhelmingly concentrated in the legislative branch, where tools such as Wordscores, Wordfish, and Wordshoal were initially developed and validated. Extensions of these methods to judicial texts have focused primarily on the U.S. Supreme Court and federal circuit courts, leaving state supreme courts largely unexplored. The present study seeks to address these gaps by applying SCM to examine the effects of transitioning from nonpartisan to partisan selection on dissent rates and by deploying the Wordscores framework to a comprehensive corpus of state supreme court opinions.

## Methodology

This study employs a mixed-methods research design combining statistical modeling of dissent rates with computational text analysis of published dissents to evaluate the effects of institutional reform on judicial opinion writing. The first component utilizes the synthetic control method (SCM), originally developed by Alberto Abadie and Javier Gardeazabal and later extended by Abadie, Alexis Diamond, and Jens Hainmueller, to estimate the causal effects of aggregate institutional interventions [@Abadie2003; @Abadie2010]. The second component employs a computational textual analysis that proceeds in four stages: a Word2Vec model trained on preprocessed opinion text generated the vector space for all subsequent analyses; the Wordscores method produced initial ideological and conventional seed-word dictionaries; these dictionaries were expanded and refined using Word2Vec; and an Evidence Minus Intuition (EMI) framework produced rhetoric scores for each opinion reflecting the balance of ideological versus conventional rhetoric.

The synthetic control analysis extends Renberg's methodological framework, which demonstrates that SCM can credibly estimate the causal effects of changes in judicial selection mechanisms on opinion-writing behavior [@Renberg2020]. SCM estimates a counterfactual outcome by constructing a weighted composite of control units that closely match the treated unit's pre-intervention characteristics. While Renberg examined the transition from partisan to nonpartisan elections, this study analyzes the inverse: the shift from nonpartisan to partisan elections. This reform was enacted in North Carolina by statute in 2017 and first implemented in the November 6, 2018 election. To estimate dissent rates had the North Carolina supreme court remained nonpartisan, a counterfactual court was constructed from a donor pool of seven state supreme courts that have consistently maintained nonpartisan elections: Arkansas, Georgia, Kentucky, Minnesota, Montana, Oregon, and Wisconsin. Pretreatment covariates used to weight these courts are described in Table \ref{tab:pretreatment}.

\begin{table}[htbp]
\captionsetup{justification=raggedright, singlelinecheck=false, skip=3pt} % less space before caption
\caption{Pretreatment Characteristics}
\label{tab:pretreatment}
\centering
\renewcommand{\arraystretch}{0.95} % tighter row spacing

\newcolumntype{H}{>{\raggedright\arraybackslash\hangindent=1em\hangafter=1}X}
\newcolumntype{V}{>{\raggedright\arraybackslash\hangindent=1em\hangafter=1}p{4cm}}

\begin{tabularx}{\textwidth}{@{} V H >{\raggedright\arraybackslash}p{3.6cm} @{}}
\toprule
\textbf{Variable} & \textbf{Operationalization} & \textbf{Source Initiative} \\
\midrule
Term Length &
Count of years between judicial elections. &
Ballotpedia \\

Number of Justices &
Count of justices on the bench. &
Ballotpedia \\

Professionalization Score &
Professionalism index based on the Court Statistics Project. &
Squire (2021) \\

Campaign Fundraising &
Amount, in dollars, of reported campaign funds raised. &
Open Secrets \\

Number of Capital Punishment Cases &
Count of capital punishment cases reviewed. &
Lexis Nexis \\

Number of Lower Court Capital Punishment Cases &
Count of capital punishment cases reviewed in the previous year by lower courts. &
Lexis Nexis \\

Number of Published Opinions &
Count of reported opinions. &
Lexis Nexis \\

Single-Member Election District &
Valued at one if the state uses single-member districts and valued at zero otherwise. &
Ballotpedia \\

Percent of Docket Concerning Criminal Procedure &
Number of reported criminal procedure cases divided by the number of reported cases. &
Lexis Nexis \\

Competitive Election &
Valued at one if the average victory margin in the most recent election was less than 10\% and zero otherwise. &
Ballotpedia \\

Ideological Spread &
Absolute difference in cfscores between the most and least liberal judge in the court. &
Bonica (2024) \\

State Citizen Ideology &
Mean ideological self-placement of all respondents in a state, aggregated from individual ANES survey responses. &
ANES Time Series Study (2024) \\

State Government Ideology &
Mean of first-dimension NOMINATE scores for congressional members (House and Senate) &
Voteview (2026) \\
\bottomrule
\end{tabularx}
\end{table}

Pretreatment covariates were collected annually from 2012 to 2024 for the treated court and each control court. Structural features including term length, number of justices, single- versus multimember election districts, and electoral competitiveness were obtained from Ballotpedia [@Ballotpedia]. Campaign finance data, defined as the total funds raised by candidates in the most recent election for each year, were collected from the National Institute on Money in Politics [@FollowTheMoney]. Court professionalization scores that measure staff size, judicial pay, and docket control were drawn from Squire and Butcher’s updated 2019 index [@Squire2021].^[Due to Squire and Butcher's discussion of the relative stability of court professionalization scores, the 2019 values are assumed unchanged for each court throughout the study period.] Caseload characteristics, including the number of published opinions, capital punishment appeals reviewed, capital cases resolved by lower courts in the prior year, and the proportion of the docket devoted to criminal procedure, were obtained from LexisNexis [@LexisNexis]. Court ideological spread was measured using Bonica’s common space campaign finance scores, CFscores [@DIME]. Because state citizen and government ideology measures from Berry et al. [@Berry1998] are unavailable for the study period, state citizen ideology was approximated using aggregated responses from the 2024 ANES Time Series Study. State government ideology was operationalized as the average first dimension NOMINATE score of all congressional members in each state [@Berry2010; @Voteview2026].

Measurement of dissent rates captures only one dimension of judicial behavior. The presence of greater dissents does not inherently imply stronger judicial independence, as dissents may alternatively function as strategic vehicles for partisan or external signaling. Accordingly, the present study analyzes the substantive content of dissents by examining the rhetoric they convey. The computational textual analysis draws on a corpus of dissenting opinions from the Collaborative Open Legal Data (COLD) Cases dataset, a repository of over 8.3 million U.S. legal decisions compiled from CourtListener. The dataset was restricted to state supreme court cases decided between 1965 and 2025, and dissent texts were preprocessed using spaCy’s large English language model. A Word2Vec neural embedding model was subsequently trained on the processed corpus using a skip gram architecture. This model learns distributed vector representations of words by predicting their surrounding context, such that terms appearing in similar linguistic environments occupy nearby positions in the embedding space. By modeling semantic proximity rather than simple word frequency, this approach captures contextual structure beyond traditional "bag of words" methods. The trained Word2Vec model defines the vector space for all subsequent analyses.

The Wordscores method was then used to create two seed word dictionaries: one capturing strongly ideological rhetoric likely to experience influence by partisan or external pressures, and one capturing centrist rhetoric reflecting conventional legal reasoning. Wordscores was applied to two reference corpora anchored in Party-Adjusted Surrogate Judge Ideology (PAJID) measures [@BraceLangerHall2000]. PAJID scores estimate the political ideology of state supreme court justices from 1970 to 2019 based on party affiliation, state political climate, and the ideology of their selectors, ranging from 0 (most conservative) to 100 (most liberal), with 50 representing the ideological center. The first corpus includes opinions authored by the top 10% most ideologically extreme justices, capturing both liberal and conservative perspectives, while the second corpus includes opinions authored by the middle 10% of the ideological spectrum. Weighted term frequencies for each corpus were calculated using Term Frequency–Inverse Document Frequency (TF-IDF), which captures a word’s importance in a document relative to the corpus.^[TF-IDF increases with a word's frequency within the document (TF) and decreaes with a word's overall frequency across the corpus (IDF) to account for common terms.] Wordscores for each reference group were then calculated by weighting each word’s TF-IDF frequency by the authoring justice’s absolute PAJID deviation, $|s_d - 50|$, and averaging across all documents:

$$W_w = \frac{\sum_{d \in R} f_{wd} \cdot |s_d - 50|}{\sum_{d \in R} f_{wd}}$$

where $W_w$ is the score for word $w$, $R$ is the set of reference texts, $f_{wd}$ is the TF-IDF–weighted frequency of $w$ in document $d$, and $|s_d - 50|$ is the absolute PAJID deviation of the authoring justice. Words were ranked by the difference between their ideological and conventional scores. The top 50 words with the highest positive difference formed the ideological seed dictionary, and the top 50 words with the highest negative difference formed the conventional seed dictionary. Each dictionary was then expanded using Word2Vec nearest neighbors to capture semantically related terms.

Rhetoric scores were calculated by adapting the Evidence Minus Intuition (EMI) method developed by Aroyehun et al [@Aroyehun2025]. Originally designed to distinguish evidence- from intuition-based language in congressional speeches, the method was applied to quantify ideological versus conventional rhetoric in judicial opinions. Two concept vectors were created by averaging the embeddings of all words in each expanded dictionary.^[Embeddings are numerical representations of words as vectors. "Vectors" are lists of numbers, and "embedding" refers to the process and result of mapping a word into that vector space.] Document vectors were then constructed for each dissent by identifying the presence of words from either dictionary and averaging their embeddings. Cosine similarity between each document vector and the concept vectors produced separate ideological and conventional scores for each opinion, reflecting how closely the opinion’s language aligns with each rhetorical pole. Positive values indicate stronger conventional rhetoric, while negative values indicate stronger ideological rhetoric. The final rhetoric score is defined as:

$$\text{Rhetoric Score} = \text{CosSim}(\text{doc}, \text{conventional}) - \text{CosSim}(\text{doc}, \text{ideological})$$

## Analysis

Give a preview of the whole analysis section

### Synthetic Controls Results

![Dissent Rates in North Carolina Supreme Court \label{dissent_rates}](figures/nc_dissent_rate.png)

This section presents the results of the synthetic control analysis. As shown in \ref{dissent_rates}, North Carolina's dissent rate remained consistently low (around 1%) from 2012 to 2017, rising to 1.9% in 2018 and 4.5% in 2020, before declining to 2.2% in 2021 amid COVID-19-related court closures. Donor courts exhibited more variable patterns.^[Wisconsin had the highest dissent rates, often exceeding 50% and reaching 88% in 2016; in many cases, opinion text was unavailable, producing fewer results when using Lexis’s OpinionBy function and likely inflating calculated rates. Arkansas showed volatile rates, ranging from 7.7% in 2012 to over 50% in 2018–2020. Georgia and Minnesota remained relatively stable, typically below 10%.] 

![Estimated impact of judicial reform on dissenting behavior \label{scm}](figures/scm.png)

As shown in \ref{scm}, the synthetic control analysis estimates a treatment effect of 0.000%, indicating no detectable change in dissent behavior following North Carolina's adoption of partisan judicial elections in 2018. This finding diverges from Renberg's [@Renberg2020], who finds that switching away from partisan elections is associated with increased dissent rates, which she attributes to justices being liberated from electoral constraints and able to assert their legal philosophy more freely. The present analysis examining the reverse transition fails to detect an inverse effect when partisan elections are adopted. One sensitivity analysis provides tentative support for the null result. Placebo tests that reassign the treatment year to each pre-intervention year (2014–2017) produce systematic gaps between North Carolina and its synthetic counterpart. Estimated placebo effects range from −2.62% to −3.78%, with a mean of −2.92%. The observed 2018 treatment effect of 0.00% is distinguishable from this placebo distribution at conventional significance levels (p = 0.042), suggesting the post-reform period is not simply reflecting pre-treatment variation. This result should nevertheless be interpreted cautiously. The sections that follow assess the robustness and substantive credibility of this null finding in greater detail.

### Model Fit

Mean Squared Prediction Error (MSPE) serves as the principal diagnostic for assessing the validity of the synthetic control design. Formally, MSPE is defined as the average squared difference between North Carolina’s observed dissent rates and those predicted by its synthetic counterpart. Substantively, it measures how closely the synthetic court reproduces the treated court’s pre-intervention trajectory. A low pre-treatment MSPE is necessary for credible inference, as it indicates that the synthetic unit approximates a plausible counterfactual prior to reform. Under those conditions, any subsequent divergence can reasonably be attributed to the institutional change rather than to model misspecification.

In the present analysis, the pre-treatment MSPE for 2012-2017 (0.0007) is consistent with the null hypothesis. At first glance, this small value appears to indicate strong fit between the synthetic and actual North Carolina Supreme Court. However, as discussed prior, dissent rates on the Court are extremely low and display limited variation. In such sparse data contexts, small absolute MSPE values may simply reflect the scale of the outcome variable rather than meaningful alignment or lackthereof in trajectory. Figure \ref{scm} reinforces this finding, visually illustrating that the synthetic court does not closely track the North Carolina Supreme Court’s actual dissent rates prior to reform. Additionally, we would expect an increase in the post-treatment MSPE if partisan elections had altered dissent behavior post-treatment, reflecting greater divergence between the treated court and its synthetic counterfactual. Instead, the post-treatment MSPE for 2018–2024 declines to 0.0002. The resulting post-to-pre MSPE ratio of 0.29, well below 1, indicates that model fit actually improves after the reform. Taken together, this pattern provides little evidence that the adoption of partisan elections measurably affected dissent rates on the North Carolina Supreme Court.

### Pretreatment Covariate Balance

A second limitation concerns the distribution of donor weights. The synthetic control algorithm assigns 100 percent of the donor pool weight to Minnesota. This eliminates one of SCM’s core advantages, as the algorithm constructs a counterfactual as a weighted composite of multiple comparison units. Although it is not uncommon for SCM to allocate weight unevenly across donors, or to exclude some entirely, such concentration is substantively reassuring only when the selected unit closely matches the treated unit on pre-treatment characteristics. This condition is not met in the present study. The full weight placed on Minnesota does not signal that its supreme court provides a strong predictive match for North Carolina. Rather, it reflects the algorithm’s constrained optimization under conditions of poor pretreatment balance. 

\begin{table}[h!]
\captionsetup{justification=raggedright, singlelinecheck=false, skip=5pt}
\caption{Covariate Balance Between Treated and Synthetic North Carolina}
\label{tab:covariate_balance}
\centering
\begin{tabular}{lccc}
\hline
\rule{0pt}{3ex}\textbf{Covariate}
& \textbf{Treated (NC)}
& \textbf{Synthetic NC}
& \textbf{Sample Mean} \\[1ex]
\hline
Campaign Finance        & 1,348,421 & 177,336 & 381,739 \\
Court Professionalization & 0.609 & 0.610 & 0.612 \\
Capital Appeals         & 0.167 & 0.333 & 2.548 \\
Lower Court Capital Appeals & 1.000 & 0.500 & 1.548 \\
Criminal Procedure Docket & 0.458 & 0.129 & 0.519 \\
Ideological Spread      & 2.283 & 1.964 & 1.291 \\
Citizen Ideology        & 3.903 & 4.161 & 3.933 \\
Government Ideology     & 0.240 & -0.093 & 0.147 \\
Term Length             & 8.000 & 6.000 & 7.429 \\
Number of Justices      & 7.000 & 7.000 & 7.286 \\
Election Structure      & 0.000 & 0.000 & 0.143 \\
Electoral Competition   & 0.667 & 0.000 & 0.167 \\
Published Opinions      & 1,057 & 657 & 224 \\
\hline
\end{tabular}
\end{table}

The court serving as the sole contributor to the counterfactual bears limited structural resemblance to the treated court across several dimensions. As Table \ref{tab:covariate_balance} shows, 11 of 14 covariates exceed the conventional 0.25 standardized difference threshold, indicating substantial imbalance. The discrepancies are especially pronounced in campaign finance ($1.35 million versus $177,336), criminal procedure dockets (0.458 versus 0.129), capital appeals (0.167 versus 0.333), and electoral competition (0.667 versus 0.000). These differences suggest that, despite receiving full weight in constructing the synthetic North Carolina Supreme Court, Minnesota’s institutional and political context diverges meaningfully from North Carolina’s prior to reform. This limitation is not unique to the present study. Although Renberg does not explicitly discuss it, her synthetic control model shows similar imbalances, including substantial overestimation of published opinions (by 92–494 percent), underestimation of criminal procedure dockets by roughly 50 percent in Arkansas and Mississippi, and pronounced divergences in capital punishment caseloads [@Renberg2020]. 

This poor covariate balance may stem from the inherent homogeneity of state supreme courts, which violates the fundamental parallel trends assumption of SCM. North Carolina's Supreme Court is structurally unique: it can bypass the Court of Appeals and holds direct appellate jurisdiction over constitutional questions, statutory challenges, and other high-stakes matters. This structure generates a substantially higher volume of published opinions, which drives down dissent rates. Additionally, diverse responses to COVID-19 beginning in 2020, including closures, delayed proceedings, and shifts in case composition, may further complicate the analysis of dissent rates during the study period. This suggests that SCM may not be a robust method for studying dissent rates, and raises questions about the validity of Renberg’s conclusions regarding the impact of selection mechanisms on dissent behavior and judicial independence.

Moreover, additional sensitivity tests including leave-one-out, placebo, and year-by-year analyses further illuminate the fragility of causal inference in this setting. Conducted by systematically excluding each donor court one at a time and recalculating the treatment effect, the leave-one-out analysis undermines confidence in the results. A robust causal estimate should remain stable across reasonable variations in model specification. By contrast, excluding each donor state supreme court produces treatment effects ranging from -0.1887 (Minnesota excluded) to -0.0875 (Wisconsin excluded), with a mean of -0.1617 and standard deviation of 0.0382. Each leave-one-out specification produces a negative treatment effect, yet the optimal weighted combination yields exactly zero. This pattern indicates that the zero treatment effect is an artifact of the specific weighting scheme rather than a robust finding.

Additionally, comparing optimal synthetic control weights decided by the algorithm to artifically equalized weights reveals no difference in results. Both methods produce an estimated average treatment effect (ATE) of 0.00, indicating no mean difference in dissent rates between North Carolina and the synthetic control across all post-treatment years. This equivalence suggests that the sophisticated weighting algorithm provides no advantage over a simple average of control courts, indicating that no weighting scheme can adequately address the severe covariate imbalances.

Lastly, examining year-by-year treatment effects reveals substantial temporal instability. The estimated effect of partisan elections on dissent rates varies dramatically across post-treatment years: 2018 (-0.0123), 2019 (-0.0150), 2020 (+0.0068), 2021 (-0.0005), 2022 (+0.0270), 2023 (-0.0135), 2024 (+0.0078). These estimates range from -0.015 to +0.027 with a standard deviation of 0.0152, nearly as large as the effects themselves. If partisan elections truly increased dissenting behavior through electoral accountability mechanisms, we would expect a sustained, consistent effect following the 2018 reform. Instead, the effects fluctuate in both direction and magnitude across years, suggesting that any apparent treatment effects likely reflect random variation or temporary fluctuations. Additionally, COVID-19 disruptions may have introduced temporal shocks that affect the analysis independently of electoral reform.

Altogether, the poorly fitted MSPE, lopsided weighting of donor courts, pretreatment imbalances, and failed sensitivity tests highlight important limitations in using SCM to assess the causal impact of electoral reform on dissenting behavior. The pre- and post-treatment MSPE values indicate that the synthetic control provides only a weak approximation of North Carolina’s dissent trajectory. The synthetic control relies entirely on Minnesota, which bears limited structural resemblance to North Carolina. Leave-one-out sensitivity tests and comparisons with equalized donor weights show that the estimated treatment effect is highly sensitive to the specific donor combination. Year-by-year estimates further demonstrate substantial temporal instability. While the pretreatment placebo tests suggest that the zero treatment effect in 2018 is significantly distinguishable from other years during the pre-treatment period, this result must be interpreted cautiously given the scarcity of comparable control units, low-variance outcomes, substantial covariate imbalances, and hypothesized treatment effects that are small relative to secular trends and measurement variability. Collectively, these findings highlight the limitations of SCM in this context and the broader challenges of studying dissent rates in highly heterogeneous state supreme court systems.

### Textual Analysis

Beyond the constraints already discussed, dissent rates alone provide only a limited perspective on how electoral reform shapes judicial behavior. While the prevalence of dissent indicates whether justices disagree with the majority, it does not reveal the depth, substance, or reasoning underlying those disagreements. Accordingly, this section presents a computational textual analysis of judicial dissents, enabling an assessment of how electoral reform influences the substantive content of judicial reasoning. In particular, the analysis examines how different election mechanisms affect both the political and legal tenor of justices’ dissents.

### Wordscores Seed Dictionaries

![Seed word dictionaries (font size proportional to difference scores) \label{wordclouds}](figures/seed_wordclouds.png)

The resulting seed terms shown in \ref{wordclouds}. Both dictionaries were manually reviewed, and a small number of generic terms or words reflecting parsing errors were excluded. Words in the ideological dictionary reflect the tendency of justices with extreme PAJID scores to engage with constitutional issues and contested legal domains. Terms such as *search, warrant, police,* and *prosecution* reflect Fourth Amendment framing and the exercise of state power; *regulation, legislative, administrative,* and *agency* characterize debates over the scope of government authority; and *drug, harm,* and *parent* mark substantively contested criminal and family law domains shaped by ideological priors. Framing terms like *individual, government, people, protect, justify,* and *risk* indicate whom the law serves and on what grounds, while *meaning* and *challenge* reflect interpretive and adversarial reasoning. 

In contrast, the conventional dictionary reflects the tendency of justices with more centrist PAJID scores to focus on civil matters while emphasizing collegiality and procedural deference. Commercial and civil law terms such as *contract, tort, accident, damage, award,* and *property* anchor opinions in technically oriented domains of lower ideological salience. Dispositional vocabulary including *reverse, remand, dismiss, deny,* and *grant* reflects procedural resolution rather than substantive constitutional engagement, and collegial terms such as *respectfully* signal deference to institutional norms. For example, the Harvard Law Review talks extensively about a powerful and historical consensus norm that motivates dissent to be particularly apologetic and reference respectfulness, attributing this rhetoric to dissenting Justices' felt obligations to justify their deviation from the status quo [@HarvardLawReview2011]. Party and role terms including *claimant, appellant,* and *attorney* further reinforce the conventional dictionary's orientation toward procedural rather than ideological reasoning.

### Word2Vec Dictionary Expansion

![Semantic space around "respectfully "\label{semantic_corner}](figures/semantic_corner_plot.png)

The seed dictionaries were expanded using Word2Vec to compute cosine similarity between a seed word's vector and all other word vectors in the embedding space, adding semantically related terms that Wordscores may have missed due to insufficient frequency in the reference corpora. \ref{semantic_corner} visualizes the 30 words most semantically similar to a conventional seed word, *respectfully*, projected into two-dimensional space using Principal Component Analysis (PCA). The cluster reveals that *respectfully* associates primarily with procedural and collegial terminology, *dissent, concur, dissenting, concurring, affirm, majority, disagree, join, colleague,* and *reverse.* The inset map (top right) situates this semantic cluster within the full embedding space of all words in the model, illustrating how the Word2Vec model captures the contextual meaning of associated words.

### Rhetoric Scores Results

To assess whether judicial rhetoric has shifted over time, a panel OLS regression of annual mean rhetoric scores on year was estimated separately for each selection mechanism, with state fixed effects and standard errors clustered by state. The overall trend is negligible and statistically insignificant ($\beta$ = -0.0004, $p$ = 0.110), indicating no secular drift in rhetoric across the full sample once state-level heterogeneity is accounted for. Within-mechanism trends are similarly flat: partisan ($\beta$ = 0.0005, $p$ = 0.872), nonpartisan ($\beta$ = -0.0013, $p$ = 0.414), and appointment ($\beta$ = 0.0004, $p$ = 0.852) courts show no detectable rhetorical trend over time. The sole exception is retention election courts, which exhibit a statistically significant negative trend ($\beta$ = -0.0037, $p$ = 0.017), indicating a modest drift toward more ideological rhetoric over time among courts using retention elections.

### Level Differences by Selection Mechanism

![Rhetoric scores over time by selection mechanism](figures/rhetoric_by_mechanism.png)

To assess whether selection mechanisms predict rhetoric levels, a panel OLS regression of annual mean raw rhetoric scores on mechanism dummies was estimated with state fixed effects, a linear year control, and standard errors clustered by state. The analysis is restricted to the eleven states that switched mechanisms at least once during the study period, as these are the only states for which within-state variation in mechanism can identify level effects net of time-invariant court characteristics. Nonpartisan elections serve as the reference category.

The unadjusted raw means suggest that elected courts write more conventionally than appointed courts. Counterintuitively, partisan courts produce the most conventional rhetoric (mean = 0.141), followed by nonpartisan courts (0.009), retention courts (-0.069), and appointment courts (-0.116). Once state fixed effects are included, the pattern reverses and strengthens considerably. Appointment courts produce significantly more ideological rhetoric than nonpartisan courts ($\beta$ = -0.286, SE = 0.056, $t$ = -5.12, $p$ < 0.001), as do retention courts ($\beta$ = -0.199, SE = 0.050, $t$ = -3.95, $p$ < 0.001). Partisan election courts trend toward more conventional rhetoric relative to nonpartisan courts ($\beta$ = 0.109, SE = 0.059, $t$ = 1.84, $p$ = 0.066), though this result falls just short of conventional significance thresholds. These findings suggest that the meaningful institutional divide in judicial rhetoric runs between courts insulated from electoral pressure and those subject to any form of electoral accountability, rather than between partisan and nonpartisan systems specifically.

### Event Study: Selection Mechanism Switches

To examine the rhetorical consequences of mechanism changes more directly, a pre/post comparison examines detrended rhetoric scores in the six years before and after each of the twelve selection mechanism switches occurring among the 50 courts between 1965 and 2019. A two-sample $t$-test assesses whether the post-switch mean differs significantly from the pre-switch mean within a $\pm$ 6 year window around each switch.

The clearest individual result is Florida's 1971 transition from partisan to retention elections ($\Delta$ = -0.264, $p$ = 0.029), which produced a statistically significant shift toward more ideological rhetoric following the removal of contested partisan competition. Arizona's 1974 transition from nonpartisan to retention elections shows a similar directional pattern ($\Delta$ = -0.269, $p$ = 0.087), as does Utah's 1985 transition ($\Delta$ = -0.163, $p$ = 0.052). Among all seven transitions toward retention elections, six of seven produce negative differences, indicating more ideological rhetoric post-switch, with a mean difference of -0.122. A sign test finds this pattern marginally consistent with a systematic effect ($p$ = 0.125), though the small sample limits power.

Among the four states transitioning from partisan to nonpartisan elections, including Kentucky, Mississippi, West Virginia, and North Carolina 2002, three of four produce negative differences, with a mean of -0.077, though none individually reach significance. Vermont's 1974 appointment-to-retention transition moves in the opposite direction ($\Delta$ = +0.358), though this result is not statistically significant ($p$ = 0.464).

North Carolina provides the closest available natural experiment, having switched selection systems twice in opposite directions. The 2002 switch away from partisan elections was followed by more ideological rhetoric ($\Delta$ = -0.150), while the 2018 reinstatement of partisan elections was also followed by more ideological rhetoric ($\Delta$ = -0.097), though neither result reaches significance. The absence of a mirror-image pattern across both North Carolina switches is inconsistent with a simple partisan-label effect and reinforces the panel regression's null finding for the partisan versus nonpartisan comparison.

Taken together, the panel and event study results point toward a consistent conclusion. The statistically robust finding is that electoral accountability in any form — including mild retention elections — is associated with more conventional judicial rhetoric relative to appointment, once between-state differences are controlled. The partisan versus nonpartisan distinction, which motivates current reform debates, does not produce a detectable or consistent rhetorical difference in either the panel regression or individual event studies. These findings suggest that the institutional divide that matters most for judicial rhetoric runs between insulated and electorally accountable courts, rather than between partisan and nonpartisan electoral systems specifically.

Potentially, selection mechanisms may not change the way justices write because they do not have to do any signalling in their opinions at all. The party heuristic may be stronger than all else.

## Conclusion

Conclusion

\newpage

## References

::: {#refs}
:::

\newpage

## Appendix

\begin{landscape}
\begin{table}[p]
\centering
\caption{Comparison of Dissent Rate Measurement Methods Across Courts (1995-2010)}
\label{tab:dissent_rates_replication}
\begin{tabular}{l*{9}{r}}
& \multicolumn{3}{c}{\textbf{Hall \& Windett (2013)}} & \multicolumn{3}{c}{\textbf{OpinionBy \& DissentBy}} & \multicolumn{3}{c}{\textbf{AND NOT Method}} \\
\cmidrule(lr){2-4} \cmidrule(lr){5-7} \cmidrule(lr){8-10}
\textbf{Court} & Opinions & Dissents & Rate & Opinions & Dissents & Rate & Opinions & Dissents & Rate \\
\midrule
NC & 13,241 & 154 & 0.0116 & 15,660 & 159 & 0.0102 & 10,687 & 156 & 0.0146 \\
OR & 1,155 & 143 & 0.1238 & 1,074 & 325 & 0.3026 & 331 & 91 & 0.2749 \\
WV & 2,218 & 765 & 0.3449 & 1,253 & 678 & 0.5411 & 351 & 163 & 0.4644 \\
MO & 1,874 & 267 & 0.1425 & 3,271 & 533 & 0.1629 & 484 & 75 & 0.1550 \\
MA & 2,808 & 172 & 0.0613 & 2,731 & 534 & 0.1955 & 780 & 152 & 0.1949 \\
ME & 3,233 & 227 & 0.0702 & 2,464 & 408 & 0.1656 & 1,002 & 136 & 0.1357 \\
IL & 2,302 & 616 & 0.2676 & 1,685 & 630 & 0.3739 & 399 & 141 & 0.3534 \\
ID & 2,119 & 244 & 0.1151 & 2,141 & 439 & 0.2050 & 551 & 110 & 0.1996 \\
HI & 2,086 & 282 & 0.1352 & 1,768 & 389 & 0.2200 & 661 & 86 & 0.1301 \\
AZ & 1,546 & 167 & 0.1080 & 2,802 & 241 & 0.0860 & 336 & 39 & 0.1161 \\
AK & 2,506 & 272 & 0.1085 & 1,923 & 269 & 0.1399 & 543 & 66 & 0.1215 \\
AL & 5,185 & 1,423 & 0.2744 & 4,474 & 1,418 & 0.3169 & 1,626 & 563 & 0.3462 \\
\bottomrule
\end{tabular}
\end{table}
\end{landscape}
[SLIDE 1: Title Slide - Collection of Underground App Distribution URLs on Telegram]

(0:00-0:15) - Speaker Introduction
"Good morning/afternoon, everyone. Thank you for being here. My name is ZixinLin, and today I'm excited to share our project titled 'Collection of Underground App Distribution URLs on Telegram'. This work was done in collaboration with my teammates — Yingqi Li, Xizhe Zhu, Zicong Wu, and Jizhou Qin."

[SLIDE 2: Content Overview]

(0:15-0:30) - Agenda
"Over the next 15 minutes, we'll cover the introduction and motivation for this research, some background on Telegram and its ecosystem, our methodology for data collection, a brief look at where our data analysis currently stands, and finally, the challenges we faced and our conclusions."

[SLIDE 3: Section Separator - Introduction]

(0:30-0:35) - Transition
"So, let's begin with the Introduction."

[SLIDE 4: Introduction - Part 1: The Problem]

(0:35-1:35) -Telegram is widely known as a messaging app with features like end-to-end encryption and anonymous user identity. But these very features, combined with weak content moderation, have also made it a hotspot for the distribution of underground mobile applications—apps that are banned or restricted on mainstream platforms like Google Play and the App Store. These include pornographic content, gambling platforms, pirated software, and more dangerously, apps that are used for fraud, phishing, and large-scale privacy violations. On the screen, you can see two real-world examples. The first is a Reuters report on how criminal networks in Southeast Asia are thriving on Telegram’s so-called underground markets. The second is from Mashable, showing how revenge porn has been widely circulated through Telegram, leaving victims in helpless situations. These are not isolated incidents—they reflect a larger pattern of abuse enabled by Telegram’s infrastructure, especially the use of bots and channels that allow such content to spread quickly and at scale. This growing threat makes it all the more urgent to understand how these apps are being disseminated, which is the core motivation behind our research.

[SLIDE 5: Introduction - Part 2: Project Aims]

(1:35-2:35) - Project Goals
"This brings us to the core objectives of our project. Our primary goal is to systematically collect, extract, and identify Telegram URLs that are actively involved in the distribution of these underground applications. We're doing this through a multi-stage, automated approach, aiming to build a solid dataset for further in-depth analysis.

Specifically, our key aims include:
First, discovering relevant underground Telegram channels. We achieve this by using search bots and carefully selected keywords.
Second, extracting all URLs embedded within the historical messages of these discovered channels.
Third, identifying which of these URLs lead to actual app download pages. This involves analyzing the content of the landing pages for keywords like 'download,' 'Android,' 'iOS,' and so on.
A crucial deliverable for us is to validate and collect at least 200 effective app download URLs.
<!-- And finally, we will compile a comprehensive final report. This report will detail the channels we found, the validated download URLs, our complete technical workflow, and the key findings from our investigation." -->

[SLIDE 6: Section Separator - Background]

(2:35-2:40) - Transition
"Now, let's delve a bit into the background to better understand the context."

[SLIDE 7: Background - Telegram Ecosystem]

(2:40-3:40) - Understanding Telegram's Role
Telegram now serves over 800 million users worldwide, and while it's widely used for legitimate communication, certain features make it highly attractive for underground use. It supports public and private channels that can broadcast to millions. It allows anonymous interaction, lacks effective moderation, and enables mass forwarding—which means malicious or illegal content can spread almost instantly. Over time, this has turned parts of Telegram into a fully functioning cybercrime ecosystem. On the screen, the left image shows a typical pornographic gambling platform—it’s openly advertised with sexualized content to attract users. The right one is also disturbing: it’s a large channel leaking personal information—names, phone numbers, even ID data—essentially a “data breach dump” for sale or exploitation. And honestly, these are just the more ‘presentable’ examples we could show. Many other groups we encountered were so graphic or exploitative that we decided not to include them in the slides. But they are very real—and very active—inside the Telegram ecosystem.

[SLIDE 8: Background - Bots in Telegram]

(3:40-4:30) - The Role of Bots
"Bots are a significant part of the Telegram ecosystem. Telegram’s Bot API allows developers to create automated tools for a wide variety of purposes. In our context, 'search bots' are particularly relevant. These bots function like internal search engines, providing users with channel recommendations based on keywords.

What's crucial to understand is that many underground actors actually buy keyword slots from these search bot operators. For example, they might pay to have their channel appear when someone searches for "VPN," "Baccarat," or other specific terms. This means that channels listed under these paid results are strategically boosted, effectively gaming the system to reach much wider audiences than they might organically. You can see on the screen how these bots present search results, often mixing organic and promoted content."

[SLIDE 9: Background - App Packages (APK/IPA)]

(4:30-5:30) - Technicals of App Distribution
"To understand how these apps are distributed, it's also helpful to briefly touch upon app package formats. Android and iOS, the two dominant mobile operating systems, use different approaches.

Android is generally more open. It uses the .apk (Android Package Kit) format. Critically, users can 'sideload' apps – meaning they can install them from unofficial sources outside the Google Play Store, such as direct web links, files shared on Telegram, or third-party marketplaces. This openness is what underground developers often exploit to bypass official vetting processes.

iOS, on the other hand, is more of a closed ecosystem. Apps are packaged as .ipa files and installation is typically restricted to the official App Store. However, it's not impenetrable. Alternative channels do exist, such as TestFlight, which is Apple's platform for beta testing apps. Others include enterprise signing certificates, which can be misused, and WebClips, which are essentially browser shortcuts that can mimic app behavior or lead to web-based app installations."

[SLIDE 10: Section Separator - Methodology]

(5:30-5:35) - Transition
"With that background in mind, let's move on to our methodology."

[SLIDE 11: Methodology - Workflow Overview]

(5:35-6:35) - Our Approach: Three Key Stages
"Our workflow for this project, as illustrated in the diagram, can be broken down into three key stages.

First, Identifying Relevant Channels. We started by leveraging Telegram bots, querying them with a curated list of keywords related to underground apps. This initial step was designed to cast a wide net and discover channels likely to be involved in illicit app distribution. This yielded over 200 channels that we then flagged for deeper investigation.

Second, Gathering Possible URLs. Once we had our list of target channels, we systematically collected and parsed their message histories. From this vast amount of data, we extracted over 10,000 potential URLs that linked to external resources – these could be anything from direct download links to landing pages.

Third, App Collection and Validation. In this stage, we filtered and validated these links. Using both traditional link analysis and OCR-based recognition on linked content, we’ve confirmed over 300 valid URLs that lead to underground mobile applications. These include everything from pirated streaming apps to modified gambling platforms.

[SLIDE 12: Methodology - Step 1: Collect Bots and Channels]

(6:35-7:35) - Channel Discovery Details
"Let's look at Step 1 in more detail. To interact with Telegram programmatically, we registered a developer account to obtain the necessary api_id and api_hash. We then used the Telethon library, a Python client for the Telegram API.

Our first task was to identify influential search bots. We manually collected a list of the top 15 commonly used Telegram search bots, like @hao1234bot for example.
Then, we compiled an extensive list of keywords, covering both Chinese and English terms. These keywords were chosen based on common types of underground apps and services, such as 'VPN,' '91' (a known code for adult content), 'Crack,' 'porn,' and '百家乐' (Baccarat, a gambling term).

The Python snippet on the slide shows a part of our script where we load these keywords, shuffle them, and then send them to the conversation interface of a search bot to retrieve channel suggestions."

[SLIDE 13: Methodology - Step 2: Extract URLs from Channels]

(7:35-8:25) - URL Extraction Details
"Once we identified relevant channels through the bots, Step 2 involved extracting URLs from their messages. Again, using Telethon, we iterated through the message history of each channel. Due to API considerations and to keep the data manageable, we set a limit of processing up to 1000 of the most recent messages per channel.

Within each message, we parsed its entities to find any embedded URLs, specifically looking for t.me/... links which are internal Telegram links, often used to cross-promote other channels or lead to user profiles, but also external HTTP/HTTPS links which might lead to download pages. The regex snippet shows the basic pattern for finding these t.me links. We also implemented error handling and logic to avoid crawling outdated or inactive links to make the process more efficient. All extracted URLs were then collected for the next stage."

[SLIDE 14: Methodology - Step 3: Identify App Pages]

(8:25-9:25) - App Page Identification and Validation
"Step 3 is focused on sifting through the thousands of collected URLs to identify actual app download pages.
First, we performed an initial filtering to remove obviously irrelevant domains or duplicates, which helped to narrow down the search space.
For the remaining URLs, we automated the process of opening each one using a headless version of the Chrome browser, controlled by Selenium. This allows us to interact with web pages programmatically.

A key part of our validation involves capturing screenshots of these pages. We programmed the browser to automatically click on common call-to-action buttons often found on download pages, such as those labeled '进入' (Enter), 'Continue,' or similar, before taking the screenshot. This helps reveal the true content of the page if it's hidden behind an initial interaction.

Finally, we apply Optical Character Recognition, or OCR, using the PaddleOCR library, to analyze these screenshots. The OCR extracts all visible text from the image, and we then search this text for keywords indicative of an app download page, such as 'download,' 'iOS,' 'apk,' 'android,' or 'app.' The images on the slide show some examples of these landing pages where such keywords were found."

[SLIDE 15: Section Separator - Data Analysis]

(9:25-9:35) - Transition to Data Analysis
"This methodology has allowed us to gather a significant amount of raw data. Now, let's briefly touch upon the Data Analysis phase."

[SLIDE 16: Data Analysis – Validity & Distribution]

"Now let’s take a closer look at our analysis results.

Starting with URL validity: Out of more than 10,000 extracted URLs, only 2.8% were confirmed as valid underground app distribution links. That’s just over 300. This low hit rate reflects the noise and obfuscation tactics used by underground actors — for example, many of the remaining links led to irrelevant content like porn aggregator sites, expired pages, or unrelated blockchain news hubs.

Moving to platform distribution: Among those 300 valid cases, we observed a strong skew toward Android, which accounts for 72.8% of the apps. This isn't surprising. Android allows sideloading and doesn’t enforce a centralized app review process like Apple’s App Store does. That makes it far more accessible for underground developers.
iOS was the second most targeted, at 16.6%, with a small portion of apps being cross-platform."

[SLIDE 16: Categories & Summary]

"When we categorize these apps by type, the dominant themes are immediately clear.
The largest share goes to gambling and pornographic applications. These are well-established verticals in the underground mobile scene due to high user demand and profitability.
Pirated software — including cracked tools, modified apps, and premium services with licensing bypassed — makes up about 17.8% of valid URLs.
We also identified a smaller but notable portion — about 13.8% — focused on AI utilities and Web3-related apps, including crypto wallets and DeFi tools. These often promise anonymity or profit but are difficult to verify.

So, in summary:
Out of thousands of links, only a small fraction were truly relevant. Yet even this small subset reveals a clear pattern — underground Telegram channels are primarily distributing high-risk, policy-violating content, and doing so in a way that favors the open Android ecosystem. This tells us that Telegram isn't just a passive host — its infrastructure actively enables this kind of app proliferation at scale."

[SLIDE 17: Section Separator - Conclusion]

(10:05-10:10) - Transition to Conclusion
"Let's now move to the conclusion and discuss some of the challenges we encountered."

[SLIDE 18: Conclusion - Challenges Encountered]

(10:10-11:40) - Overcoming Hurdles
"No research project is without its challenges, and ours was no exception.

One significant hurdle was Bot Interaction Rate Limiting. When we were aggressively probing the search bots with numerous keywords, Telegram's anti-spam mechanisms sometimes temporarily banned our IP or account. To mitigate this, we introduced randomized delays between interactions using asyncio.sleep and implemented timeouts for bots that weren't responding, making our collection process more robust and less disruptive.

Another issue was Entity Type Ambiguity. Links like t.me/... can point to different types of Telegram entities – a public channel, a private chat, or a user profile. The Telethon API requires specific handling for each type. We had to develop heuristic algorithms to correctly identify the entity type before attempting to access its message history, ensuring our crawler could operate safely and effectively.

We also encountered Region Restrictions on some content. Certain channels or download pages were inaccessible from our default location. We addressed this by employing VPN tunneling to route our traffic through different geographical regions and sometimes used alternate Apple ID environments to simulate being in a compliant locale for iOS-related content.

And on a more personal note, there's the mental health aspect. I was the only female member in our team, and frankly, some moments were hard to stomach. Sifting through this ecosystem — seeing large-scale malicious channels with massive subscriber bases, or scams that manipulate people’s desperation — felt like watching a curtain get ripped open on a very dark corner of the internet.
It was painful at times and my world shattered a little.
You can even see it in some of the… colorful messages we came across. These weren’t just abstract threats — they were real, manipulative, sometimes explicitly abusive content.
It reminded me that cybersecurity isn’t just about code and systems — it’s about protecting people. And that makes it all the more important.

[SLIDE 19: Conclusion - Summary and Future Work]

(11:40-13:10) - Key Takeaways and Next Steps
"So, to conclude, in this project, we successfully implemented a automated pipeline designed to identify Telegram channels that are actively promoting underground mobile applications.

Our method is a multi-pronged approach, combining bot-driven discovery of channels, regex-based extraction of URLs from messages, the use of a headless browser to capture dynamic webpage content as screenshots, and OCR-based keyword recognition to validate app download pages.
Through this process, we have been able to extract and filter over 200 high-signal URLs that are directly linked to illicit application distribution. This is a significant step towards quantifying the scale of this problem.

These findings are important because they help uncover Telegram’s often-overlooked role in the unregulated dissemination of mobile apps. This is particularly relevant in regions like Chinese-speaking contexts, where stricter official censorship often drives users and distributors to alternative platforms like Telegram.

Looking ahead, this pipeline provides a strong foundation for future work. We envision several possible extensions.
First, we could expand our coverage beyond public channels — into private groups, closed channels, or even direct interactions with bots. These are harder to reach, but potentially hold more covert or coordinated behavior.
Second, by incorporating semantic analysis of message patterns, we could begin to detect coordinated campaigns or recurring scam strategies, adding another layer of intelligence.
And third, we see value in leveraging visual cues from screenshots — things like app UI elements, repeated banners, or warning signs — to build automated classifiers that can assess risk levels or flag suspicious content proactively.
Together, these directions could push us closer to real-time moderation tools that not only monitor Telegram’s ecosystem, but actually help shape safer online environments.

[SLIDE 20: Section Separator - References]

(13:10-13:15) - Acknowledging Sources
"Finally, our work builds upon existing research and utilizes several key technologies."

[SLIDE 21: References]

(13:15-13:30) - Displaying References
"Here are some of the core academic papers, technical documentation, and industry reports that informed our approach and provided valuable context for this project. I won't go through them individually, but they are here for your reference."

[SLIDE 22: End Slide - Thank You / Q&A]

(13:30-15:00) - Closing and Q&A
"That concludes my presentation on our efforts to collect underground app distribution URLs on Telegram. We believe this research provides valuable insights into a growing area of concern and offers a methodology that can be further developed to combat the spread of malicious and unwanted applications.

Thank you very much for your time and attention. I’d be happy to answer any questions you may have."
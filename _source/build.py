#!/usr/bin/env python3
"""Builds the FoVL notes site from HTML fragments in src/ into ../fovl-site/."""
import os, html, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..')

PARTS = [
 ("V", "Part 0 — Vision (course intro)", "Dr. Divya Saxena's opening lecture: what computer vision is and how it grew from Marr to CLIP."),
 ("A", "Part A — Language, Information & Classical NLP", "Dr. Sidharth Ranjan's lectures: what language is, how to measure it, and the classic statistical toolkit."),
 ("B", "Part B — Neural NLP", "From a single neuron to word embeddings, RNNs, attention, and real applications."),
]

MODS = [
 # slug, part, title, lede, lectures
 ("00-computer-vision-intro","V","Computer Vision: The Big Picture","Marr's stages, SIFT and HOG, ImageNet and deep learning, segmentation, and CLIP joining images with text.","Vision intro slides (Introduction_Part1)"),
 ("01-what-is-language","A","What is Language?","Language as a window to the mind: symbols, meaning, the inner and outer world, and why language is slippery.","Language Lecture 1 (+ start of Lecture 2)"),
 ("02-can-machines-understand","A","Can Machines Understand Language?","Marr's three levels, the Turing test and the Total Turing test — how to even ask the question properly.","Language Lecture 2"),
 ("03-nlp-nlu-cl","A","NLP vs NLU vs Computational Linguistics","ELIZA vs SHRDLU, the recipe for building an NLU system, ambiguity, and the 'NLP trinity'.","Language Lecture 3"),
 ("04-zipfs-law","A","Zipf's Law: The Shape of Language","Why 'the' is everywhere and most words are rare — and what that says about human effort.","Language Lecture 4a"),
 ("05-shannon-redundancy","A","Shannon, Redundancy & Entropy","How a wartime engineer measured information using English itself — and why you can read 'fll n th blnks'.","Language Lectures 4b & 5"),
 ("06-information-theory","A","The Information-Theory Toolkit","Entropy, joint & conditional entropy, chain rule, mutual information and KL divergence — with worked numbers.","Language Lecture 6"),
 ("07-ngram-language-models","A","N-gram Language Models & Perplexity","Turning counts into probabilities, scoring sentences, perplexity, smoothing and back-off.","Language Lectures 7 & 8"),
 ("08-pos-tagging-syntax","A","POS Tagging, HMMs & Syntax","Tagging words with HMMs, chunking, and the two ways to draw a sentence's structure.","Language Lecture 9"),
 ("09-neural-network-basics","B","Neural Network Basics","Lines, losses and gradient descent — the engine inside every modern NLP model.","Neural NLP Lecture 1 (10 Oct)"),
 ("10-word2vec","B","Word Embeddings: word2vec","From one-hot vectors to dense meaning vectors: the skip-gram model, softmax and cross-entropy.","Neural NLP Lecture 2 (16 Oct)"),
 ("11-negative-sampling-glove","B","Negative Sampling & GloVe","Making word2vec fast, and learning meaning from co-occurrence ratios instead.","Neural NLP Lecture 3 (17 Oct)"),
 ("12-evaluating-embeddings","B","Evaluating Embeddings & Their Limits","Intrinsic vs extrinsic evaluation, FastText, bias, and why static vectors aren't enough.","Neural NLP Lecture 4 (19 Oct, part 1)"),
 ("13-neural-language-models","B","From N-grams to Neural Language Models","Count-based LMs, text generation, and the fixed-window neural LM.","Neural NLP Lectures 4–5 (19 & 23 Oct)"),
 ("14-rnns","B","Recurrent Neural Networks (RNNs)","One small network reused at every word: training, teacher forcing, BIO tagging, vanishing gradients, LSTM/GRU.","Neural NLP Lectures 5–6 (23 Oct & 13 Nov)"),
 ("15-seq2seq-attention","B","Seq2Seq & Attention","Machine translation with encoder–decoders, the bottleneck problem, and attention — with a full numeric example.","Neural NLP Lecture 6 (13 Nov)"),
 ("16-coreference-resolution","B","Coreference Resolution","Finding every mention of the same entity: mention-pair, mention-ranking, end-to-end and clustering models, plus B-Cubed scoring.","Neural NLP slides FOVL4 (Nov)"),
 ("17-question-answering","B","Question Answering Systems","Factoid vs complex QA, the IR-based pipeline, ranking, MRR and dense retrievers.","Neural NLP Lecture 7 (15 Nov, part 1)"),
 ("18-sentiment-analysis","B","Sentiment & Aspect-Based Analysis","Opinions, attitudes, sarcasm, lexicons, and aspect-based sentiment with LSTMs and attention.","Neural NLP Lecture 7 (15 Nov, part 2)"),
 ("19-exam-cheatsheet","C","Exam Cheat-Sheet & Formula Bank","Every key formula, the topics the instructors flagged, and quick self-test questions.","All lectures"),
]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'

def head(title, prefix):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="Simple, example-first notes for Foundations of Vision and Language (FoVL) — language & NLP part.">
{FONTS}
<link rel="stylesheet" href="{prefix}assets/style.css">
<script src="{prefix}assets/app.js"></script>
</head>'''

def topbar(prefix, menu=True):
    mb = '<button class="btn menu-btn" id="menuBtn" aria-label="Open menu">☰ Topics</button>' if menu else ''
    return f'''<header class="topbar"><div class="in">{mb}<a class="brand" href="{prefix}index.html">FoVL <span>Notes</span></a><div class="spacer"></div><a class="btn hide-sm" href="{prefix}notes/19-exam-cheatsheet.html">Cheat-sheet</a><button class="btn" id="themeBtn" aria-label="Toggle dark mode">☾ Theme</button></div><div class="progress"></div></header>'''

def sidebar(cur_slug):
    out = ['<aside class="side">']
    for code, ptitle, _ in PARTS + [("C","Revision","")]:
        out.append(f'<h4>{html.escape(ptitle.split(" — ")[-1] if " — " in ptitle else ptitle)}</h4>')
        for i,(slug,part,title,_,_) in enumerate(MODS):
            if part!=code: continue
            n = slug.split('-')[0]
            cls = 'cur' if slug==cur_slug else ''
            out.append(f'<a class="{cls}" data-mod="{slug}" href="{slug}.html"><span class="n">{n}</span>{html.escape(title)}</a>')
    out.append('<h4>On this page</h4><nav class="toc" id="toc"></nav></aside>')
    return '\n'.join(out)

def footer():
    return '<footer class="foot">FoVL Notes · written from the course lecture recordings and slides (Foundations of Vision &amp; Language, IIT Jodhpur) · for revision, not a substitute for the slides.</footer>'

def build_page(idx):
    slug, part, title, lede, lec = MODS[idx]
    body = open(os.path.join(HERE,'src',slug+'.html'),encoding='utf-8').read()
    prev = MODS[idx-1] if idx>0 else None
    nxt = MODS[idx+1] if idx+1<len(MODS) else None
    pager = '<div class="pager">'
    pager += f'<a class="prev" href="{prev[0]}.html"><small>← Previous</small>{html.escape(prev[2])}</a>' if prev else '<a class="prev" href="../index.html"><small>← Back</small>All topics</a>'
    pager += f'<a class="next" href="{nxt[0]}.html"><small>Next →</small>{html.escape(nxt[2])}</a>' if nxt else '<a class="next" href="../index.html"><small>Done →</small>Back to all topics</a>'
    pager += '</div>'
    partname = {"V":"Part 0 · Vision intro","A":"Part A · Classical NLP","B":"Part B · Neural NLP","C":"Revision"}[part]
    num = slug.split('-')[0]
    page = f'''{head(title+" · FoVL Notes","../")}
<body data-page="{slug}">
{topbar("../")}
<div class="layout">
{sidebar(slug)}
<main><article class="article">
<div class="crumbs"><a href="../index.html">All topics</a> / {partname}</div>
<h1>{num}. {html.escape(title)}</h1>
<p class="lede">{html.escape(lede)}</p>
<div class="meta-row"><span class="chip">{partname}</span><span class="chip alt">🎙 {html.escape(lec)}</span></div>
{body}
<label class="done-row"><input type="checkbox" id="doneBox"> I've finished this topic</label>
{pager}
</article></main>
</div>
{footer()}
</body></html>'''
    open(os.path.join(OUT,'notes',slug+'.html'),'w',encoding='utf-8').write(page)

def build_index():
    cards = []
    for code, ptitle, pdesc in PARTS + [("C","Revision","One page with every formula and the topics flagged for the exam.")]:
        cards.append(f'<div class="partttl"><h2>{html.escape(ptitle)}</h2></div><p style="color:var(--muted);margin-top:0">{html.escape(pdesc)}</p><div class="grid">')
        for slug,part,title,lede,lec in MODS:
            if part!=code: continue
            n = slug.split('-')[0]
            cards.append(f'<a class="mod" data-mod="{slug}" href="notes/{slug}.html"><span class="n">{n}</span><h3>{html.escape(title)}</h3><p>{html.escape(lede)}</p><span class="lec">🎙 {html.escape(lec)}</span></a>')
        cards.append('</div>')
    page = f'''{head("FoVL Notes — Foundations of Vision & Language, explained simply","")}
<body data-page="home">
{topbar("", menu=False)}
<section class="hero">
<div class="chip">IIT Jodhpur · Foundations of Vision &amp; Language</div>
<h1>Big ideas of language &amp; NLP, explained like a story.</h1>
<p>Notes on every topic in the FoVL language lectures, from "what is language?" to attention and question answering, plus the vision intro. More than 60 diagrams and charts, drawn from the class numbers. Each idea comes in plain words first, then an everyday analogy and a worked example with real numbers. Each page also has a short "what it's for" table and every numerical done in class, plus extra practice questions.</p>
<div class="cta"><a href="notes/01-what-is-language.html">Start at topic 01 →</a><a class="ghost" href="notes/19-exam-cheatsheet.html">Jump to the cheat-sheet</a></div>
</section>
<div class="home">
<h2 style="border:0;margin-top:1em">How to read these notes</h2>
<div class="how">
<div class="box key"><span class="lbl">Key idea</span><p>The one sentence to remember.</p></div>
<div class="box an"><span class="lbl">Analogy</span><p>An everyday picture of the concept.</p></div>
<div class="box ex"><span class="lbl">Worked example</span><p>Real numbers, step by step.</p></div>
<div class="box exam"><span class="lbl">Exam tip</span><p>Things the instructors said to prepare.</p></div>
<div class="box try"><span class="lbl">Numericals</span><p>Every numerical from class, plus practice questions at the same level with hidden solutions.</p></div>
<div class="box key"><span class="lbl">What it's for</span><p>A short table on each page: why each concept exists and where it's used.</p></div>
</div>
<div class="tldr" style="margin-top:1.4em"><h3>The whole course in one breath</h3>
<p>Vision opens the course: from Marr's stages to CLIP, which links pictures and words (00). Language is a structured, predictable code for thoughts (01–03). Because it's predictable, we can <b>measure</b> it: Zipf's law describes its shape, and Shannon's entropy measures its surprise (04–06). Turn counts into probabilities and you get <b>language models</b> scored by perplexity (07). Add hidden tags and you get <b>HMM taggers</b> and syntax (08). Then neural networks learn <b>word vectors</b> (09–12), <b>RNNs</b> read sequences (13–14), <b>attention</b> lets a model look back at the important words (15), and the same tools power <b>coreference resolution</b>, <b>question answering</b> and <b>sentiment analysis</b> (16–18).</p></div>
{''.join(cards)}
</div>
{footer()}
</body></html>'''
    open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(page)

if __name__=='__main__':
    missing=[m[0] for m in MODS if not os.path.exists(os.path.join(HERE,'src',m[0]+'.html'))]
    for i,m in enumerate(MODS):
        if m[0] in missing: continue
        build_page(i)
    build_index()
    print('built', len(MODS)-len(missing), 'pages; missing:', missing)

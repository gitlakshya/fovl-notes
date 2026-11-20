"""All figures for the FoVL notes. Each entry: (file, heading text, figure html).
Numbers are computed here from the class data so the charts match the worked examples."""
import math, json, os
import numpy as np
from vizlib import *

HERE = os.path.dirname(os.path.abspath(__file__))
F = []   # (file, heading, html)

def add(file, heading, html): F.append((file, heading, html))

# ---------------------------------------------------------------- 00 vision
def timeline():
    ev = [(1966, 'Summer Vision\nProject (MIT)'), (1978, 'Marr: 2½-D\nsketch'), (1999, 'SIFT\nkeypoints'),
          (2005, 'HOG person\ndetector'), (2009, 'ImageNet\n15M images'), (2012, 'AlexNet:\ndeep CNNs win'),
          (2015, 'Detection &\nsegmentation'), (2021, 'CLIP & DALL·E:\nvision + language')]
    W, H = 900, 210
    o = line(40, 110, 870, 110, 'ax', 2)
    x0, x1 = 60, 850
    for i, (yr, lab) in enumerate(ev):
        x = x0 + i * (x1 - x0) / (len(ev) - 1)
        up = i % 2 == 0
        o += circle(x, 110, 7, 'c1')
        o += text(x, 134 if up else 96, str(yr), '', size=12, weight=700)
        ly = 40 if up else 158
        o += line(x, 110, x, ly + (22 if up else -6), 'grid', 1)
        for k, l in enumerate(lab.split('\n')):
            o += text(x, ly + k * 15, l, '', size=12)
    return fig('cv-timeline', W, H, o, 'A short history of computer vision, as told on the intro slides: from hand-designed features (SIFT, HOG) to learned features (CNNs on ImageNet) to models that join images and text (CLIP).')
add('00-computer-vision-intro.html', 'A short history', timeline())

def marr_pipeline():
    o = ''
    st = [('Input image', 'pixel intensities'), ('Primal sketch', 'edges, blobs, bars'),
          ('2½-D sketch', 'depth & surface\norientation (viewer-centred)'), ('3-D model', 'object-centred shape')]
    for i, (a, b) in enumerate(st):
        x = 20 + i * 215
        o += box(x, 40, 175, 62, a, 'bx1' if i in (0, 3) else 'bx')
        for k, l in enumerate(b.split('\n')):
            o += text(x + 87, 124 + k * 15, l, 'mut', size=11)
        if i < 3: o += arrow(x + 178, 71, x + 212, 71)
    o += text(450, 20, 'Marr (1970s): vision is computed in stages', '', size=13, weight=700)
    return fig('marr', 880, 165, o, 'Marr\'s stages of visual representation. "2½-D" because depth is known only for the surfaces you can see from where you stand: you see the front of the basketball, not its back.')
add('00-computer-vision-intro.html', 'Marr', marr_pipeline())

def seg_types():
    o = ''
    titles = ['Classification', 'Detection', 'Semantic segmentation', 'Instance segmentation']
    for k, t in enumerate(titles):
        x = 15 + k * 218
        o += text(x + 100, 18, t, '', size=12, weight=700)
        o += rect(x, 28, 200, 130, 'bx', 8)
        chairs = [(x + 30, 80), (x + 110, 70)]
        for j, (cx, cy) in enumerate(chairs):
            cls = 'c2' if k == 2 else (['c1', 'c3'][j] if k == 3 else 'chair')
            o += f'<rect x="{cx}" y="{cy}" width="50" height="45" rx="4" class="{cls}" opacity=".85"/>'
            o += f'<rect x="{cx}" y="{cy-30}" width="10" height="32" rx="3" class="{cls}" opacity=".85"/>'
            if k == 1:
                o += f'<rect x="{cx-6}" y="{cy-36}" width="62" height="88" rx="2" class="det" fill="none" stroke-width="2"/>'
                o += text(cx + 25, cy - 40, 'chair', 'acc', size=10, weight=700)
        if k == 0: o += text(x + 100, 150, '"chair"', 'acc', size=12, weight=700)
        if k == 2: o += text(x + 100, 150, 'all chairs = one colour', 'mut', size=10)
        if k == 3: o += text(x + 100, 150, 'each chair its own colour', 'mut', size=10)
    return fig('cv-tasks', 890, 170, o, 'Four vision tasks of increasing detail. Semantic segmentation knows <i>what</i> is a chair; instance segmentation also knows <i>which</i> chair.')
add('00-computer-vision-intro.html', 'Segmentation', seg_types())

def clip_fig():
    texts = ['a photo of a cat', 'a red motorcycle', 'a cup of coffee', 'a horse silhouette']
    imgs = ['cat', 'bike', 'coffee', 'horse']
    M = [[.31, .12, .10, .14], [.11, .33, .09, .12], [.09, .10, .29, .08], [.13, .12, .07, .30]]
    o = heat(10, 40, 90, 34, texts, ['🐱 img1', '🏍 img2', '☕ img3', '🐎 img4'], M, vmax=.33, rlabel_w=150)
    o += text(330, 18, 'Cosine similarity between text and image embeddings', '', size=12, weight=700)
    return fig('clip', 540, 185, o, 'CLIP puts captions and pictures in the same vector space. The matching pair (the diagonal) has the highest cosine similarity, exactly like word similarity in word2vec, but across two modalities. (Illustrative numbers in the style of the slide.)')
add('00-computer-vision-intro.html', 'CLIP', clip_fig())

# ---------------------------------------------------------------- 01 language
def layers():
    lv = [('Pragmatics & discourse', 'what the speaker means in context'), ('Semantics', 'meaning of words & sentences'),
          ('Syntax', 'how words combine into phrases'), ('Morphology', 'word parts: un-break-able'),
          ('Phonology', 'sound patterns of a language'), ('Phonetics', 'physical speech sounds')]
    o = ''
    n = len(lv)
    for i, (a, b) in enumerate(lv):
        w = 260 + i * 70
        x = 350 - w / 2
        y = 20 + i * 42
        o += rect(x, y, w, 36, 'bx1' if i % 2 == 0 else 'bx', 8)
        o += text(350, y + 16, a, '', size=13, weight=700)
        o += text(350, y + 30, b, 'mut', size=10.5)
    o += arrow(690, 270, 690, 30, 'ar', 2, None)
    o += text(700, 150, 'more abstract', 'mut', 'start', 11)
    return fig('lang-layers', 800, 285, o, 'The layers of language, from raw sound (bottom) to meaning in context (top). NLP systems work at every level: speech recognition at the bottom, chatbots at the top.')
add('01-what-is-language.html', 'The layers of language', layers())

def ambiguity_tree():
    o = text(380, 18, '"I saw the man with the telescope"', '', size=14, weight=700)
    for k, (title, att) in enumerate([('Reading 1: I used the telescope', 'saw'), ('Reading 2: the man had the telescope', 'man')]):
        x0 = 20 + k * 380
        o += text(x0 + 170, 48, title, 'acc' if k == 0 else 'ex', size=12, weight=700)
        words = ['I', 'saw', 'the man', 'with the telescope']
        xs = []; cx = []; x = x0 + 10
        for w_ in words:
            bw = len(w_) * 7.4 + 18
            o += box(x, 150, bw, 28, w_, 'bx', size=12)
            xs.append(x); cx.append(x + bw / 2); x += bw + 8
        tgt = cx[1] if att == 'saw' else cx[2]
        o += path(f'M{cx[3]:.1f},150 C{cx[3]:.1f},88 {tgt:.1f},88 {tgt:.1f},150', 'ln1' if k == 0 else 'ln3', 2.5)
        o += text((cx[3] + tgt) / 2, 92, 'attaches to "' + att + '"', 'mut', size=11)
    return fig('pp-attach', 780, 195, o, 'One sentence, two structures. The phrase "with the telescope" can attach to the verb (instrument) or to the noun (description). Symbols are ambiguous; context decides.')
add('01-what-is-language.html', 'ambiguous', ambiguity_tree())

# ---------------------------------------------------------------- 02 Marr / Turing
def marr_levels():
    rows = [('Computational', 'WHAT is the goal and why?', 'Add two numbers'),
            ('Algorithmic', 'HOW: which representation & steps?', 'Column addition with carry'),
            ('Implementation', 'WITH WHAT physical stuff?', 'Neurons / transistors / abacus')]
    o = text(130, 22, 'Level', 'mut', size=12, weight=700) + text(390, 22, 'Question it answers', 'mut', size=12, weight=700) + text(650, 22, 'Example: a calculator', 'mut', size=12, weight=700)
    for i, (a, b, c) in enumerate(rows):
        y = 36 + i * 54
        o += box(30, y, 200, 44, a, 'bx1')
        o += box(270, y, 240, 44, b, 'bx', size=12)
        o += box(550, y, 200, 44, c, 'bx', size=12)
        o += arrow(232, y + 22, 268, y + 22) + arrow(512, y + 22, 548, y + 22)
    return fig('marr-levels', 780, 205, o, 'Marr\'s three levels of analysis. The same computational goal can have many algorithms, and the same algorithm many implementations.')
add('02-can-machines-understand.html', "Marr's three levels", marr_levels())

# ---------------------------------------------------------------- 03 NLP/NLU/CL
def venn3():
    o = f'<circle cx="250" cy="120" r="95" class="vn1"/><circle cx="380" cy="120" r="95" class="vn2"/><circle cx="315" cy="190" r="70" class="vn3"/>'
    o += text(200, 90, 'NLP', '', size=15, weight=700) + text(200, 108, 'build useful', 'mut', size=11) + text(200, 122, 'language tools', 'mut', size=11)
    o += text(430, 90, 'CL', '', size=15, weight=700) + text(430, 108, 'study language', 'mut', size=11) + text(430, 122, 'with computers', 'mut', size=11)
    o += text(315, 215, 'NLU', '', size=15, weight=700) + text(315, 232, 'understand meaning', 'mut', size=11)
    o += text(315, 140, 'shared', 'mut', size=11) + text(315, 154, 'methods', 'mut', size=11)
    return fig('nlp-venn', 630, 270, o, 'NLP (engineering goal), CL (scientific goal) and NLU (the meaning part) overlap heavily: they share the same data, models and evaluation methods.')
add('03-nlp-nlu-cl.html', 'Three names that sound alike', venn3())

def recipe():
    st = ['Collect\ndata', 'Annotate\n(labels)', 'Choose a\nmodel', 'Train', 'Evaluate', 'Error\nanalysis']
    o = ''
    for i, s in enumerate(st):
        x = 15 + i * 128
        o += box(x, 30, 104, 56, s, 'bx1' if i in (0, 4) else 'bx', size=12)
        if i < len(st) - 1: o += arrow(x + 106, 58, x + 126, 58)
    o += path('M700,88 C700,135 70,135 70,88', 'ln2', 2, dash='5 4')
    o += text(385, 148, 'improve and repeat', 'ac2', size=11, weight=600)
    return fig('nlu-recipe', 790, 158, o, 'The recipe for building an NLU / CL system is a loop: what you learn from the errors goes back into the data and the model.')
add('03-nlp-nlu-cl.html', 'The recipe for building', recipe())

# ---------------------------------------------------------------- 04 Zipf
def zipf_real():
    d = json.load(open(os.path.join(HERE, 'zipf_counts.json')))
    top = d['top']
    pts = [(i + 1, c) for i, (w, c) in enumerate(top) if c > 0]
    xs = np.log10([p[0] for p in pts[:1000]]); ys = np.log10([p[1] for p in pts[:1000]])
    slope, icpt = np.polyfit(xs, ys, 1)
    ax = Axes(70, 20, 380, 220, (1, 2000), (1, 10000), logx=True, logy=True)
    o = ax.frame([1, 10, 100, 1000], [1, 10, 100, 1000, 10000], 'rank (log scale)', 'frequency (log scale)')
    sample = [p for p in pts if p[0] <= 20 or p[0] % 7 == 0]
    o += ax.dots(sample, 'c1', 2.6)
    o += ax.polyline([(1, 10 ** icpt), (2000, 10 ** (icpt + slope * math.log10(2000)))], 'ln2', 2, dash='6 4')
    for w, r in [('the', 1), ('you', 2), ('so', 3)]:
        o += text(ax.px(r) + 8, ax.py(top[r - 1][1]) + 4, w, '', 'start', 11, 600)
    o += text(330, 50, f'best-fit slope = {slope:.2f}', 'ex', 'start', 12, 700)
    # right: top 15 bar chart
    ax2 = Axes(530, 20, 340, 220, (0, top[0][1] * 1.1), (0, top[0][1] * 1.1))
    ax2 = Axes(530, 20, 340, 220, (0, 1), (0, top[0][1] * 1.15))
    lab = [w for w, c in top[:12]]; val = [c for w, c in top[:12]]
    o += ax2.frame([], [0, 2000, 4000, 6000], '', '', yfmt=lambda v: f'{v//1000}k' if v else '0')
    o += bars(ax2, lab, val, 'c1', fmt=lambda v: '', rot=-45)
    o += text(700, 14, 'Top 12 words in our lectures', '', size=12, weight=700)
    cap = (f'Zipf\'s law on real data: all words spoken in the FoVL language lectures (transcripts, {d["tokens"]:,} tokens, {d["types"]:,} word types). '
           f'On log–log axes the rank–frequency points fall close to a straight line with slope ≈ {slope:.1f} (Zipf predicts −1). A few words ("the", "you", "so") do most of the work.')
    return fig('zipf-real', 900, 300, o, cap)
add('04-zipfs-law.html', "Zipf's discovery", zipf_real())

def dice():
    from itertools import product
    cnt = {}
    for a, b, c in product(range(1, 7), repeat=3): cnt[a + b + c] = cnt.get(a + b + c, 0) + 1
    ax = Axes(60, 20, 360, 190, (0, 1), (0, 30))
    o = ax.frame([], [0, 10, 20, 27], 'sum of three dice', 'ways (out of 216)')
    o += bars(ax, [str(s) for s in range(3, 19)], [cnt[s] for s in range(3, 19)], 'c3', fmt=lambda v: '', lsize=10)
    o += text(240, 14, 'Normal-ish: most values in the middle', '', size=12, weight=700)
    ax2 = Axes(520, 20, 340, 190, (0, 1), (0, 1.05))
    vals = [1 / r for r in range(1, 17)]
    o += ax2.frame([], [0, .5, 1], 'word rank', 'relative frequency', yfmt=lambda v: f'{v:g}')
    o += bars(ax2, [str(r) for r in range(1, 17)], vals, 'c1', fmt=lambda v: '', lsize=10)
    o += text(690, 14, 'Zipfian: f ∝ 1/rank, a long tail', '', size=12, weight=700)
    return fig('dice-vs-zipf', 900, 250, o, 'The class contrast. Left: sums of three dice range from 3 to 18 and pile up in the middle (a bell shape). Right: word frequencies do not; the 1st word is twice as common as the 2nd, three times the 3rd, and so on.')
add('04-zipfs-law.html', 'The question: are words', dice())

# ---------------------------------------------------------------- 05 Shannon
def shannon_model():
    st = [('Information\nsource', 'bx1'), ('Transmitter\n(encoder)', 'bx'), ('Channel', 'bx'), ('Receiver\n(decoder)', 'bx'), ('Destination', 'bx1')]
    o = ''
    for i, (s, c) in enumerate(st):
        x = 10 + i * 180
        o += box(x, 40, 124, 56, s, c, size=12)
        if i < 4: o += arrow(x + 126, 68, x + 178, 68) + text(x + 152, 58, ['message', 'signal', 'signal\u2032', 'message'][i], 'mut', size=10)
    o += box(312, 135, 120, 40, 'Noise source', 'bx2', size=12)
    o += arrow(372, 135, 372, 98, 'ar2')
    return fig('shannon', 890, 190, o, 'Shannon\'s model of communication (1948). Redundancy in the message is what lets the receiver recover it even when noise corrupts the signal.')
add('05-shannon-redundancy.html', 'What is "the signal"?', shannon_model())

def entropy_orders():
    lab = ['equal\nletters', '1st order\n(letter freq.)', '2nd order\n(pairs)', '3rd order\n(triples)', 'Shannon\'s\nhuman est.']
    val = [4.70, 4.14, 3.56, 3.3, 1.3]
    ax = Axes(70, 30, 520, 200, (0, 1), (0, 5))
    o = ax.frame([], [0, 1, 2, 3, 4, 5], '', 'bits per letter')
    n = len(val); bw = ax.w / n
    for i, v in enumerate(val):
        x0 = ax.x + i * bw + bw * .15
        o += f'<rect x="{x0:.1f}" y="{ax.py(v):.1f}" width="{bw*.7:.1f}" height="{ax.py(0)-ax.py(v):.1f}" rx="4" class="{"c1" if i < 4 else "c3"}"/>'
        o += text(x0 + bw * .35, ax.py(v) - 6, f'{v:g}', '', size=12, weight=700)
        for k, l in enumerate(lab[i].split('\n')):
            o += text(x0 + bw * .35, ax.y + ax.h + 16 + k * 13, l, 'mut', size=11)
    o += text(330, 18, 'More context → less surprise per letter', '', size=12, weight=700)
    return fig('entropy-orders', 620, 275, o, 'Entropy of English letters as the model sees more context. log₂26 ≈ 4.7 bits if all letters were equally likely; people guessing with full context need only about 1–1.3 bits, so English is roughly 70–75% redundant. (Classic Shannon-style estimates.)')
add('05-shannon-redundancy.html', 'How redundant is English?', entropy_orders())

def surprisal():
    ax = Axes(70, 20, 420, 200, (0.01, 1), (0, 7))
    pts = [(p, -math.log2(p)) for p in np.linspace(0.01, 1, 200)]
    o = ax.frame([.01, .25, .5, .75, 1], [0, 1, 2, 3, 4, 5, 6, 7], 'probability of the event p', 'surprise = −log₂ p (bits)', xfmt=lambda v: f'{v:g}')
    o += ax.polyline(pts, 'ln1', 3)
    for p, l in [(.5, 'coin: 1 bit'), (.125, 'die-8: 3 bits'), (1 / 26, 'letter: 4.7 bits')]:
        o += ax.dots([(p, -math.log2(p))], 'c2', 5) + text(ax.px(p) + 10, ax.py(-math.log2(p)) - 4, l, '', 'start', 11, 600)
    return fig('surprisal', 520, 270, o, 'Surprise (information) of an outcome falls as its probability rises. Entropy is the <i>average</i> surprise.')
add('05-shannon-redundancy.html', 'Entropy: measuring surprise', surprisal())

# ---------------------------------------------------------------- 06 info theory
def kl_fig():
    lab = ['a', 'b', 'c', 'd']
    p = [.5, .25, .125, .125]; q = [.25, .25, .25, .25]
    kl = sum(pi * math.log2(pi / qi) for pi, qi in zip(p, q))
    ax = Axes(60, 30, 420, 180, (0, 1), (0, .6))
    o = ax.frame([], [0, .2, .4, .6], 'outcome', 'probability', yfmt=lambda v: f'{v:.1f}')
    bw = ax.w / 4
    for i in range(4):
        x0 = ax.x + i * bw + 12
        o += f'<rect x="{x0:.1f}" y="{ax.py(p[i]):.1f}" width="{bw/2-14:.1f}" height="{ax.py(0)-ax.py(p[i]):.1f}" rx="3" class="c1"/>'
        o += f'<rect x="{x0+bw/2-10:.1f}" y="{ax.py(q[i]):.1f}" width="{bw/2-14:.1f}" height="{ax.py(0)-ax.py(q[i]):.1f}" rx="3" class="c4"/>'
        o += text(x0 + bw / 2 - 12, ax.y + ax.h + 16, lab[i], 'mut', size=12)
    o += legend(360, 40, [('c1', 'true P = (½, ¼, ⅛, ⅛)'), ('c4', 'model Q = uniform')])
    o += text(270, 18, f'D(P‖Q) = Σ p log₂(p/q) = {kl:.2f} bits', 'ex', size=13, weight=700)
    return fig('kl', 520, 255, o, 'KL divergence measures the extra bits you pay for coding data from P with a code built for Q. Here H(P) = 1.75 bits but the uniform code costs 2 bits, so D(P‖Q) = 0.25. It is 0 only when P = Q.')
add('06-information-theory.html', 'Relative entropy', kl_fig())

def chain_rule_bar():
    o = ''
    o += rect(40, 40, 600, 40, 'c1o', 6) + text(340, 65, 'H(X, Y)  — total uncertainty of the pair', 'hmt', size=13, weight=700)
    o += rect(40, 95, 260, 40, 'c3o', 6) + text(170, 120, 'H(X)', 'hmt', size=13, weight=700)
    o += rect(300, 95, 340, 40, 'c4o', 6) + text(470, 120, 'H(Y | X): what is left after X', 'hmt', size=13, weight=700)
    o += text(340, 25, 'Chain rule:  H(X, Y) = H(X) + H(Y | X)', '', size=13, weight=700)
    return fig('chain-rule', 680, 150, o, 'The chain rule as a bar: knowing X first removes H(X) of the uncertainty; the rest, H(Y | X), is what a language model tries to make small.')
add('06-information-theory.html', 'The chain rule', chain_rule_bar())

# ---------------------------------------------------------------- 07 n-gram LMs
def bigram_heat():
    words = ['<s>', 'I', 'am', 'Sam', 'do', 'like']
    nxt = ['I', 'am', 'Sam', 'do', 'like', '</s>']
    C = {('<s>', 'Sam'): 3, ('<s>', 'I'): 1, ('<s>', 'do'): 1, ('Sam', 'I'): 3, ('Sam', '</s>'): 2, ('I', 'am'): 2, ('I', 'like'): 2,
         ('I', 'do'): 1, ('am', 'Sam'): 1, ('am', '</s>'): 1, ('do', 'like'): 1, ('do', 'I'): 1, ('like', '</s>'): 2, ('like', 'Sam'): 1}
    tot = {'<s>': 5, 'I': 5, 'am': 2, 'Sam': 5, 'do': 2, 'like': 3}
    M = [[C.get((a, b), 0) / tot[a] for b in nxt] for a in words]
    o = heat(20, 40, 70, 32, words, nxt, M, fmt=lambda v: '0' if v == 0 else (f'{v:.2f}'.rstrip('0').rstrip('.')), vmax=1, rlabel_w=60)
    o += text(260, 16, 'P(next word | previous word) from the class corpus', '', size=12, weight=700)
    o += text(22, 30, 'prev ↓  next →', 'mut', 'start', 10)
    return fig('bigram-heat', 520, 250, o, 'The bigram table of the in-class corpus (each row sums to 1). Reading "Sam I am" is a walk through the darkest cells: P(Sam|&lt;s&gt;) 0.6 × P(I|Sam) 0.6 × P(am|I) 0.4 × P(&lt;/s&gt;|am) 0.5 = 0.072.')
add('07-ngram-language-models.html', 'N-gram models and the Markov assumption', bigram_heat())

def ppl_orders():
    ax = Axes(70, 30, 330, 190, (0, 1), (0, 1000))
    o = ax.frame([], [0, 250, 500, 750, 1000], '', 'perplexity (lower is better)')
    o += bars(ax, ['Unigram', 'Bigram', 'Trigram'], [962, 170, 109], ['c4', 'c1', 'c3'], fmt=lambda v: f'{v:g}', lsize=12)
    o += text(235, 18, 'WSJ test set (slide table)', '', size=12, weight=700)
    return fig('ppl-orders', 440, 255, o, 'More context makes the model less "perplexed": perplexity drops from 962 to 170 to 109 as n grows.')
add('07-ngram-language-models.html', 'Evaluating language models', ppl_orders())

def interp_lambda():
    b = [1 / 3, 1 / 3, 1 / 6, 2 / 9, 0.0294118, 0.206897]
    u = [0.206897, 0.206897, 0.103448, 0.137931, 0.0344828, 0.206897]
    lams = np.linspace(0, 1, 101)
    ppl = []
    for l in lams:
        lp = sum(math.log10(l * bi + (1 - l) * ui) for bi, ui in zip(b, u))
        ppl.append(10 ** (-lp / 6))
    ax = Axes(70, 25, 440, 190, (0, 1), (5.5, 8))
    o = ax.frame([0, .25, .5, .75, 1], [5.5, 6, 6.5, 7, 7.5, 8], 'λ (weight on the smoothed bigram)', 'perplexity', xfmt=lambda v: f'{v:g}', yfmt=lambda v: f'{v:g}')
    o += ax.polyline(list(zip(lams, ppl)), 'ln1', 3)
    for l, lab in [(0, 'unigram only 7.82'), (.5, 'λ = 0.5 → 6.63'), (1, 'bigram only 5.85')]:
        v = ppl[int(round(l * 100))]
        o += ax.dots([(l, v)], 'c2', 5) + text(ax.px(l) + (8 if l < 1 else -8), ax.py(v) + (-8 if l < 1 else 20), lab, '', 'start' if l < 1 else 'end', 11, 600)
    return fig('interp', 540, 265, o, 'Linear interpolation from the SRILM lab notebook: P = λ·P<sub>bigram</sub> + (1−λ)·P<sub>unigram</sub> on "Sam I do like linguistics" (both add-one smoothed, &lt;unk&gt; for linguistics). The three dots are exactly SRILM\'s outputs (7.82454, 6.63422, 5.8464). On this toy sentence more bigram weight always helps; on real dev data the best λ sits in between, which is why you tune it.')
add('07-ngram-language-models.html', 'Hands-on: SRILM toolkit', interp_lambda())

def srilm_flow():
    st = [('training text', 'brown-train.txt'), ('ngram-count', '-order 2 -write'), ('.count file', 'n-gram counts'), ('ngram-count', '-lm -addsmooth / -unk'),
          ('.lm file', 'ARPA probabilities'), ('ngram -ppl', '-debug 2'), ('logprob, ppl', 'per word & per file')]
    o = ''
    for i, (a, b) in enumerate(st):
        x = 10 + i * 126
        cls = 'bx1' if i in (1, 3, 5) else 'bx'
        o += box(x, 30, 112, 56, a, cls, b, size=12)
        if i < 6: o += arrow(x + 113, 58, x + 124, 58)
    o += text(450, 110, 'Step 1: count  →  Step 2: estimate (smooth, back off)  →  Step 3: test (perplexity)', 'mut', size=12)
    return fig('srilm', 900, 125, o, 'The three SRILM steps from the lab handout (SRILM_Activity.pdf). Commands are in the highlighted boxes.')
add('07-ngram-language-models.html', 'Hands-on: SRILM toolkit', srilm_flow())

# ---------------------------------------------------------------- 08 HMM / syntax
def viterbi():
    words = ['crazy', 'killer', 'clown']
    V = {'A': [.25, 0, 0], 'N': [0, .075, .015]}
    o = text(430, 18, 'Viterbi trellis for "crazy killer clown" (HMM model 2)', '', size=13, weight=700)
    xs = [190, 430, 670]; ys = {'A': 70, 'N': 190}
    o += text(60, 74, 'A (adj)', '', 'start', 13, 700) + text(60, 194, 'N (noun)', '', 'start', 13, 700)
    for i, w in enumerate(words):
        o += text(xs[i], 262, f'"{w}"', 'acc', size=13, weight=700)
    # edges
    for i in range(2):
        for a in 'AN':
            for b in 'AN':
                best = (a, b) in [('A', 'N'), ('N', 'N')] and ((i == 0 and a == 'A') or (i == 1 and a == 'N'))
                o += arrow(xs[i] + 38, ys[a], xs[i + 1] - 38, ys[b], 'arb' if best else 'arf', 3 if best else 1.2)
    for i in range(3):
        for t in 'AN':
            v = V[t][i]
            best = (i == 0 and t == 'A') or (i > 0 and t == 'N')
            o += f'<rect x="{xs[i]-36}" y="{ys[t]-20}" width="72" height="40" rx="10" class="{"bx1" if best else "bx"}"/>'
            o += text(xs[i], ys[t] + 5, f'{v:g}', '', size=13, weight=700)
    o += text(310, 225, '0.25 × a(A→N) 1 × b(killer|N) 0.3 = 0.075', 'mut', size=10.5)
    o += text(550, 225, '0.075 × a(N→N) 0.5 × b(clown|N) 0.4 = 0.015', 'mut', size=10.5)
    o += text(120, 290, 'π·b:  A = 0.25 × 1 = 0.25,  N = 0.75 × 0 = 0', 'mut', 'start', 11)
    o += text(120, 306, 'Best path (bold): A → N → N with probability 0.015', 'ex', 'start', 12, 700)
    return fig('viterbi', 860, 320, o, 'Each cell keeps the best probability of reaching that tag at that word; bold arrows are the back-pointers of the winning path. "killer clown" alone gives N N = 0.75 × 0.3 × 0.5 × 0.4 = 0.045 (the class answer).')
add('08-pos-tagging-syntax.html', 'Hidden Markov Model (HMM) tagger', viterbi())

def iob():
    toks = [('The', 'B-NP'), ('little', 'I-NP'), ('girl', 'I-NP'), ('saw', 'B-VP'), ('a', 'B-NP'), ('big', 'I-NP'), ('dog', 'I-NP')]
    o = ''
    x = 20
    for t, tag in toks:
        w = 92
        o += box(x, 70, w - 8, 34, t, 'bx', size=13)
        cls = 'c1' if 'NP' in tag else 'c3'
        o += f'<rect x="{x}" y="112" width="{w-8}" height="24" rx="6" class="{cls}" opacity=".9"/>' + text(x + (w - 8) / 2, 129, tag, 'hmt', size=12, weight=700)
        x += w
    o += f'<rect x="16" y="60" width="268" height="84" rx="12" class="grp" fill="none" stroke-width="2" stroke-dasharray="5 4"/>' + text(150, 52, 'NP chunk', 'acc', size=12, weight=700)
    o += f'<rect x="292" y="60" width="84" height="84" rx="12" class="grp3" fill="none" stroke-width="2" stroke-dasharray="5 4"/>' + text(334, 52, 'VP', 'ex', size=12, weight=700)
    o += f'<rect x="384" y="60" width="268" height="84" rx="12" class="grp" fill="none" stroke-width="2" stroke-dasharray="5 4"/>' + text(518, 52, 'NP chunk', 'acc', size=12, weight=700)
    return fig('iob', 670, 160, o, 'Chunking as tagging: B- starts a chunk, I- continues it, O is outside any chunk. Turning chunks into tags lets the same HMM / neural tagger do chunking.')
add('08-pos-tagging-syntax.html', 'Chunking and B-I-O tags', iob())

# ---------------------------------------------------------------- 09 NN basics
def pats():
    data = [(1, 2), (2, 4), (4, 5)]
    ax = Axes(60, 25, 330, 210, (0, 5), (0, 7))
    o = ax.frame([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7], 'pats', 'wags')
    for (w, b, cls, lab) in [(1, 1.37, 'ln1', 'w=1, b=1.37: C=0.67'), (.25, .68, 'ln4', 'w=0.25, b=0.68: bad fit')]:
        o += ax.polyline([(0, b), (5, w * 5 + b)], cls, 2.5)
        o += text(ax.px(5) - 4, ax.py(w * 5 + b) - 7, lab, '', 'end', 11, 600)
    o += ax.dots(data, 'c2', 6)
    for (x, y) in data:
        yh = x + 1.37
        o += line(ax.px(x), ax.py(y), ax.px(x), ax.py(yh), 'res', 1.5, '3 3')
    # right: cost curve over b with w = 1
    ax2 = Axes(500, 25, 360, 210, (0, 3), (0, 7))
    bs = np.linspace(0, 3, 121)
    C = [sum((y - x - b) ** 2 for x, y in data) for b in bs]
    o += ax2.frame([0, .5, 1, 1.5, 2, 2.5, 3], [0, 1, 2, 3, 4, 5, 6, 7], 'bias b (w fixed at 1)', 'cost C = Σ (y − ŷ)²', xfmt=lambda v: f'{v:g}')
    o += ax2.polyline(list(zip(bs, C)), 'ln1', 3)
    # gradient descent steps from b=0 with lr .1
    b = 0.0; steps = []
    for k in range(6):
        steps.append((b, sum((y - x - b) ** 2 for x, y in data)))
        g = sum(-2 * (y - x - b) for x, y in data)
        b -= .1 * g
    o += ax2.polyline(steps, 'ln2', 1.5, dash='4 3') + ax2.dots(steps, 'c2', 4.5)
    o += text(ax2.px(4 / 3), ax2.py(2 / 3) + 22, 'minimum: b = 1.33, C = 0.67', 'ex', size=11, weight=700)
    o += text(ax2.px(0) + 12, ax2.py(steps[0][1]) + 4, 'start: b = 0, C = 6', '', 'start', 11)
    return fig('pats', 900, 290, o, 'Left: the class "pats → wags" data (1→2, 2→4, 4→5) with two candidate lines; dashed red lines are the errors that get squared. Right: the cost as a function of b. Gradient descent (red dots, learning rate 0.1) rolls downhill: b = 0 → 0.8 → 1.12 → 1.25 → … → 1.33.')
add('09-neural-network-basics.html', 'Gradient descent: walking downhill', pats())

def activations():
    ax = Axes(60, 20, 420, 220, (-5, 5), (-1.2, 1.5))
    xs = np.linspace(-5, 5, 201)
    o = ax.frame([-4, -2, 0, 2, 4], [-1, -.5, 0, .5, 1, 1.5], 'z', 'activation', yfmt=lambda v: f'{v:g}')
    o += ax.polyline([(x, 1 / (1 + math.exp(-x))) for x in xs], 'ln1', 3)
    o += ax.polyline([(x, math.tanh(x)) for x in xs], 'ln3', 3)
    o += ax.polyline([(x, min(max(x, 0), 1.5)) for x in xs if x <= 1.5], 'ln4', 3)
    o += legend(90, 40, [('c1', 'sigmoid σ(z) ∈ (0, 1)'), ('c3', 'tanh(z) ∈ (−1, 1)'), ('c4', 'ReLU max(0, z)')])
    return fig('activations', 520, 285, o, 'The three non-linearities from class. Sigmoid squashes to a probability, tanh is zero-centred, and ReLU is cheap and does not saturate for positive z. Their flat regions are where gradients vanish.')
add('09-neural-network-basics.html', 'Non-linearities', activations())

def sigmoid_cls():
    ax = Axes(60, 20, 420, 200, (-6, 6), (0, 1))
    xs = np.linspace(-6, 6, 201)
    o = ax.frame([-6, -3, 0, 3, 6], [0, .5, 1], 'score z = w·x + b', 'P(class = 1)', yfmt=lambda v: f'{v:g}')
    o += line(ax.px(-6), ax.py(.5), ax.px(6), ax.py(.5), 'res', 1.5, '5 4')
    o += ax.polyline([(x, 1 / (1 + math.exp(-x))) for x in xs], 'ln1', 3)
    o += text(ax.px(3), ax.py(.5) + 18, 'predict 1 when σ(z) > 0.5', 'mut', size=11)
    return fig('sigmoid', 520, 265, o, 'The sigmoid turns any score into a probability. The decision boundary is where the score is 0 (σ = 0.5).')
add('09-neural-network-basics.html', 'From regression to classification', sigmoid_cls())

# ---------------------------------------------------------------- 10 word2vec
def window_fig():
    words = ['cats', 'like', 'milk']
    o = text(380, 18, 'Skip-gram training pairs with window = 1 (class notebook corpus)', '', size=12, weight=700)
    x0 = 120
    for i, w in enumerate(words):
        o += box(x0 + i * 120, 40, 96, 36, w, 'bx1' if i == 1 else 'bx', size=13)
    o += arrow(x0 + 168, 80, x0 + 50, 112, 'ar', 2) + arrow(x0 + 168, 80, x0 + 288, 112, 'ar', 2)
    o += text(x0 + 168, 132, 'center "like" → context "cats", "milk"', 'mut', size=11)
    corpus = ['cats like milk', 'cats drink milk', 'dogs like milk', 'dogs chase balls', 'cats chase balls']
    for k, s in enumerate(corpus):
        o += text(560, 50 + k * 18, s, '', 'start', 12)
    o += text(560, 150, '5 sentences × 4 pairs = 20 pairs', 'ex', 'start', 12, 700)
    return fig('sg-window', 780, 165, o, 'Each 3-word sentence gives 4 (center, context) pairs with window 1: (cats, like), (like, cats), (like, milk), (milk, like). Five sentences give the 20 training pairs printed in the notebook.')
add('10-word2vec.html', 'word2vec (Mikolov', window_fig())

def train_w2v():
    corpus = ["cats like milk", "cats drink milk", "dogs like milk", "dogs chase balls", "cats chase balls"]
    sents = [s.split() for s in corpus]
    vocab = sorted(set(w for s in sents for w in s)); wid = {w: i for i, w in enumerate(vocab)}
    V, d, lr, epochs = len(vocab), 3, .05, 500
    pairs = []
    for s in sents:
        ids = [wid[w] for w in s]
        for i, c in enumerate(ids):
            for j in range(max(0, i - 1), min(len(ids), i + 2)):
                if i != j: pairs.append((c, ids[j]))
    np.random.seed(42)
    E = np.random.randn(V, d) * .1; W = np.random.randn(d, V) * .1
    losses = []
    for ep in range(epochs):
        np.random.shuffle(pairs); tl = 0
        for c, ctx in pairs:
            h = E[c].copy(); sc = h @ W; sc -= sc.max(); p = np.exp(sc) / np.exp(sc).sum()
            tl += -math.log(p[ctx] + 1e-12)
            err = p.copy(); err[ctx] -= 1
            gW = np.outer(h, err); gh = W @ err
            W -= lr * gW; E[c] -= lr * gh
        losses.append(tl / len(pairs))
    return vocab, E, losses
vocab, E, losses = train_w2v()

def w2v_plot():
    Ec = E - E.mean(0)
    U, S, Vt = np.linalg.svd(Ec, full_matrices=False)
    P = Ec @ Vt[:2].T
    lo, hi = P.min(0) - .6, P.max(0) + .6
    ax = Axes(50, 25, 360, 240, (lo[0], hi[0]), (lo[1], hi[1]))
    o = ax.frame([], [], '', 'PCA component 2', grid=False)
    groups = {'cats': 'c1', 'dogs': 'c1', 'milk': 'c3', 'balls': 'c3', 'like': 'c2', 'drink': 'c2', 'chase': 'c2'}
    for w, (a, b) in zip(vocab, P):
        o += ax.dots([(a, b)], groups[w], 7) + text(ax.px(a) + 10, ax.py(b) + 4, w, '', 'start', 13, 700)
    o += legend(60, 292, [('c1', 'animals'), ('c2', 'verbs'), ('c3', 'objects')]) + text(230, 292, 'PCA component 1 →', 'mut', size=12)
    ax2 = Axes(520, 25, 340, 240, (0, 500), (0, 2.2))
    o += ax2.frame([0, 100, 200, 300, 400, 500], [0, .5, 1, 1.5, 2], 'epoch', 'average cross-entropy loss', yfmt=lambda v: f'{v:g}')
    o += ax2.polyline(list(enumerate(losses)), 'ln1', 2.5)
    o += text(ax2.px(250), ax2.py(losses[250]) - 12, f'starts at {losses[0]:.2f} ≈ ln 7, ends at {losses[-1]:.2f}', 'mut', size=11)
    return fig('w2v-pca', 900, 330, o, 'Re-running the class word2vec notebook (skip-gram, full softmax, d = 3, window 1, 500 epochs, seed 42). Left: the 7 learned vectors projected to 2-D with PCA, as in the notebook\'s plot; words used in similar contexts land near each other. Right: the training loss starts at ln 7 ≈ 1.95 (a uniform guess over 7 words) and falls as the model learns. The loss cannot reach 0 because one center word has several correct contexts.')
add('10-word2vec.html', 'Cross-entropy loss', w2v_plot())

def onehot_dense():
    o = text(200, 18, 'One-hot (V = 7)', '', size=12, weight=700) + text(610, 18, 'Dense embedding (d = 3)', '', size=12, weight=700)
    for r, w in enumerate(['cats', 'dogs', 'milk']):
        y = 36 + r * 40
        o += text(40, y + 20, w, '', 'end', 12, 700)
        idx = vocab.index(w)
        for k in range(7):
            o += f'<rect x="{55+k*34}" y="{y}" width="30" height="30" rx="4" class="{"c1" if k == idx else "bx"}"/>' + text(70 + k * 34, y + 20, '1' if k == idx else '0', 'hmt' if k == idx else 'mut', size=11)
        o += text(470, y + 20, w, '', 'end', 12, 700)
        for k in range(3):
            v = E[idx][k]
            o += f'<rect x="{485+k*62}" y="{y}" width="58" height="30" rx="4" class="{"c3" if v > 0 else "c4"}" fill-opacity="{min(.25+abs(v)/3,1):.2f}"/>' + text(514 + k * 62, y + 20, f'{v:.2f}', '', size=11, weight=600)
    o += text(200, 170, 'cats · dogs = 0 (every pair is orthogonal)', 'mut', size=11)
    cs = float(E[vocab.index('cats')] @ E[vocab.index('dogs')] / np.linalg.norm(E[vocab.index('cats')]) / np.linalg.norm(E[vocab.index('dogs')]))
    o += text(580, 170, f'cos(cats, dogs) = {cs:.2f} (learned from contexts)', 'ex', size=11, weight=700)
    return fig('onehot-dense', 760, 185, o, 'One-hot vectors are long, sparse and say nothing about similarity. Embeddings are short, dense and learned; the values here are the vectors trained above.')
add('10-word2vec.html', "What's wrong with one-hot vectors?", onehot_dense())

# ---------------------------------------------------------------- 11 neg sampling / GloVe
def negdist():
    corpus = ["cats like milk", "cats drink milk", "dogs like milk", "dogs chase balls", "cats chase balls"]
    from collections import Counter
    c = Counter(w for s in corpus for w in s.split())
    ws = sorted(c); tot = sum(c.values())
    p1 = [c[w] / tot for w in ws]
    p75 = np.array([c[w] ** .75 for w in ws]); p75 = p75 / p75.sum()
    ax = Axes(60, 30, 520, 190, (0, 1), (0, .25))
    o = ax.frame([], [0, .05, .1, .15, .2, .25], '', 'sampling probability', yfmt=lambda v: f'{v:.2f}')
    bw = ax.w / len(ws)
    for i, w in enumerate(ws):
        x0 = ax.x + i * bw + 8
        o += f'<rect x="{x0:.1f}" y="{ax.py(p1[i]):.1f}" width="{bw/2-10:.1f}" height="{ax.py(0)-ax.py(p1[i]):.1f}" rx="3" class="c4"/>'
        o += f'<rect x="{x0+bw/2-6:.1f}" y="{ax.py(p75[i]):.1f}" width="{bw/2-10:.1f}" height="{ax.py(0)-ax.py(p75[i]):.1f}" rx="3" class="c1"/>'
        o += text(x0 + bw / 2 - 8, ax.y + ax.h + 16, f'{w} ({c[w]})', 'mut', size=11)
    o += legend(400, 40, [('c4', 'raw frequency c/15'), ('c1', 'word2vec: c^0.75, renormalised')])
    o += text(320, 18, 'Negative-sampling distribution for the class toy corpus', '', size=12, weight=700)
    return fig('negdist', 620, 260, o, f'Raising counts to the power 0.75 flattens the distribution: frequent words (cats, milk: {p1[1]:.2f} → {p75[1]:.2f}) are picked a bit less, the rare "drink" a bit more ({p1[ws.index("drink")]:.3f} → {p75[ws.index("drink")]:.3f}). This is the exact rule in the class negative-sampling notebook (K = 3 negatives per positive pair).')
add('11-negative-sampling-glove.html', 'Negative sampling', negdist())

def glove_heat():
    corpus = ["ice is solid", "ice melts in water", "steam is a gas", "water turns into steam", "ice and water are related",
              "steam and gas are related", "cats drink milk", "dogs drink milk", "cats like milk", "dogs chase balls"]
    from collections import defaultdict
    X = defaultdict(float)
    for s in corpus:
        t = s.split()
        for i, a in enumerate(t):
            for j in range(max(0, i - 2), min(len(t), i + 3)):
                if i != j: X[(a, t[j])] += 1 / abs(i - j)
    rows = ['ice', 'steam', 'water', 'gas', 'milk']
    cols = ['solid', 'gas', 'water', 'related', 'is', 'drink']
    M = [[X[(r, c)] for c in cols] for r in rows]
    o = heat(10, 40, 72, 32, rows, cols, M, fmt=lambda v: '0' if v == 0 else f'{v:.2f}'.rstrip('0').rstrip('.'), vmax=2, rlabel_w=60)
    o += text(260, 16, 'Weighted co-occurrence X (window 2, weight 1/distance)', '', size=12, weight=700)
    return fig('glove-x', 520, 225, o, 'Part of the co-occurrence matrix built by the class GloVe notebook. A neighbour 1 word away adds 1, 2 words away adds ½. "ice is solid": X(ice, solid) = ½. GloVe then learns vectors so that w<sub>i</sub>·w̃<sub>j</sub> + b<sub>i</sub> + b̃<sub>j</sub> ≈ log X<sub>ij</sub>.')
add('11-negative-sampling-glove.html', 'Co-occurrence matrices', glove_heat())

def ratio_fig():
    lab = ['solid', 'gas', 'water', 'fashion']; val = [8.9, 0.085, 1.36, 0.96]
    ax = Axes(70, 30, 400, 190, (0, 1), (0.05, 20), logy=True)
    o = ax.frame([], [.1, 1, 10], 'probe word k', 'P(k|ice) / P(k|steam)  (log)', yfmt=lambda v: f'{v:g}')
    o += line(ax.x, ax.py(1), ax.x + ax.w, ax.py(1), 'res', 1.5, '5 4')
    bw = ax.w / 4
    for i, v in enumerate(val):
        x0 = ax.x + i * bw + bw * .2
        y1, y0 = sorted([ax.py(v), ax.py(1)])
        cls = 'c1' if v > 2 else ('c2' if v < .5 else 'c4')
        o += f'<rect x="{x0:.1f}" y="{y1:.1f}" width="{bw*.6:.1f}" height="{y0-y1:.1f}" rx="3" class="{cls}"/>'
        o += text(x0 + bw * .3, (y1 - 6) if v > 1 else (y0 + 14), f'{v:g}', '', size=12, weight=700)
        o += text(x0 + bw * .3, ax.y + ax.h + 16, lab[i], 'mut', size=12)
    return fig('glove-ratio', 500, 260, o, 'The GloVe insight: ratios of co-occurrence probabilities separate meanings. Far above 1 → related to ice (solid); far below 1 → related to steam (gas); near 1 → related to both (water) or neither (fashion).')
add('11-negative-sampling-glove.html', 'GloVe', ratio_fig())

# ---------------------------------------------------------------- 12 evaluation
def analogy():
    o = ''
    P = {'man': (80, 200), 'woman': (80, 80), 'king': (360, 210), 'queen': (360, 90)}
    o += arrow(*P['man'], *P['woman'], 'arb', 2.5, 'gender')
    o += arrow(*P['king'], *P['queen'], 'arb', 2.5, 'gender')
    o += arrow(*P['man'], *P['king'], 'ar', 1.5, 'royalty', dash='5 4')
    o += arrow(*P['woman'], *P['queen'], 'ar', 1.5, None, dash='5 4')
    for w, (x, y) in P.items():
        o += circle(x, y, 6, 'c1') + text(x + (12 if x > 200 else -12), y + 5, w, '', 'start' if x > 200 else 'end', 14, 700)
    o += text(560, 110, 'king − man + woman', '', 'middle', 14, 700) + text(560, 134, '≈ queen', 'ex', 'middle', 16, 700)
    o += text(560, 160, 'find the nearest word by cosine', 'mut', size=11)
    return fig('analogy', 700, 240, o, 'Word analogies as parallelograms: the same offset vector (here "gender") appears for many word pairs. Intrinsic test: solve a : b :: c : ? with vector arithmetic.')
add('12-evaluating-embeddings.html', 'Intrinsic evaluation', analogy())

def spearman_fig():
    human = [9.2, 8.5, 7.9, 6.1, 5.0, 3.2, 2.1, 1.0]
    model = [.81, .74, .79, .52, .40, .35, .12, .18]
    rh = np.argsort(np.argsort(-np.array(human))) + 1; rm = np.argsort(np.argsort(-np.array(model))) + 1
    d2 = int(((rh - rm) ** 2).sum()); n = len(human); rho = 1 - 6 * d2 / (n * (n * n - 1))
    ax = Axes(70, 25, 380, 220, (0, 10), (0, 1))
    o = ax.frame([0, 2, 4, 6, 8, 10], [0, .25, .5, .75, 1], 'human similarity score (0–10)', 'model cosine similarity', yfmt=lambda v: f'{v:g}')
    o += ax.dots(list(zip(human, model)), 'c1', 6)
    o += text(560, 70, 'Spearman ρ = 1 − 6Σd² / (n(n²−1))', '', 'middle', 12, 700)
    o += text(560, 95, f'ranks differ by d: Σd² = {d2}, n = {n}', 'mut', 'middle', 11)
    o += text(560, 122, f'ρ = 1 − 6·{d2}/(8·63) = {rho:.3f}', 'ex', 'middle', 13, 700)
    o += text(560, 150, 'compares ORDER, not raw values', 'mut', 'middle', 11)
    return fig('spearman', 700, 290, o, 'How the Word Embeddings assignment scores a model: cosine similarity for each word pair vs the human rating, then Spearman\'s rank correlation per language, averaged over languages (macro average). Eight made-up pairs shown.')
add('12-evaluating-embeddings.html', 'Intrinsic evaluation', spearman_fig())

# ---------------------------------------------------------------- 13 neural LM
def softmax_fig():
    z = [1.8, -2.2, 2.9, -0.3]; ez = np.exp(z); p = ez / ez.sum()
    lab = ['books', 'laptops', 'exams', 'minds']
    ax = Axes(60, 30, 300, 180, (0, 1), (-3, 3.5))
    o = ax.frame([], [-3, -2, -1, 0, 1, 2, 3], '', 'score z = W·x', yfmt=lambda v: f'{v:g}')
    o += line(ax.x, ax.py(0), ax.x + ax.w, ax.py(0), 'ax', 1)
    bw = ax.w / 4
    for i, v in enumerate(z):
        x0 = ax.x + i * bw + bw * .2; y1, y0 = sorted([ax.py(v), ax.py(0)])
        o += f'<rect x="{x0:.1f}" y="{y1:.1f}" width="{bw*.6:.1f}" height="{y0-y1:.1f}" rx="3" class="{"c1" if v > 0 else "c4"}"/>' + text(x0 + bw * .3, (y1 - 5) if v > 0 else (y0 + 13), f'{v:g}', '', size=11, weight=700)
        o += text(x0 + bw * .3, ax.y + ax.h + 16, lab[i], 'mut', size=11)
    o += arrow(380, 120, 450, 120, 'ar', 2.5, 'softmax')
    ax2 = Axes(500, 30, 300, 180, (0, 1), (0, 1))
    o += ax2.frame([], [0, .25, .5, .75, 1], '', 'probability', yfmt=lambda v: f'{v:g}')
    o += bars(ax2, lab, list(p), 'c3', fmt=lambda v: f'{v:.3f}' if v < .01 else f'{v:.2f}')
    return fig('softmax', 840, 245, o, 'Softmax turns raw scores into a probability distribution over the vocabulary: exponentiate, then divide by the sum. Negative scores become tiny but never exactly 0. (Scores from the slide example.)')
add('13-neural-language-models.html', 'A neural language model', softmax_fig())

# ---------------------------------------------------------------- 14 RNN
def unrolled():
    words = ['the', 'students', 'opened', 'their']
    o = ''
    for i, w in enumerate(words):
        x = 60 + i * 175
        o += box(x, 175, 90, 32, w, 'bx', size=12)
        o += arrow(x + 45, 175, x + 45, 140, 'ar', 1.8, None)
        o += text(x + 62, 162, 'Wₑ', 'mut', 'start', 11)
        o += box(x + 5, 95, 80, 44, f'h{i+1}', 'bx1')
        o += arrow(x + 45, 95, x + 45, 60, 'ar', 1.8)
        o += text(x + 62, 82, 'U', 'mut', 'start', 11)
        o += box(x + 10, 22, 70, 36, f'ŷ{i+1}', 'bx', size=12)
        if i < 3: o += arrow(x + 87, 117, x + 178, 117, 'arb', 2.2) + text(x + 132, 110, 'Wₕ', 'acc', size=11, weight=700)
    o += box(-2 + 0, 100, 40, 34, 'h0', 'bx', size=11)
    o += arrow(38, 117, 63, 117, 'arb', 2.2)
    o += text(770, 117, '…', '', size=20)
    return fig('rnn-unrolled', 800, 220, o, 'An RNN unrolled over time. The SAME weights Wₑ (input), Wₕ (recurrent) and U (output) are reused at every step, so the parameter count does not grow with sentence length. hₜ = tanh(Wₕhₜ₋₁ + Wₑxₜ + b).')
add('14-rnns.html', 'The core idea', unrolled())

def vanish():
    ks = list(range(0, 21))
    ax = Axes(70, 20, 440, 220, (0, 20), (1e-6, 1e4), logy=True)
    o = ax.frame([0, 5, 10, 15, 20], [1e-6, 1e-4, 1e-2, 1, 1e2, 1e4], 'number of time steps back (k)', 'gradient factor (log scale)', yfmt=lambda v: {1e-6:'10⁻⁶',1e-4:'10⁻⁴',1e-2:'0.01',1:'1',1e2:'100',1e4:'10⁴'}[v])
    o += ax.polyline([(k, .5 ** k) for k in ks], 'ln1', 3) + ax.polyline([(k, 1.5 ** k) for k in ks], 'ln2', 3)
    o += line(ax.x, ax.py(1), ax.x + ax.w, ax.py(1), 'res', 1, '4 4')
    o += ax.dots([(10, .5 ** 10)], 'c1', 5) + text(ax.px(10) - 8, ax.py(.5 ** 10) + 20, '0.5¹⁰ ≈ 0.00098', '', 'end', 11, 700)
    o += text(ax.px(14), ax.py(1.5 ** 14) - 10, '1.5ᵏ explodes', 'ac2', 'middle', 11, 700)
    o += text(ax.px(16), ax.py(.5 ** 16) - 12, '0.5ᵏ vanishes', 'acc', 'middle', 11, 700)
    return fig('vanish', 540, 285, o, 'Backpropagating through k steps multiplies k similar factors. Below 1 the gradient vanishes (distant words stop influencing learning); above 1 it explodes (fixed by gradient clipping). LSTMs and GRUs fix the vanishing case with gates.')
add('14-rnns.html', 'Vanishing and exploding gradients', vanish())

def lstm():
    o = rect(150, 40, 520, 170, 'bx', 16)
    o += line(130, 70, 700, 70, 'ln1c', 4) + text(705, 74, 'cₜ (cell: long-term memory)', 'acc', 'start', 12, 700) + text(60, 74, 'cₜ₋₁', 'acc', 'start', 12, 700)
    gates = [('forget\ngate f', 'how much old memory to keep', 230), ('input\ngate i', 'how much new info to write', 380), ('output\ngate o', 'how much memory to show', 530)]
    for g, d, x in gates:
        o += box(x - 50, 120, 100, 50, g, 'bx1', size=12)
        o += text(x, 190, d, 'mut', size=10.5)
        o += arrow(x, 120, x, 76, 'ar', 1.6)
    o += text(240, 100, '× f', '', 'start', 12, 700) + text(390, 100, '+ i·c̃', '', 'start', 12, 700) + text(540, 100, 'hₜ = o · tanh(cₜ)', '', 'start', 12, 700)
    o += line(130, 230, 700, 230, 'ln3c', 3) + text(705, 234, 'hₜ (hidden state)', 'ex', 'start', 12, 700) + text(60, 234, 'hₜ₋₁, xₜ', 'ex', 'start', 12, 700)
    return fig('lstm', 900, 250, o, 'An LSTM cell. The cell state is a "conveyor belt": information flows along it with only element-wise × and +, so gradients survive many steps. Each gate is a sigmoid between 0 (block) and 1 (pass). A GRU merges these into two gates (update, reset).')
add('14-rnns.html', 'LSTM and GRU', lstm())

# ---------------------------------------------------------------- 15 attention
def attention_fig():
    H = [(2, 0), (-1, 2), (1, -1), (0, 1)]; s = (1, -2)
    sc = [h[0] * s[0] + h[1] * s[1] for h in H]; e = np.exp(sc); a = e / e.sum()
    c = (sum(ai * h[0] for ai, h in zip(a, H)), sum(ai * h[1] for ai, h in zip(a, H)))
    # left: bar of attention weights
    ax = Axes(60, 30, 300, 190, (0, 1), (0, 1))
    o = ax.frame([], [0, .25, .5, .75, 1], '', 'attention weight α', yfmt=lambda v: f'{v:g}')
    o += bars(ax, [f'h{i+1} (score {sc[i]})' for i in range(4)], list(a), ['c1', 'c4', 'c2', 'c4'], fmt=lambda v: f'{v:.4f}', lsize=10)
    o += text(210, 18, 'scores sᵀhᵢ → softmax → α', '', size=12, weight=700)
    # right: vector geometry
    ax2 = Axes(470, 30, 300, 220, (-2, 3), (-2.5, 2.5))
    o += ax2.frame([-2, -1, 0, 1, 2, 3], [-2, -1, 0, 1, 2], '', '', yfmt=lambda v: f'{v:g}')
    ox, oy = ax2.px(0), ax2.py(0)
    for i, h in enumerate(H):
        o += arrow(ox, oy, ax2.px(h[0]), ax2.py(h[1]), 'ar', 1.6) + text(ax2.px(h[0]) + 10, ax2.py(h[1]) - 4, f'h{i+1}', '', 'start', 12, 700)
    o += arrow(ox, oy, ax2.px(s[0]), ax2.py(s[1]), 'ar3', 2.2) + text(ax2.px(s[0]) + 8, ax2.py(s[1]) + 14, 's (decoder)', 'ex', 'start', 12, 700)
    o += arrow(ox, oy, ax2.px(c[0]), ax2.py(c[1]), 'ar2', 3) + text(ax2.px(c[0]) + 8, ax2.py(c[1]) - 6, f'c = ({c[0]:.2f}, {c[1]:.2f})', 'ac2', 'start', 12, 700)
    return fig('attention', 840, 285, o, 'The class attention numerical drawn out. Left: h₃ points most in the direction of the decoder state s, so it gets 73% of the attention. Right: the context vector c is the α-weighted average of the encoder states and lands close to h₃ (pulled a little toward h₁).')
add('15-seq2seq-attention.html', 'Attention: let the decoder look back', attention_fig())

def attn_heat():
    src = ['il', 'a', 'm\'', 'entarté']; tgt = ['he', 'hit', 'me', 'with', 'a', 'pie']
    M = [[.9, .05, .03, .02], [.1, .6, .1, .2], [.05, .1, .8, .05], [.05, .1, .05, .8], [.05, .2, .05, .7], [.02, .05, .03, .9]]
    o = heat(10, 40, 70, 30, tgt, src, M, vmax=1, rlabel_w=60, fmt=lambda v: f'{v:.2f}')
    o += text(200, 16, 'Decoder word ↓ attends to source word →', '', size=12, weight=700)
    return fig('attn-heat', 360, 235, o, 'An attention map for the slide\'s French example (illustrative weights). One source word ("entarté") gets attention from three target words: attention handles one-to-many alignments for free, with no separate alignment model.')
add('15-seq2seq-attention.html', 'Attention: let the decoder look back', attn_heat())

def bottleneck():
    src = ['il', 'a', 'm\'', 'entarté']; tgt = ['he', 'hit', 'me', 'with', 'a', 'pie']
    o = ''
    for i, w in enumerate(src):
        x = 20 + i * 80
        o += box(x, 150, 64, 28, w, 'bx', size=12) + box(x + 4, 90, 56, 36, 'enc', 'bx1', size=11)
        o += arrow(x + 32, 150, x + 32, 128)
        if i < 3: o += arrow(x + 62, 108, x + 82, 108)
    o += circle(370, 108, 22, 'c2', 'h₄', 'hmt')
    o += arrow(322, 108, 346, 108, 'ar', 2)
    o += text(370, 70, 'bottleneck:', 'ac2', size=11, weight=700) + text(370, 84, 'one vector', 'ac2', size=11, weight=700)
    for i, w in enumerate(tgt):
        x = 420 + i * 72
        o += box(x, 90, 56, 36, 'dec', 'bx1', size=11) + box(x, 30, 56, 28, w, 'bx', size=12)
        o += arrow(x + 28, 90, x + 28, 60)
        if i < 5: o += arrow(x + 58, 108, x + 70, 108)
    o += arrow(392, 108, 418, 108, 'ar', 2)
    return fig('bottleneck', 860, 190, o, 'Plain seq2seq: everything the decoder knows about the source must squeeze through the last encoder state (the bottleneck). Attention removes it by letting each decoder step look at all encoder states.')
add('15-seq2seq-attention.html', 'The bottleneck problem', bottleneck())

# ---------------------------------------------------------------- 16 coref
def coref_fig():
    toks = [('I', 'c1'), ('voted for', None), ('Nader', 'c3'), ('because', None), ('he', 'c3'), ('was most aligned with', None), ('my', 'c1'), ('values,', None), ('she', 'c2'), ('said.', None)]
    o = ''
    x = 15; pos = {}
    for t, c in toks:
        w = len(t) * 8.3 + 18
        if c:
            o += f'<rect x="{x:.1f}" y="40" width="{w:.1f}" height="32" rx="8" class="{c}" opacity=".9"/>' + text(x + w / 2, 61, t, 'hmt', size=13, weight=700)
            pos.setdefault(c, []).append(x + w / 2)
        else:
            o += text(x + w / 2, 61, t, '', size=13)
        x += w + 6
    for c, xs in pos.items():
        for a, b in zip(xs, xs[1:]):
            o += path(f'M{a:.1f},74 C{a:.1f},{110+ (b-a)/12:.1f} {b:.1f},{110+(b-a)/12:.1f} {b:.1f},74', 'ln' + {'c1': '1', 'c3': '3', 'c2': '2'}[c], 2)
    o += legend(20, 150, [('c1', 'cluster 1: {I, my}'), ('c3', 'cluster 2: {Nader, he}'), ('c2', 'cluster 3: {she}')])
    return fig('coref', 760, 200, o, 'The slide sentence with its gold clusters. A mention-pair model scores every pair of mentions; transitive closure then turns the links above the 0.5 threshold into clusters.')
add('16-coreference-resolution.html', 'What is coreference?', coref_fig())

def pair_heat():
    m = ['I', 'Nader', 'he', 'my', 'she']
    S = {('I', 'my'): .98, ('Nader', 'he'): .95, ('I', 'he'): .05, ('I', 'Nader'): .02, ('she', 'I'): .85, ('she', 'Nader'): 0.0}
    M = [[(S.get((a, b)) if S.get((a, b)) is not None else S.get((b, a), 0)) if a != b else 0 for b in m] for a in m]
    o = heat(10, 40, 64, 30, m, m, M, vmax=1, rlabel_w=60, fmt=lambda v: '' if v == 0 else f'{v:.2f}')
    o += text(200, 16, 'Mention-pair scores p(coref) from the slide', '', size=12, weight=700)
    return fig('pair-heat', 400, 210, o, 'Pairwise scores (blank = not given on the slide). Cells above 0.5 become links. Note (she, I) = 0.85 would wrongly join "she" to {I, my} under transitive closure; the page discusses this slide quirk.')
add('16-coreference-resolution.html', 'Model 1: mention pair', pair_heat())

def bcubed():
    o = text(380, 18, 'B-Cubed: score every mention, then average', '', size=12, weight=700)
    o += text(140, 46, 'Gold clusters', 'mut', size=12, weight=700) + text(560, 46, 'System clusters', 'mut', size=12, weight=700)
    gold = [['a', 'b', 'c'], ['d', 'e']]; sysc = [['a', 'b'], ['c', 'd', 'e']]
    def draw(cl, x0):
        out = ''; x = x0
        for k, c in enumerate(cl):
            w = len(c) * 46 + 14
            out += f'<rect x="{x}" y="60" width="{w}" height="50" rx="22" class="{"grp" if k == 0 else "grp3"}" fill="none" stroke-width="2"/>'
            for j, mm in enumerate(c):
                out += circle(x + 30 + j * 46, 85, 16, 'c1' if mm in 'abc' else 'c3', mm, 'hmt')
            x += w + 20
        return out
    o += draw(gold, 40) + draw(sysc, 450)
    o += text(380, 140, 'mention c: system cluster {c, d, e}, gold cluster {a, b, c} → overlap {c}', '', size=11)
    o += text(380, 158, 'precision(c) = 1/3,  recall(c) = 1/3', 'ex', size=12, weight=700)
    return fig('bcubed', 780, 170, o, 'B-Cubed looks at each mention\'s cluster: precision = |system ∩ gold| / |system|, recall = |system ∩ gold| / |gold|. Averaging over all mentions rewards getting most mentions right.')
add('16-coreference-resolution.html', 'Evaluation: B-Cubed', bcubed())

# ---------------------------------------------------------------- 17 QA
def qa_pipe():
    st = [('Question\nprocessing', 'answer type,\nkeywords'), ('Document\nretrieval', 'search engine\n(TF-IDF / BM25)'), ('Passage\nretrieval', 'rank passages\nwith the keywords'), ('Answer\nextraction', 'find the span\nof the right type')]
    o = text(80, 70, '"Who coined the\nterm cyberspace?"'.split('\n')[0], 'acc', 'middle', 12, 700) + text(80, 86, 'term cyberspace?"', 'acc', 'middle', 12, 700)
    for i, (a, b) in enumerate(st):
        x = 160 + i * 175
        o += box(x, 45, 140, 56, a, 'bx1' if i in (0, 3) else 'bx', size=12)
        for k, l in enumerate(b.split('\n')): o += text(x + 70, 122 + k * 14, l, 'mut', size=11)
        o += arrow(x - 33, 73, x - 2, 73)
    o += arrow(862, 73, 880, 73) + text(905, 70, '"William', 'ex', 'middle', 12, 700) + text(905, 86, 'Gibson"', 'ex', 'middle', 12, 700)
    return fig('qa-pipe', 960, 160, o, 'The IR-based factoid QA pipeline from the slides. The answer type (PERSON for "Who") filters candidate spans in the final step.')
add('17-question-answering.html', 'The IR-based pipeline', qa_pipe())

def mrr_fig():
    qs = [('Q1', 1), ('Q2', 3), ('Q3', 2), ('Q4', None)]
    o = ''
    for k, (q, r) in enumerate(qs):
        y = 30 + k * 38
        o += text(30, y + 18, q, '', 'start', 13, 700)
        for j in range(5):
            hit = (r == j + 1)
            o += f'<rect x="{80+j*58}" y="{y}" width="50" height="28" rx="6" class="{"c3" if hit else "bx"}"/>' + text(105 + j * 58, y + 18, f'#{j+1}', 'hmt' if hit else 'mut', size=11, weight=600)
        o += text(400, y + 18, f'1/rank = {("1/" + str(r)) if r else "0 (not found)"}', '', 'start', 12)
    mrr = (1 + 1 / 3 + 1 / 2 + 0) / 4
    o += text(400, 190, f'MRR = (1 + 1/3 + 1/2 + 0) / 4 = {mrr:.3f}', 'ex', 'start', 13, 700)
    return fig('mrr', 680, 205, o, 'Mean Reciprocal Rank: for each question, find the rank of the first correct answer (green) and take 1/rank; then average. A system that always ranks the right answer first scores 1.')
add('17-question-answering.html', 'Evaluating QA', mrr_fig())

# ---------------------------------------------------------------- 18 sentiment
def absa():
    o = text(420, 22, '"The food was delicious but the service was painfully slow."', '', size=13, weight=700)
    o += box(40, 50, 170, 50, 'Aspect\nextraction', 'bx1', size=12)
    o += arrow(212, 75, 270, 55) + arrow(212, 75, 270, 115)
    o += box(272, 35, 170, 40, 'food', 'bx', size=13) + box(272, 95, 170, 40, 'service', 'bx', size=13)
    o += arrow(444, 55, 520, 55) + arrow(444, 115, 520, 115)
    o += f'<rect x="522" y="35" width="200" height="40" rx="10" class="c3"/>' + text(622, 60, 'positive  ("delicious")', 'hmt', size=12, weight=700)
    o += f'<rect x="522" y="95" width="200" height="40" rx="10" class="c2"/>' + text(622, 120, 'negative  ("painfully slow")', 'hmt', size=12, weight=700)
    o += text(420, 165, 'Document-level sentiment would just say "mixed"; ABSA says what is good and what is bad.', 'mut', size=11)
    return fig('absa', 840, 180, o, 'Aspect-based sentiment analysis: first find the aspects, then decide the polarity for each one, usually with attention on the opinion words near each aspect.')
add('18-sentiment-analysis.html', 'Aspect-based sentiment analysis', absa())

def sentiment_scale():
    words = [('terrible', -3), ('bad', -2), ('meh', -.5), ('okay', .5), ('good', 2), ('excellent', 3)]
    ax = Axes(40, 40, 720, 30, (-3.5, 3.5), (0, 1))
    o = f'<defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" class="stopneg"/><stop offset=".5" class="stopmid"/><stop offset="1" class="stoppos"/></linearGradient></defs>'
    o += f'<rect x="40" y="70" width="720" height="14" rx="7" fill="url(#sg)"/>'
    for w, v in words:
        x = ax.px(v)
        o += line(x, 62, x, 92, 'ax', 1.5) + text(x, 54, w, '', size=13, weight=700) + text(x, 110, f'{v:+g}', 'mut', size=11)
    o += text(400, 140, 'Lexicon approach: add up word scores; flip on negation ("not good" → −2).', 'mut', size=11)
    return fig('sent-scale', 800, 155, o, 'A sentiment lexicon places words on a polarity scale. Simple and explainable, but it misses sarcasm, domain shifts ("unpredictable plot" is good, "unpredictable steering" is bad) and context.')
add('18-sentiment-analysis.html', 'Approach 1: sentiment lexicons', sentiment_scale())

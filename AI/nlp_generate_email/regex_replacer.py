import re

replacement_pattern = [
(r'won\'t','will not'),
(r'can\'t', 'cannot'),
(r'i\'m', 'i am'),
(r'ain\'t','is not'),
(r'(\w+)\'ll','\g<1> will'),
(r'(\w+)n\'t', '\g<1> not'),
(r'(\w+)\'ve', '\g<1> have'),
(r'(\w+)\'s', '\g<1> is'),
(r'(\w+)\'re', '\g<1> are'),
(r'(\w+)\'d','\g<1> would')        
]


class RegexReplacer(object):
    def __init__(self, patterns=replacement_pattern):
        self.patterns = [(re.compile(regex), repl) for(regex, repl) in patterns]

    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)
        return s


if __name__ == "__main__":
    rp = RegexReplacer()
    print(rp.replace("can't is a contraction"))
    print(rp.replace("I should've done that thing I didn't do"))


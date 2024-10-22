import re
from tree import TreeNode  # Assuming TreeNode class is in tree.py
from nltk.tree import Tree

def loadRules(file_path):
    rules = {}
    with open(file_path, 'r') as file:
        for ruleLine in file:
            if '->' in ruleLine:
                # Manually split ruleLine into left-hand and right-hand parts
                parts = ruleLine.split('->')
                
                # First part is lefthand, second part is rightHand
                lefthand = parts[0].strip()
                rightHand = parts[1].strip()
                
                # Initialize rightHandOptions list
                rightHandOptions = []
                
                # Split right-hand side by '|' and handle each option
                options = rightHand.split('|')
                for option in options:
                    # Split each option into individual tokens (words) and strip spaces
                    token_list = option.strip().split()
                    rightHandOptions.append(token_list)
                
                # Add the rule to the dictionary
                rules[lefthand] = rightHandOptions
    return rules

def loadLexicon(file_path):
    lexicon = {}
    with open(file_path, 'r') as file:
        for lexiconLine in file:
            if '->' in lexiconLine:
                parts = lexiconLine.split('->')
                lefthand = parts[0].strip()
                rightHand = parts[1].strip()
                       
                # Split right-hand side by '|' and handle each option
                options = rightHand.split('|')
                for option in options:
                    word = option.strip()
                    lexicon[word] = lefthand  # Directly map word to part of speech
    return lexicon

def tokenize(sentence):
    return sentence.lower().split()

def match_rule(tokens, wordTarget, rules, lexicon, index):
    if wordTarget not in rules:
        print(f"No rule found for: {wordTarget}")
        return None, index
    
    node = TreeNode(wordTarget)

    for phrases in rules[wordTarget]:
        temp_index = index
        matched = True

        for phrase in phrases:
            if temp_index < len(tokens):
                token = tokens[temp_index]

                # Match the symbol phrases to words from lexicon
                if token in lexicon and lexicon[token] == phrase:
                    part_node = TreeNode(phrase)
                    token_node = TreeNode(token)
                    part_node.add_child(token_node)
                    node.add_child(part_node)
                    temp_index += 1
                   
                
                # Specifically match an adjective before a noun
                elif phrase == "adj" and token in lexicon and lexicon[token] == "adj":
                    part_node = TreeNode("adj")
                    token_node = TreeNode(token)
                    part_node.add_child(token_node)
                    node.add_child(part_node)
                    temp_index += 1
                    

                # Recursive call for non-terminals (grammar rules)
                elif phrase in rules:
                    sub_tree, temp_index = match_rule(tokens, phrase, rules, lexicon, temp_index)
                    if sub_tree is not None:    
                        node.add_child(sub_tree)
                    else:
                        matched = False
                        break
            else:
                matched = False
                break

        if matched:
            return node, temp_index

    print(f"Failed to match rule: '{wordTarget}'")
    return None, index


# Converts TreeNode to NLTK Tree for graphical output
def nltkTree(node):
    if len(node.children) == 0:
        return node.value
    return Tree(node.value, [nltkTree(child) for child in node.children])

# Parses the sentence and visualizes it with NLTK tree
def parseSentence(sentence, rules, lexicon):
    """Parses a sentence, builds a syntax tree, and displays it using NLTK."""
    tokens = tokenize(sentence)
    parse_tree, index = match_rule(tokens, 'S', rules, lexicon, 0)

    # Check if the parse was successful and all tokens were consumed
    if parse_tree is not None and index == len(tokens):
        print(f"Accepted: {sentence}")

        # Convert to NLTK Tree and draw it
        nltk_tree = nltkTree(parse_tree)
        nltk_tree.draw()  # This will open a window displaying the graphical syntax tree
    else:
        print(f"Rejected: {sentence} (index: {index}, token length: {len(tokens)})")
      
if __name__ == "__main__":
    rules = loadRules("./GrammerRules/rules.txt")
    lexicon = loadLexicon("./GrammerRules/lexicon.txt")
    
    print("Lexicon:", lexicon) 
    
    sentences = [
        "The people dislike the white dog",
        "The people like the white dog",
        "The person dislikes the white dog",
        "The person likes the white dog",
        "A person dislikes the white dog",
        "A person likes the white dog"
    ]
    
    for sentence in sentences:
        parseSentence(sentence, rules, lexicon)

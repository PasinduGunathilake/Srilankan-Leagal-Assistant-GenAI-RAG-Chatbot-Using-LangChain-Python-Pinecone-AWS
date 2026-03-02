import re


# Normal refusal
REFUSAL_MESSAGE=(
    "The query cannot be awared as it is not supported by the provided leagal context. "
    "This response is generated strictly based on the supplied statutory material."
)


# input level rule-based guardrail
# List of regular expression patterns that indicate a legal-related question
# These patterns help detect whether the user's query is about Sri Lankan law
LEGAL_PATTERNS = [

    r"\bact\b",              # Matches the word "act" (e.g., Penal Act)
    r"\bsection\s+\d+",      # Matches "section 5", "section 23", etc.
    r"\blaw\b",              # Matches the word "law"
    r"\bpenalty\b",          # Matches the word "penalty"
    r"\bcourt\b",            # Matches the word "court"
    r"\boffence\b",          # Matches the word "offence"
    r"\bconstitution\b",     # Matches the word "constitution"
    r"\bfine\b",             # Matches the word "fine"
    r"\bregulation\b",       # Matches the word "regulation"
    r"\bminister\b",         # Matches the word "minister"
    r"\bsubsection\b",       # Matches the word "subsection"
    r"\bclause\b",           # Matches the word "clause"
    r"\btribunal\b"          # Matches the word "tribunal"
]

def input_guardrail(query: str) ->bool:
    """
    INPUT-LEVEL GUARDRAIL FUNCTION

    Purpose:
    --------
    Checks whether the user's query appears to be related to Sri Lankan law.

    Returns:
    --------
    True  -> If query looks legal-related
    False -> If query is likely unrelated (e.g., general knowledge)

    How it works:
    -------------
    1. Converts the query to lowercase.
    2. Checks if any legal pattern exists in the query.
    3. If at least one pattern matches → return True.
    4. If no pattern matches → return False.
    """
    # convert query to lowercase
    query_lower = query.lower()

    # check
    for pattern in LEGAL_PATTERNS:

        #if pattern found in query, return it is as related query
        if re.search(pattern, query_lower):
            return True
    
    return False


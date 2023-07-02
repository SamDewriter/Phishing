"""Feature extractor for phishing URL detection."""

import re
from urllib.parse import urlparse

import math
import string

def calculate_entropy(data):
    """Calculate the entropy of a given string."""
    if not data:
        return 0

    entropy = 0
    data_size = len(data)
    for char in string.printable:
        p_x = float(data.count(char)) / data_size
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)

    return entropy

class FeaturesExtractor:
    """Extract features from a URL."""

    def __init__(self, url):
        """Initialize the class."""
        self.url = url
        self.parsed_url = urlparse(url)
        self.url_path = self.parsed_url.path.strip('/')
        self.domain = self.parsed_url.netloc

    def extract_domain_features(self):
        """Extract domain-related features."""
        domain_features = {}
        domain_tokens = self.parsed_url.netloc.split('.')

        # Path-related features
        domain_features['domain_token_count'] = len(domain_tokens)
        domain_features['avgpathtokenlen'] = len(self.url_path.split('/')) / max(1,
                        len(self.url_path.split('/')))

        # Query Length
        domain_features['urlLen'] = len(self.url)
        domain_features['domainlength'] = len(self.parsed_url.netloc)

        # Ratio features
        domain_features['ArgUrlRatio'] = len(self.parsed_url.query) / max(1, len(self.url))
        domain_features['NumberofDotsinURL'] = self.url.count('.')
        domain_features['URL_DigitCount'] = sum(c.isdigit() for c in self.url)
        domain_features['LongestPathTokenLength'] = len(max(self.url.split('/'), key=len))

        domain_features['Filename_LetterCount'] = sum(c.isalpha() for c in
                                                      self.url_path.split('/')[-1])
        domain_features['Path_LongestWordLength'] = len(max(self.url_path.split('/'), key=len))

        # Special Characters in URL
        special_chars = re.findall('[^A-Za-z0-9./-]', self.url)
        domain_features['spcharUrl'] = len(special_chars)

        return domain_features

    def extract_number_features(self):
        """Extract number-related features."""
        number_features = {}

        # Calculate NumberRate_Domain
        domain_chars = sum(1 for char in self.domain if char.isalnum())
        number_rate_domain = domain_chars / len(self.domain)
        number_features['NumberRate_Domain'] = number_rate_domain

        return number_features

    def extract_entropy_features(self):
        """Extract entropy-related features."""
        entropy_features = {}

        # Extract the domain, directory name, filename, and extension
        domain = self.parsed_url.netloc

        # Calculate Entropy_Domain
        entropy_domain = calculate_entropy(domain)
        entropy_features['Entropy_Domain'] = entropy_domain

        return entropy_features

    def all_features(self):
        """Extract all features."""
        domain_features = self.extract_domain_features()
        entropy_features = self.extract_entropy_features()
        number_features = self.extract_number_features()

        return {**domain_features, **number_features,
                **entropy_features,
                               }
